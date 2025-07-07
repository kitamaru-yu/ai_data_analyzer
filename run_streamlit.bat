@echo off
echo 企業データ分析システムを起動中...
echo.

cd /d "c:\Users\kitamaru-yu\Desktop\Github Copilot"

echo Streamlitアプリケーションを起動します...
streamlit run src/ui/streamlit_app.py --server.port 8501

pause
