"""
End-to-End SQLite Flow Test
Verifies the complete pipeline:
HTML form -> POST /predict -> ML model -> predicted crop -> SQLite INSERT -> result.html -> /history -> SQLite SELECT -> prediction displayed
"""

import sys
import sqlite3
from app import app
from database import DB_PATH, get_predictions

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_sqlite_flow():
    print("=" * 60)
    print("RUNNING END-TO-END SQLITE FLOW VERIFICATION")
    print("=" * 60)

    client = app.test_client()

    # 1. Prepare valid test input
    payload = {
        'N': '90',
        'P': '42',
        'K': '43',
        'temperature': '20.8',
        'humidity': '82',
        'ph': '6.5',
        'rainfall': '202'
    }

    # 2. Form -> POST /predict -> ML model -> predicted crop -> result.html
    print("\nStep 1: Submitting HTML Form via POST /predict...")
    resp = client.post('/predict', data=payload, follow_redirects=True)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    assert 'Recommended Crop' in resp.text, "Result page missing 'Recommended Crop' heading!"
    assert 'Rice' in resp.text, "Result page missing predicted crop 'Rice'!"
    print("  -> POST /predict returned HTTP 200 OK with recommended crop 'Rice'.")

    # 3. Direct SQLite verification of the INSERT operation
    print("\nStep 2: Checking SQLite INSERT in crop_prediction.db...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, N, P, K, temperature, humidity, ph, rainfall, predicted_crop, timestamp
        FROM predictions
        ORDER BY id DESC
        LIMIT 1;
    """)
    latest_row = cursor.fetchone()
    conn.close()

    assert latest_row is not None, "No rows found in SQLite database!"
    print(f"  -> Latest row retrieved: id={latest_row['id']}, N={latest_row['N']}, crop='{latest_row['predicted_crop']}', time='{latest_row['timestamp']}'")
    assert latest_row['N'] == 90.0, f"Expected N=90.0, got {latest_row['N']}"
    assert latest_row['P'] == 42.0, f"Expected P=42.0, got {latest_row['P']}"
    assert latest_row['K'] == 43.0, f"Expected K=43.0, got {latest_row['K']}"
    assert latest_row['temperature'] == 20.8, f"Expected temperature=20.8, got {latest_row['temperature']}"
    assert latest_row['humidity'] == 82.0, f"Expected humidity=82.0, got {latest_row['humidity']}"
    assert latest_row['ph'] == 6.5, f"Expected ph=6.5, got {latest_row['ph']}"
    assert latest_row['rainfall'] == 202.0, f"Expected rainfall=202.0, got {latest_row['rainfall']}"
    # Match the formatted agricultural crop name stored by the application ('Rice (Paddy)')
    assert 'Rice' in latest_row['predicted_crop'], f"Expected crop name containing 'Rice', got {latest_row['predicted_crop']}"
    print("  -> SQLite INSERT verified with exact matching columns.")

    # 4. /history -> SQLite SELECT -> prediction displayed
    print("\nStep 3: Checking /history route and SQLite SELECT display...")
    resp_hist = client.get('/history')
    assert resp_hist.status_code == 200, f"Expected 200 OK from /history, got {resp_hist.status_code}"
    assert 'Crop Prediction History' in resp_hist.text, "History page missing header!"
    assert 'Rice' in resp_hist.text, "History page missing newly inserted prediction 'Rice'!"
    assert 'Local SQLite Database: Connected' in resp_hist.text, "History page missing SQLite connection badge!"
    print("  -> /history rendered HTTP 200 OK and successfully displayed the inserted prediction.")

    print("\n" + "=" * 60)
    print("SQLITE FLOW VERIFICATION: 100% PASSED")
    print("=" * 60)
    return True

if __name__ == '__main__':
    test_sqlite_flow()
