@echo off
title Smart Crop Prediction System - Local Offline Server
echo ========================================================
echo   Smart Crop Prediction System - Starting Offline Server
echo ========================================================
echo.
echo Launching Application on http://localhost:5000 ...
echo Press Ctrl+C in this terminal window anytime to stop.
echo.
timeout /t 2 >nul
start http://localhost:5000
py app.py
pause
