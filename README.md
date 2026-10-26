# Smart Crop Prediction System 🌱

An intelligent, production-ready, and beginner-friendly agricultural advisory web application that recommends the most suitable crop to cultivate based on soil nutrients and climatic parameters.

---

## 1. Project Title
**Smart Crop Prediction System** — Agricultural Decision Support Web Application.

---

## 2. Project Description
Agriculture faces major challenges when crops are planted in unsuitable soil or suboptimal climatic zones, resulting in low crop yield, nutrient exhaustion, and financial distress. 

The **Smart Crop Prediction System** resolves this by analyzing:
- **Soil Nutrients:** Nitrogen ($N$), Phosphorus ($P$), Potassium ($K$), and Soil pH
- **Climatic Factors:** Ambient Temperature ($^\circ\text{C}$), Relative Humidity ($\%$), and Rainfall ($\text{mm}$)

Using a high-performance **Random Forest Classifier** trained on 2,200 agricultural benchmark records across 22 crops, the system predicts the most compatible crop with **99.55% accuracy**, offers practical agronomic profiles (season, water, soil suitability), and tracks historical recommendations via **SQLite3** (`crop_prediction.db`).

---

## 3. Features
- **Accurate Machine Learning:** Evaluates 4 candidate models (Random Forest, Decision Tree, KNN, Logistic Regression) and deploys the best-performing model.
- **Easy-to-Understand Interface:** Clean agricultural design, intuitive labels, readable typography, and accessible contrasts tailored for farmers and field officers.
- **⚡ One-Click Presets:** Instant quick-fill buttons (Rice Paddy, Cotton Soil, Maize Field, Banana Grove, Apple Orchard, etc.) for effortless testing without manual typing.
- **Crop Information Dossier:** Actionable insights including growing season, suitable soil type, and water requirements for all 22 crop classes.
- **Printable Advisory:** One-click clean print layout (`window.print()`) for extension officers and farmers.
- **Embedded SQLite3 Database:** Automatic initialization and local storage of all prediction records in `crop_prediction.db`.
- **100% Offline Capable:** Runs smoothly without internet connectivity and requires zero external database installation.
- **Input Validation & Safety:** Guards against empty inputs, non-numeric characters, negative values, and extreme out-of-bound measurements without crashing.

---

## 4. Technologies
- **Machine Learning:** Python, Scikit-learn, Pandas, NumPy, Joblib, Matplotlib, Seaborn
- **Backend:** Flask, Python-dotenv
- **Database:** SQLite3 (Python built-in standard library)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Deployment:** Render (with Gunicorn) & Local Windows Execution

---

## 5. Project Structure
```text
smart-crop-prediction/
│
├── dataset/
│   └── Crop_recommendation.csv        # Kaggle Crop Recommendation dataset (2,200 rows)
│
├── model/
│   ├── crop_model.pkl                 # Best trained model (Random Forest, 99.55% accuracy)
│   └── scaler.pkl                     # Fitted StandardScaler artifact
│
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css          # Local Bootstrap 5 stylesheet (offline ready)
│   │   └── style.css                  # Custom agricultural UI styling & print layout
│   ├── js/
│   │   ├── bootstrap.bundle.min.js    # Local Bootstrap 5 bundle (offline ready)
│   │   └── script.js                  # Client validation, preset handlers, and loading UX
│   └── images/
│       ├── model_comparison.png       # Generated ML evaluation plot
│       └── feature_importance.png     # Generated feature importance plot
│
├── templates/
│   ├── index.html                     # Home page & prediction input form
│   ├── result.html                    # Prominent recommendation & agronomic advisory
│   ├── history.html                   # Prediction history ledger
│   └── about.html                     # Project architecture, ML explanation, & tech stack
│
├── crop_data.py                       # Agronomic knowledge base for 22 crops
├── database.py                        # SQLite3 connector with automatic table initialization
├── train_model.py                     # ML pipeline: data inspection, training, & evaluation
├── app.py                             # Flask web server & route handlers
├── run_offline.bat                    # One-click Windows offline launcher
├── test_app.py                        # Automated unit test suite
├── verify_all.py                      # Comprehensive verification audit script
├── crop_prediction.db                 # Auto-generated SQLite3 database file
├── requirements.txt                   # Dependency manifest
├── .env                               # Environment secrets (ignored by Git)
├── .env.example                       # Template for environment configuration
├── .gitignore                         # Git exclusion rules
└── README.md                          # Comprehensive documentation
```

---

## 6. Dataset
- **File:** `dataset/Crop_recommendation.csv`
- **Source:** Kaggle Crop Recommendation Dataset
- **Volume:** 2,200 samples, 8 columns, 0 missing values, 0 duplicates
- **Classes (22 Crops, 100 samples each):** `apple`, `banana`, `blackgram`, `chickpea`, `coconut`, `coffee`, `cotton`, `grapes`, `jute`, `kidneybeans`, `lentil`, `maize`, `mango`, `mothbeans`, `mungbean`, `muskmelon`, `orange`, `papaya`, `pigeonpeas`, `pomegranate`, `rice`, `watermelon`.
- **Features:**
  1. `N`: Nitrogen content in soil ($\text{kg/ha}$)
  2. `P`: Phosphorus content in soil ($\text{kg/ha}$)
  3. `K`: Potassium content in soil ($\text{kg/ha}$)
  4. `temperature`: Ambient temperature in Celsius ($^\circ\text{C}$)
  5. `humidity`: Relative atmospheric humidity ($\%$)
  6. `ph`: Soil acidity / alkalinity score ($0 - 14$)
  7. `rainfall`: Precipitation depth in millimeters ($\text{mm}$)

