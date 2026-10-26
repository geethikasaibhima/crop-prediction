# Smart Crop Prediction System

Use the website to get a crop recommendation based on soil and weather conditions.

## Use the website

1. Open the home page and select **Predict a Crop**.
2. Enter the conditions for your field:
   - **Nitrogen (N), Phosphorus (P), Potassium (K):** soil nutrient values in kg/ha.
   - **Temperature:** degrees Celsius.
   - **Humidity:** percentage.
   - **Soil pH:** acidity or alkalinity, from 0 to 14.
   - **Rainfall:** millimeters.
3. If you do not have field values to hand, choose a quick-fill preset to enter sample values. You can edit them afterward.
4. Select **Predict Suitable Crop**. If a value is missing, not numeric, or outside the accepted range, correct it and submit again.
5. Review the recommended crop, confidence, possible alternatives, and crop guidance for season, suitable soil, and water needs. The entered values are shown for reference.
6. Choose **Predict Another Crop** to try different conditions, **Print Advisory** to print the result, or **View History** to see recent saved predictions.

Use **History** in the navigation to return to recent predictions at any time. History is stored locally by the running application.

## Start the website on Windows

From the project folder, run these commands once to set up the app:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env`, replace the `SECRET_KEY` placeholder with a random secret, then start the site:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Keep the terminal open while using the site; press **Ctrl+C** in it to stop the app.

## Note

Recommendations are general guidance based on the values provided. Local climate, soil testing, and farming practices can affect crop suitability.
