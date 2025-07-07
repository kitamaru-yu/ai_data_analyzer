@echo off
echo 企業データ分析システムを起動しています...
echo.
echo 1. コマンドライン版
echo 2. Webアプリケーション版
echo.
set /p choice="選択してください (1 or 2): "

if "%choice%"=="1" (
    echo コマンドライン版を起動します...
    python main.py
) else if "%choice%"=="2" (
    echo Webアプリケーション版を起動します...
    echo ブラウザで http://localhost:8501 にアクセスしてください
    streamlit run streamlit_app.py
) else (
    echo 無効な選択です。
    pause
)

pause
