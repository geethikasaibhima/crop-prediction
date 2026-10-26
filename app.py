import os
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from crop_data import get_crop_info
from database import init_db, save_prediction, get_predictions

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'crop_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

FEATURE_COLUMNS = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('SECRET_KEY must be set in the environment.')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize SQLite database and table automatically on startup
init_db()

# Global variables for model and scaler
model = None
scaler = None


def load_model_and_scaler():
    """Ensures model and scaler are loaded, training them if not present."""
    global model, scaler

    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("[App] Model artifacts missing. Initiating automated training pipeline...")
        from train_model import run_pipeline
        run_pipeline()

    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        print("[App] Model and StandardScaler loaded successfully.")
    except Exception as e:
        print(f"[App Error] Could not load model artifacts: {e}")
        model = None
        scaler = None


# Load model at startup
load_model_and_scaler()


@app.after_request
def add_header(response):
    """Disable caching for static files during development and testing."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def validate_and_parse_input(form_data):
    """
    Validates form input according to agronomic and scientific boundaries.
    Returns (cleaned_dict, error_message).
    """
    field_rules = {
        'N': {'label': 'Nitrogen (N)', 'min': 0.0, 'max': 300.0, 'unit': 'kg/ha'},
        'P': {'label': 'Phosphorus (P)', 'min': 0.0, 'max': 300.0, 'unit': 'kg/ha'},
        'K': {'label': 'Potassium (K)', 'min': 0.0, 'max': 300.0, 'unit': 'kg/ha'},
        'temperature': {'label': 'Temperature', 'min': -10.0, 'max': 60.0, 'unit': '°C'},
        'humidity': {'label': 'Humidity', 'min': 0.0, 'max': 100.0, 'unit': '%'},
        'ph': {'label': 'Soil pH', 'min': 0.0, 'max': 14.0, 'unit': ''},
        'rainfall': {'label': 'Rainfall', 'min': 0.0, 'max': 1000.0, 'unit': 'mm'}
    }

    cleaned = {}
    for col, rule in field_rules.items():
        val_str = form_data.get(col, '').strip()

        if not val_str:
            return None, f"Please enter a valid {rule['label']} value."

        try:
            val = float(val_str)
        except (ValueError, TypeError):
            return None, f"Invalid value for {rule['label']}. Please enter a valid number."

        if val < rule['min']:
            if rule['min'] == 0.0:
                return None, f"{rule['label']} cannot be negative. Please enter a value >= 0."
            return None, f"{rule['label']} must be at least {rule['min']} {rule['unit']}."

        if val > rule['max']:
            return None, f"{rule['label']} cannot exceed {rule['max']} {rule['unit']}."

        cleaned[col] = val

    return cleaned, None


@app.route('/')
def index():
    """Home page rendering the interactive crop prediction form."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Validates user input, preprocesses features, executes ML prediction,
    records in SQLite database, and renders results.
    """
    global model, scaler

    # Ensure model is ready
    if model is None or scaler is None:
        load_model_and_scaler()
        if model is None or scaler is None:
            return render_template('index.html',
                                   error_message="The Machine Learning model is currently initializing. Please try again shortly.",
                                   form_data=request.form)

    # Support JSON and HTML Form submission
    payload = request.get_json(silent=True) or request.form

    cleaned_data, error_message = validate_and_parse_input(payload)
    if error_message:
        if request.is_json:
            return jsonify({'error': error_message}), 400
        return render_template('index.html', error_message=error_message, form_data=payload)

    try:
        # Construct input DataFrame with exact training column order
        input_values = [cleaned_data[col] for col in FEATURE_COLUMNS]
        input_df = pd.DataFrame([input_values], columns=FEATURE_COLUMNS)

        # Apply fitted StandardScaler
        scaled_input = scaler.transform(input_df)

        # Predict primary crop
        prediction = model.predict(scaled_input)[0]
        crop_label = str(prediction).lower()

        # Compute probabilities and top alternatives if supported
        alternatives = []
        confidence_percent = 95.0
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(scaled_input)[0]
            classes = model.classes_
            top_indices = probabilities.argsort()[::-1][:3]

            top_prob = probabilities[top_indices[0]] * 100
            confidence_percent = round(top_prob, 1)

            for idx in top_indices[1:]:
                prob = probabilities[idx] * 100
                if prob >= 1.0:
                    alt_name = classes[idx]
                    alt_info = get_crop_info(alt_name)
                    alternatives.append({
                        'label': alt_name,
                        'name': alt_info['name'],
                        'emoji': alt_info['emoji'],
                        'confidence': round(prob, 1)
                    })

        # Agricultural profile lookup
        crop_info = get_crop_info(crop_label)

        # Save successful prediction to SQLite3 database
        record = {
            'N': cleaned_data['N'],
            'P': cleaned_data['P'],
            'K': cleaned_data['K'],
            'temperature': cleaned_data['temperature'],
            'humidity': cleaned_data['humidity'],
            'ph': cleaned_data['ph'],
            'rainfall': cleaned_data['rainfall'],
            'predicted_crop': crop_info['name']
        }
        db_saved = save_prediction(record)

        if request.is_json:
            return jsonify({
                'success': True,
                'crop': crop_info['name'],
                'crop_key': crop_label,
                'crop_info': crop_info,
                'confidence': confidence_percent,
                'alternatives': alternatives,
                'db_saved': db_saved
            })

        return render_template(
            'result.html',
            crop=crop_info['name'],
            crop_key=crop_label,
            crop_info=crop_info,
            confidence=confidence_percent,
            alternatives=alternatives,
            input_data=cleaned_data,
            db_saved=db_saved
        )

    except Exception as e:
        print(f"[Prediction Error] {e}")
        user_error = "An unexpected error occurred during prediction. Please verify your inputs and try again."
        if request.is_json:
            return jsonify({'error': user_error}), 500
        return render_template('index.html', error_message=user_error, form_data=payload)


@app.route('/history')
def history():
    """Displays previous prediction records from SQLite3 database."""
    records = get_predictions(limit=50)
    return render_template(
        'history.html',
        records=records,
        db_connected=True
    )


@app.route('/about')
def about():
    """Displays information on the system, ML models comparison, and technologies."""
    return render_template('about.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', error_message="The requested page was not found."), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error_message="A system error occurred. Please try again shortly."), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
