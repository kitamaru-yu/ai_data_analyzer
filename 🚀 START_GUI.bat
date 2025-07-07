@echo off
chcp 65001 >nul
echo [企業データ分析システム] GUI版を起動中...
echo.
cd /d "%~dp0"
python launchers\gui_launcher.py
pause
