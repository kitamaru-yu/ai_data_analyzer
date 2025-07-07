@echo off
title 企業データ分析システム - GUI起動
color 0B
mode con: cols=80 lines=30

:menu
cls
echo.
echo    ╔══════════════════════════════════════════════════════════════════════════╗
echo    ║                     企業データ分析システム                              ║
echo    ║                        GUI インターフェース                              ║
echo    ╚══════════════════════════════════════════════════════════════════════════╝
echo.
echo    🚀 システムメニュー
echo.
echo    [1] GUI アプリケーションを起動 (推奨)
echo    [2] システム状態を確認
echo    [3] 環境設定を表示
echo    [4] テストを実行
echo    [5] 終了
echo.
echo    ═══════════════════════════════════════════════════════════════════════════
echo.
set /p choice="    選択してください (1-5): "

if "%choice%"=="1" goto start_gui
if "%choice%"=="2" goto check_status
if "%choice%"=="3" goto show_config
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" goto exit
goto menu

:start_gui
cls
echo.
echo    🌟 GUI アプリケーションを起動中...
echo.
echo    ブラウザで http://localhost:8501 が自動的に開きます
echo    ※ 終了するには Ctrl+C を押してください
echo.
cd /d "c:\Users\kitamaru-yu\Desktop\Github Copilot"
call .venv\Scripts\activate
streamlit run src/ui/streamlit_app.py --server.port 8501 --server.headless false --browser.gatherUsageStats false
goto menu

:check_status
cls
echo.
echo    📊 システム状態チェック中...
echo.
cd /d "c:\Users\kitamaru-yu\Desktop\Github Copilot"
call .venv\Scripts\activate
python -c "
import sys
print('Python バージョン:', sys.version)
print()
try:
    import streamlit
    print('✓ Streamlit:', streamlit.__version__)
except:
    print('✗ Streamlit: インストールされていません')
try:
    import pandas
    print('✓ Pandas:', pandas.__version__)
except:
    print('✗ Pandas: インストールされていません')
try:
    import plotly
    print('✓ Plotly:', plotly.__version__)
except:
    print('✗ Plotly: インストールされていません')
try:
    from src.core.config import Config
    print('✓ 設定モジュール: OK')
    print('利用可能モデル数:', len(Config.AVAILABLE_MODELS))
except Exception as e:
    print('✗ 設定モジュール:', e)
"
echo.
pause
goto menu

:show_config
cls
echo.
echo    ⚙️ 環境設定を表示中...
echo.
cd /d "c:\Users\kitamaru-yu\Desktop\Github Copilot"
call .venv\Scripts\activate
python -c "
from src.core.config import Config
Config.display_config()
print()
print('利用可能なモデル:')
for i, model in enumerate(Config.AVAILABLE_MODELS, 1):
    print(f'  {i}. {model}')
"
echo.
pause
goto menu

:run_tests
cls
echo.
echo    🧪 テストを実行中...
echo.
cd /d "c:\Users\kitamaru-yu\Desktop\Github Copilot"
call .venv\Scripts\activate
python -m pytest tests/ -v
echo.
pause
goto menu

:exit
cls
echo.
echo    👋 システムを終了します
echo.
echo    ありがとうございました！
echo.
timeout /t 2 /nobreak > nul
exit
