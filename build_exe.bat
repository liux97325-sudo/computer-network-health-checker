@echo off
setlocal
cd /d "%~dp0"
python generate_icon.py
python -m PyInstaller --clean --noconfirm --onefile --windowed --name "电脑网络健康情况检测" --icon network_health.ico app.py
echo.
echo Build finished: dist\电脑网络健康情况检测.exe
pause