---

## 7. Installation
Prerequisites:
- Python 3.9 or higher (tested on Python 3.11, 3.12, 3.14)
- Git (optional for cloud deployment)

Clone or navigate to the workspace directory:
```powershell
cd C:\Users\polas\Desktop\crop-prediction
```

---

## 8. Virtual Environment Setup
To isolate project dependencies, create and activate a virtual environment:

### Windows (PowerShell / Command Prompt):
```powershell
py -m venv venv
.\venv\Scripts\activate
```

---

## 9. Package Installation
Install all dependencies listed in `requirements.txt`:
```powershell
py -m pip install -r requirements.txt
```
*(Note: SQLite3 is built directly into Python's standard library, so no separate database installation is needed).*

---

## 10. Model Training
To inspect the CSV, preprocess features with `StandardScaler`, train all 4 classifiers, generate performance charts, and save the best model:

```powershell
py train_model.py
```

### Actual Benchmark Comparison Results:
```text
====================================
MODEL RESULTS
====================================

Random Forest
Accuracy: 0.9955
Precision: 0.9957
Recall: 0.9955
F1 Score: 0.9955

Decision Tree
Accuracy: 0.9795
Precision: 0.9806
Recall: 0.9795
F1 Score: 0.9794

KNN
Accuracy: 0.9795
Precision: 0.9804
Recall: 0.9795
F1 Score: 0.9793

Logistic Regression
Accuracy: 0.9727
Precision: 0.9740
Recall: 0.9727
F1 Score: 0.9725

====================================
BEST MODEL: Random Forest
====================================
```
The trained model is serialized to `model/crop_model.pkl` and scaler to `model/scaler.pkl`.

---

## 11. Database Setup (SQLite3)
Database initialization is **100% automated**. 
When `app.py` launches, `init_db()` in `database.py` creates `crop_prediction.db` and the `predictions` table if they do not already exist:

```sql
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    N REAL NOT NULL,
    P REAL NOT NULL,
    K REAL NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    ph REAL NOT NULL,
    rainfall REAL NOT NULL,
    predicted_crop TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

---

## 12. Environment Variables
Create a file named `.env` in the root folder (a template is provided in `.env.example`):

```ini
PORT=5000
FLASK_ENV=production
SECRET_KEY=replace-with-a-random-secret
```

Generate a secure value with `py -c "import secrets; print(secrets.token_hex(32))"` and use it for `SECRET_KEY`. The app will not start if `SECRET_KEY` is missing.

---

## 13. Running Locally

### Option A: One-Click Windows Launcher
Double-click `run_offline.bat` in the project folder. It will start the server and automatically launch your default browser.

### Option B: Terminal Command
```powershell
py app.py
```
Open your web browser and navigate to:
```text
http://localhost:5000
```

---

## 14. GitHub Setup
The project is hosted at [geethikasaibhima/crop-prediction](https://github.com/geethikasaibhima/crop-prediction). To get a local copy:

Clone the repository:
```powershell
git clone https://github.com/geethikasaibhima/crop-prediction.git
cd crop-prediction
```

To publish later changes:
```powershell
git add .
git commit -m "Describe your changes"
git push origin main
```
*(Note: `.env` and `crop_prediction.db` are automatically ignored by `.gitignore`).*

---

## 15. Render Deployment
Deploy the application on Render in a few clicks:

1. Log in to [Render](https://render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository (`crop-prediction`).
4. Configure the settings:
   - **Name:** `smart-crop-prediction`
   - **Region:** Any close region (e.g., Singapore, Frankfurt, Oregon)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn app:app
     ```
5. In the **Environment Variables** section, add:
   - `SECRET_KEY`: *Any secure random string*
   - `PYTHON_VERSION`: `3.11.9` (or `3.12.0`)
6. Click **Deploy Web Service**.
7. Render will build the environment, start Gunicorn, and automatically initialize `crop_prediction.db`.

---

## 16. Common Errors & Solutions
1. **`ValueError: could not convert string to float`**:
   - *Fix:* Ensure inputs are numeric. The frontend script and backend validation catch and report non-numeric entries with clear user messages.
2. **`sqlite3.OperationalError`**:
   - *Fix:* Ensure the application has write permissions in the project root directory. `database.init_db()` automatically provisions the database.
3. **`FileNotFoundError: model/crop_model.pkl`**:
   - *Fix:* Run `py train_model.py`. The Flask backend is also designed to automatically run training on boot if model files are absent.
4. **`Port 5000 already in use`**:
   - *Fix:* Specify a different port in `.env` (e.g. `PORT=5050`) or run `py app.py`.

---

## 17. Future Enhancements
- Integration of live satellite / OpenWeatherMap weather API for auto-filling temperature, humidity, and rainfall based on GPS location.
- Multi-lingual audio voice input for non-literate farmers.
- Soil NPK sensor integration via IoT microcontrollers (ESP32 / Arduino).
- Fertilizer dosage calculator to adjust nutrient levels for targeted crops.
