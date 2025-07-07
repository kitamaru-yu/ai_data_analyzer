@echo off
cls
echo ========================================
echo   企業データ分析システム GUI起動
echo ========================================
echo.
echo システムを起動中...
echo.

cd /d "c:\Users\kitamaru-yu\Desktop\Github Copilot"

echo 仮想環境をアクティベート中...
call .venv\Scripts\activate

echo.
echo Streamlit GUI アプリケーションを起動中...
echo ブラウザで http://localhost:8501 が自動的に開きます
echo.
echo ※ 終了するには Ctrl+C を押してください
echo.

streamlit run src/ui/streamlit_app.py --server.port 8501 --server.headless false --browser.gatherUsageStats false

echo.
echo アプリケーションが終了しました
pause
