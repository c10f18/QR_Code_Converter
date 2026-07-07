@echo off
rem QR Code Converter exe 빌드 스크립트
rem 산출물: dist\QR_Code_Converter.exe
pyinstaller --onefile --windowed --clean --name QR_Code_Converter src\main.py
pause
