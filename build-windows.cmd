@echo off
setlocal
python -m pip install --upgrade pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name BREAK_EXECUTOR break_executor.py
if errorlevel 1 exit /b %errorlevel%
echo.
echo Build concluido: dist\BREAK_EXECUTOR.exe
endlocal
