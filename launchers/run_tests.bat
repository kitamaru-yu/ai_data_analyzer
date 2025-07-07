@echo off
echo テストを実行中...
echo.

cd /d "%~dp0\.."

echo 設定のテストを実行...
python -m pytest tests/test_config.py -v

echo.
echo データ分析のテストを実行...
python -m pytest tests/test_data_analyzer.py -v

echo.
echo 可視化のテストを実行...
python -m pytest tests/test_visualizer.py -v

echo.
echo 全てのテストを実行...
python -m pytest tests/ -v

pause
