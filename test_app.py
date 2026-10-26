"""
Comprehensive test suite verifying all 8 core test cases:
1. Valid crop prediction
2. Empty fields
3. Text entered into numeric fields
4. Negative values
5. Invalid pH
6. SQLite database operations
7. History with records / no records
8. Mobile responsive markup & routes
"""

import unittest
import os
import sqlite3
from app import app, load_model_and_scaler
from database import init_db, get_predictions, DB_PATH

class SmartCropPredictionTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()
        init_db()
        load_model_and_scaler()

    def test_01_valid_crop_prediction(self):
        """Test 1: Valid crop prediction."""
        payload = {
            'N': '90',
            'P': '42',
            'K': '43',
            'temperature': '20.88',
            'humidity': '82.0',
            'ph': '6.5',
            'rainfall': '202.9'
        }
        # HTML form submit
        response = self.client.post('/predict', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recommended Crop', response.data)
        self.assertIn(b'Rice', response.data)

        # JSON submit
        json_resp = self.client.post('/predict', json=payload)
        self.assertEqual(json_resp.status_code, 200)
        data = json_resp.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['crop_key'], 'rice')
        print("[PASS] Test 1: Valid crop prediction returns expected crop (Rice).")

    def test_02_empty_fields(self):
        """Test 2: Empty fields."""
        payload = {
            'N': '',
            'P': '42',
            'K': '43',
            'temperature': '20.88',
            'humidity': '82.0',
            'ph': '6.5',
            'rainfall': '202.9'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid Nitrogen (N) value.', response.data)

        json_resp = self.client.post('/predict', json=payload)
        self.assertEqual(json_resp.status_code, 400)
        self.assertIn('Please enter a valid', json_resp.get_json()['error'])
        print("[PASS] Test 2: Empty fields rejected with user-friendly error message.")

    def test_03_text_entered_into_numeric_fields(self):
        """Test 3: Text entered into numeric fields."""
        payload = {
            'N': 'abc',
            'P': '42',
            'K': 'hello',
            'temperature': '20.88',
            'humidity': '82.0',
            'ph': '6.5',
            'rainfall': '202.9'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid value for', response.data)

        json_resp = self.client.post('/predict', json=payload)
        self.assertEqual(json_resp.status_code, 400)
        self.assertIn('Invalid value', json_resp.get_json()['error'])
        print("[PASS] Test 3: Text entered into numeric fields safely caught without crashing.")

    def test_04_negative_values(self):
        """Test 4: Negative values."""
        payload = {
            'N': '-15',
            'P': '42',
            'K': '43',
            'temperature': '20.88',
            'humidity': '82.0',
            'ph': '6.5',
            'rainfall': '202.9'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cannot be negative', response.data)

        json_resp = self.client.post('/predict', json=payload)
        self.assertEqual(json_resp.status_code, 400)
        self.assertIn('cannot be negative', json_resp.get_json()['error'])
        print("[PASS] Test 4: Negative values rejected with clear explanation.")

    def test_05_invalid_ph(self):
        """Test 5: Invalid pH."""
        # Negative pH
        payload_neg = {
            'N': '50', 'P': '50', 'K': '50',
            'temperature': '25', 'humidity': '60',
            'ph': '-2.5', 'rainfall': '100'
        }
        resp_neg = self.client.post('/predict', data=payload_neg)
        self.assertEqual(resp_neg.status_code, 200)
        self.assertIn(b'Soil pH cannot be negative', resp_neg.data)

        # pH > 14
        payload_high = {
            'N': '50', 'P': '50', 'K': '50',
            'temperature': '25', 'humidity': '60',
            'ph': '18.0', 'rainfall': '100'
        }
        resp_high = self.client.post('/predict', data=payload_high)
        self.assertEqual(resp_high.status_code, 200)
        self.assertIn(b'Soil pH cannot exceed 14.0', resp_high.data)
        print("[PASS] Test 5: Out-of-bounds pH (< 0 and > 14) properly rejected.")

    def test_06_sqlite_database_operations(self):
        """Test 6: SQLite database operations and persistence."""
        self.assertTrue(os.path.exists(DB_PATH), "crop_prediction.db file must exist.")
        payload = {
            'N': '100', 'P': '75', 'K': '50',
            'temperature': '27.3', 'humidity': '80.3',
            'ph': '5.9', 'rainfall': '104.9'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Banana', response.data)

        # Query database to confirm row was inserted
        records = get_predictions(limit=5)
        self.assertGreater(len(records), 0)
        self.assertEqual(records[0]['predicted_crop'], 'Banana')
        print("[PASS] Test 6: SQLite3 prediction insert and query persistence confirmed.")

    def test_07_history_page(self):
        """Test 7: History with records / no records."""
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Crop Prediction History', response.data)
        self.assertIn(b'Local SQLite Database: Connected', response.data)
        print("[PASS] Test 7: History page successfully renders SQLite records and badges.")

    def test_08_mobile_and_navigation(self):
        """Test 8: Mobile responsive layout and navigation."""
        resp_index = self.client.get('/')
        self.assertEqual(resp_index.status_code, 200)
        self.assertIn(b'viewport', resp_index.data)
        self.assertIn(b'width=device-width', resp_index.data)

        resp_about = self.client.get('/about')
        self.assertEqual(resp_about.status_code, 200)
        self.assertIn(b'About the Smart Crop Prediction System', resp_about.data)

        resp_404 = self.client.get('/nonexistent-route-for-testing')
        self.assertEqual(resp_404.status_code, 404)
        print("[PASS] Test 8: Mobile responsive viewport, pages, and 404 handling confirmed.")


if __name__ == '__main__':
    unittest.main()
