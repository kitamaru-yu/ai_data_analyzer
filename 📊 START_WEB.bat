@echo off
chcp 65001 >nul
echo [企業データ分析システム] Web版を起動中...
echo ブラウザで http://localhost:8501 が自動的に開きます
echo * 終了するには Ctrl+C を押してください
echo.
cd /d "%~dp0"
call launchers\run_streamlit.bat
pause
