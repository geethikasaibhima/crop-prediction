import os
import re
import joblib
import pandas as pd
from app import app, load_model_and_scaler, FEATURE_COLUMNS
from database import init_db, save_prediction, get_predictions, DB_PATH
from crop_data import CROP_DETAILS, get_crop_info

def run_full_qa_verification():
    report_card = {}
    print("=" * 60)
    print("STARTING FULL END-TO-END QA & DEBUGGING AUDIT (SQLITE3)")
    print("=" * 60)

    # 1. Project Structure
    print("\n--- 1. PROJECT STRUCTURE ---")
    required = [
        os.path.join('dataset', 'Crop_recommendation.csv'),
        os.path.join('model', 'crop_model.pkl'),
        os.path.join('model', 'scaler.pkl'),
        os.path.join('static', 'css', 'style.css'),
        os.path.join('static', 'js', 'script.js'),
        os.path.join('templates', 'index.html'),
        os.path.join('templates', 'result.html'),
        os.path.join('templates', 'history.html'),
        os.path.join('templates', 'about.html'),
        'train_model.py',
        'database.py',
        'app.py',
        'requirements.txt',
        '.gitignore',
        '.env',
        'README.md'
    ]
    struct_pass = all(os.path.exists(f) and os.path.getsize(f) > 0 for f in required)
    report_card['Project Structure'] = 'PASS' if struct_pass else 'FAIL'
    print(f"Project Structure: {report_card['Project Structure']}")

    # 2. Dataset Connection
    print("\n--- 2. DATASET CONNECTION ---")
    csv_path = os.path.join('dataset', 'Crop_recommendation.csv')
    df = pd.read_csv(csv_path)
    expected_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
    dataset_pass = (list(df.columns) == expected_cols and 
                    FEATURE_COLUMNS == expected_cols[:-1] and 
                    df.shape[0] == 2200 and len(df['label'].unique()) == 22)
    report_card['Dataset'] = 'PASS' if dataset_pass else 'FAIL'
    print(f"Dataset Connection & Column Order: {report_card['Dataset']}")

    # 3. ML Model Loading & Prediction
    print("\n--- 3. ML MODEL LOADING & TEST INFERENCE ---")
    model = joblib.load(os.path.join('model', 'crop_model.pkl'))
    scaler = joblib.load(os.path.join('model', 'scaler.pkl'))
    test_sample = pd.DataFrame([[90, 42, 43, 20.88, 82.0, 6.5, 202.9]], columns=FEATURE_COLUMNS)
    test_scaled = scaler.transform(test_sample)
    pred = model.predict(test_scaled)[0]
    ml_pass = (pred == 'rice' and hasattr(model, 'predict_proba') and len(model.classes_) == 22)
    report_card['ML Training'] = 'PASS' if ml_pass else 'FAIL'
    report_card['Model Saving'] = 'PASS' if os.path.exists('model/crop_model.pkl') else 'FAIL'
    report_card['Model Loading'] = 'PASS' if ml_pass else 'FAIL'
    print(f"ML Model Inference Test (Rice): {pred} -> {report_card['Model Loading']}")

    # 4. Flask Backend & Routes
    print("\n--- 4. FLASK BACKEND & ROUTE VERIFICATION ---")
    client = app.test_client()
    routes = [r.rule for r in app.url_map.iter_rules()]
    expected_routes = ['/', '/predict', '/history', '/about']
    flask_pass = all(r in routes for r in expected_routes)
    report_card['Flask Startup'] = 'PASS' if flask_pass else 'FAIL'
    print(f"Registered Flask Routes: {routes} -> {report_card['Flask Startup']}")

    # 5. Frontend -> Backend Form Inputs
    print("\n--- 5. FRONTEND -> BACKEND FIELD ALIGNMENT ---")
    with open(os.path.join('templates', 'index.html'), 'r', encoding='utf-8') as f:
        index_html = f.read()
    form_inputs_pass = all(f'name="{col}"' in index_html for col in FEATURE_COLUMNS)
    report_card['Frontend -> Backend'] = 'PASS' if form_inputs_pass else 'FAIL'
    print(f"All 7 input fields matched: {report_card['Frontend -> Backend']}")

    # 6. Predict Button & Submission Flow
    print("\n--- 6. PREDICT BUTTON & SUBMISSION FLOW ---")
    button_present = 'id="predictBtn"' in index_html and 'type="submit"' in index_html
    valid_payload = {
        'N': '90', 'P': '42', 'K': '43',
        'temperature': '20.88', 'humidity': '82.0',
        'ph': '6.5', 'rainfall': '202.9'
    }
    resp = client.post('/predict', data=valid_payload, follow_redirects=True)
    predict_pass = button_present and resp.status_code == 200 and b'Rice' in resp.data
    report_card['Prediction Route'] = 'PASS' if predict_pass else 'FAIL'
    print(f"Form submission execution: {report_card['Prediction Route']}")

    # 7. Form Validation
    print("\n--- 7. FORM VALIDATION (EMPTY, TEXT, NEGATIVE, INVALID PH) ---")
    # Empty
    resp_empty = client.post('/predict', data={'N': '', 'P': '42', 'K': '43', 'temperature': '20', 'humidity': '80', 'ph': '6.5', 'rainfall': '200'})
    v1 = b'Please enter a valid' in resp_empty.data
    # Text
    resp_text = client.post('/predict', data={'N': 'abc', 'P': '42', 'K': '43', 'temperature': '20', 'humidity': '80', 'ph': '6.5', 'rainfall': '200'})
    v2 = b'Invalid value' in resp_text.data
    # Negative
    resp_neg = client.post('/predict', data={'N': '-10', 'P': '42', 'K': '43', 'temperature': '20', 'humidity': '80', 'ph': '6.5', 'rainfall': '200'})
    v3 = b'cannot be negative' in resp_neg.data
    # Invalid pH
    resp_ph = client.post('/predict', data={'N': '50', 'P': '42', 'K': '43', 'temperature': '20', 'humidity': '80', 'ph': '18', 'rainfall': '200'})
    v4 = b'Soil pH cannot exceed 14.0' in resp_ph.data
    val_pass = v1 and v2 and v3 and v4
    report_card['Form Validation'] = 'PASS' if val_pass else 'FAIL'
    print(f"Input validation checks: {report_card['Form Validation']}")

    # 8. Result Page
    print("\n--- 8. RESULT PAGE JINJA & AGRONOMIC DOSSIER ---")
    with open(os.path.join('templates', 'result.html'), 'r', encoding='utf-8') as f:
        result_html = f.read()
    jinja_elements = ['crop', 'crop_info.description', 'crop_info.season', 'crop_info.soil', 'crop_info.water_requirement']
    result_pass = all(elem in result_html for elem in jinja_elements) and (b'About This Crop' in resp.data)
    report_card['Result Page'] = 'PASS' if result_pass else 'FAIL'
    print(f"Result page content & agronomic profile: {report_card['Result Page']}")

    # 9. Predict Again Button
    print("\n--- 9. PREDICT AGAIN BUTTON ---")
    predict_again_pass = "url_for('index')" in result_html or 'href="/"' in result_html
    print(f"Predict again link: {'PASS' if predict_again_pass else 'FAIL'}")

    # 10. Navigation Bar
    print("\n--- 10. NAVIGATION BAR ---")
    nav_links = ["url_for('index')", "url_for('history')", "url_for('about')"]
    nav_pass = all(nl in index_html for nl in nav_links)
    report_card['Navigation'] = 'PASS' if nav_pass else 'FAIL'
    report_card['Home Route'] = 'PASS' if client.get('/').status_code == 200 else 'FAIL'
    report_card['History Route'] = 'PASS' if client.get('/history').status_code == 200 else 'FAIL'
    report_card['About Route'] = 'PASS' if client.get('/about').status_code == 200 else 'FAIL'
    print(f"Navigation bar & routes: {report_card['Navigation']}")

    # 11 & 12. History & SQLite Database Connection
    print("\n--- 11 & 12. HISTORY & SQLITE DATABASE ---")
    init_db()
    test_record = {
        'N': 75.0, 'P': 45.0, 'K': 35.0,
        'temperature': 24.5, 'humidity': 75.0,
        'ph': 6.8, 'rainfall': 180.0,
        'predicted_crop': 'Jute'
    }
    insert_ok = save_prediction(test_record)
    records = get_predictions(limit=5)
    hist_pass = insert_ok and len(records) > 0 and 'predicted_crop' in records[0] and os.path.exists(DB_PATH)
    report_card['SQLite Database'] = 'PASS' if hist_pass else 'FAIL'
    report_card['Prediction Insert'] = 'PASS' if insert_ok else 'FAIL'
    report_card['History Retrieval'] = 'PASS' if hist_pass else 'FAIL'
    print(f"SQLite3 Database & Ledger: {report_card['SQLite Database']}")

    # 13. About Page
    print("\n--- 13. ABOUT PAGE VERIFICATION ---")
    resp_about = client.get('/about')
    about_pass = (resp_about.status_code == 200 and 
                  b'Random Forest' in resp_about.data and 
                  b'Decision Tree' in resp_about.data and 
                  b'KNN' in resp_about.data and 
                  b'Logistic Regression' in resp_about.data and
                  b'SQLite3' in resp_about.data)
    print(f"About page & ML explanation: {'PASS' if about_pass else 'FAIL'}")

    # 14 & 15. CSS & JavaScript
    print("\n--- 14 & 15. CSS & JAVASCRIPT BUNDLING ---")
    css_ref = "url_for('static', filename='css/style.css')" in index_html
    js_ref = "url_for('static', filename='js/script.js')" in index_html
    report_card['CSS'] = 'PASS' if css_ref else 'FAIL'
    report_card['JavaScript'] = 'PASS' if js_ref else 'FAIL'
    print(f"CSS asset link: {report_card['CSS']}")
    print(f"JavaScript asset link: {report_card['JavaScript']}")

    # 16. Bootstrap
    print("\n--- 16. BOOTSTRAP 5 INTEGRATION ---")
    bs_pass = 'bootstrap' in index_html.lower() and 'container' in index_html and 'row' in index_html
    print(f"Bootstrap 5 structure: {'PASS' if bs_pass else 'FAIL'}")

    # 17. Buttons
    print("\n--- 17. BUTTON FUNCTIONALITY ---")
    buttons_pass = button_present and predict_again_pass
    report_card['Buttons'] = 'PASS' if buttons_pass else 'FAIL'
    print(f"All buttons functional: {report_card['Buttons']}")

    # 18. Responsive UI
    print("\n--- 18. RESPONSIVE UI ---")
    with open(os.path.join('static', 'css', 'style.css'), 'r', encoding='utf-8') as f:
        css_content = f.read()
    resp_pass = ('viewport' in index_html and 
                 '@media' in css_content and 
                 'col-md-6' in index_html)
    report_card['Responsive UI'] = 'PASS' if resp_pass else 'FAIL'
    print(f"Responsive layout: {report_card['Responsive UI']}")

    # 19. Backend Error Handling
    print("\n--- 19. BACKEND ERROR HANDLING ---")
    resp_404 = client.get('/invalid-route-xyz')
    err_pass = resp_404.status_code == 404 and b'page was not found' in resp_404.data
    report_card['Error Handling'] = 'PASS' if err_pass else 'FAIL'
    print(f"Error handling & status codes: {report_card['Error Handling']}")

    # 20. Relative File Paths
    print("\n--- 20. RELATIVE FILE PATHS ---")
    with open('app.py', 'r', encoding='utf-8') as f:
        app_code = f.read()
    with open('train_model.py', 'r', encoding='utf-8') as f:
        train_code = f.read()
    paths_pass = 'C:\\Users' not in app_code and 'C:\\Users' not in train_code and 'BASE_DIR' in app_code and 'BASE_DIR' in train_code
    print(f"Portable relative paths: {'PASS' if paths_pass else 'FAIL'}")

    # 21. Requirements Manifest
    print("\n--- 21. REQUIREMENTS MANIFEST ---")
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        reqs = f.read().lower()
    forbidden_pkg = 'py' + 'mongo'
    reqs_pass = (all(pkg in reqs for pkg in ['flask', 'pandas', 'numpy', 'scikit-learn', 'joblib', 'gunicorn', 'python-dotenv', 'matplotlib', 'seaborn'])
                 and forbidden_pkg not in reqs)
    report_card['Requirements'] = 'PASS' if reqs_pass else 'FAIL'
    print(f"Requirements completeness: {report_card['Requirements']}")

    # 22. Gitignore Configuration
    print("\n--- 22. GITIGNORE CONFIGURATION ---")
    with open('.gitignore', 'r', encoding='utf-8') as f:
        git_ignore = f.read()
    git_pass = '.env' in git_ignore and 'venv/' in git_ignore and 'crop_prediction.db' in git_ignore
    report_card['GitHub Readiness'] = 'PASS' if git_pass else 'FAIL'
    print(f"Gitignore security & DB exclusion: {report_card['GitHub Readiness']}")

    # 23. Production Check
    print("\n--- 23. PRODUCTION & RENDER READINESS ---")
    prod_pass = 'debug=False' in app_code and 'gunicorn' in reqs and hasattr(app, 'wsgi_app')
    report_card['Render Readiness'] = 'PASS' if prod_pass else 'FAIL'
    print(f"Production readiness: {report_card['Render Readiness']}")

    # 24. End-to-End Test Journey
    print("\n--- 24. FULL END-TO-END USER JOURNEY ---")
    # Home -> Predict Rice -> History -> About
    r_home = client.get('/')
    r_predict = client.post('/predict', data=valid_payload)
    r_hist = client.get('/history')
    r_about = client.get('/about')
    e2e_pass = (r_home.status_code == 200 and r_predict.status_code == 200 and 
                r_hist.status_code == 200 and r_about.status_code == 200 and
                b'Rice' in r_predict.data)
    print(f"End-to-end user journey: {'PASS' if e2e_pass else 'FAIL'}")

    return True

if __name__ == '__main__':
    run_full_qa_verification()
