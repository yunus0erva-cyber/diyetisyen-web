@echo off
chcp 65001 > nul
title Florya MEV Koleji - Depo, Stok ve Kantin Portali
echo =======================================================
echo    FLORYA MEV KOLEJI - OPERASYON PORTALI BASLATILIYOR
echo =======================================================
echo.

set PYTHON_PATH=C:\Users\doruk\AppData\Local\Programs\Python\Python311\python.exe

if not exist "%PYTHON_PATH%" set PYTHON_PATH=python

echo [1/2] Sistem kontrol ediliyor...
"%PYTHON_PATH%" port_temizle.py > nul 2>&1

echo [2/2] Web sitesi yukleniyor ve internet tarayiciniz aciliyor...
echo.
echo *******************************************************
echo   Web sitesi hazirlaniyor. Bu siyah pencereyi KULLANIM
echo   BITENE KADAR KAPATMAYIN.
echo   Kullanimi bitirince bu pencereyi carpisindan (X)
echo   kapatabilirsiniz, otomatik yedek alinacaktir.
echo *******************************************************
echo.

"%PYTHON_PATH%" -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

echo.
echo =======================================================
echo [OTOMATIK GUVENCE] Program kapatildi, veriler buluta esitleniyor...
echo =======================================================
"%PYTHON_PATH%" yedekle.py

pause
