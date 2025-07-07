# 🏢 企業データ分析システム

AI を活用した高度なデータ分析と戦略提案システム

## 🚀 クイック起動

### 最も簡単な方法
```
🚀 START_GUI.bat をダブルクリック
```
美しいGUIランチャーが起動します

### Web版を直接起動
```
📊 START_WEB.bat をダブルクリック
```
ブラウザで http://localhost:8501 が開きます

## 📁 プロジェクト構造

```
📦 企業データ分析システム/
├── 🚀 START_GUI.bat          # メイン起動ファイル
├── 📊 START_WEB.bat          # Web版起動ファイル
├── 📋 main.py                # メインエントリーポイント
├── 📄 requirements.txt       # 依存関係
├── 🔧 .env                   # 環境設定
├── 📖 README.md              # このファイル
├── 📁 src/                   # ソースコード
│   ├── 🎯 core/              # コアモジュール
│   │   ├── config.py         # 設定管理
│   │   ├── data_analyzer.py  # データ分析
│   │   ├── visualizer.py     # 可視化
│   │   └── ai_analyzer.py    # AI分析
│   └── 🎨 ui/                # ユーザーインターフェース
│       └── streamlit_app.py  # Streamlitアプリ
├── 📁 launchers/             # 起動ファイル
│   ├── gui_launcher.py       # GUIランチャー
│   ├── run_streamlit.bat     # Streamlit起動
│   ├── run_tests.bat         # テスト実行
│   └── GUI_Launcher.bat      # 高機能メニュー
├── 📁 data/                  # データファイル
│   ├── business_data.csv     # ビジネスデータ
│   ├── sample_data.csv       # サンプルデータ
│   └── market_context.txt    # 市場情報
├── 📁 docs/                  # ドキュメント
│   ├── README.md            # 詳細な使用方法
│   └── USAGE_GUIDE.md       # 使用ガイド
├── 📁 tests/                 # テストコード
│   ├── test_config.py        # 設定テスト
│   ├── test_data_analyzer.py # 分析テスト
│   └── test_visualizer.py    # 可視化テスト
└── 📁 legacy/                # 旧バージョンファイル
    └── (古いファイル群)
```

## 🎯 主な機能

### 📊 データ分析
- **基本統計分析**: データの概要、分布、傾向を把握
- **相関分析**: 変数間の関係性を発見
- **時系列分析**: 時間的な変化とトレンドを分析
- **外れ値検出**: 異常値や特異なパターンを特定

### 🎨 データ可視化
- **インタラクティブグラフ**: Plotlyを使用した高度な可視化
- **統計チャート**: 分布図、散布図、相関マップ
- **ダッシュボード**: エグゼクティブ向け総合ダッシュボード

### 🤖 AI 戦略提案
- **データ洞察**: AIによる自動的な洞察抽出
- **戦略提案**: ビジネス改善のための具体的な提案
- **次のアクション**: 実行可能な行動計画

## 🔧 利用可能モデル

- **GPT-4.1**: 最新の高性能モデル
- **GPT-4.1 Turbo**: 高性能かつ高速
- **GPT-4**: 標準的な高品質モデル
- **GPT-4 Turbo**: バランスの取れた高性能
- **GPT-4o**: 最適化された高性能モデル
- **GPT-4o Mini**: 軽量で高速
- **GPT-3.5 Turbo**: 高速で経済的
- **GPT-3.5 Turbo 16K**: 長文対応

## 📝 使用方法

1. **起動**: `🚀 START_GUI.bat` をダブルクリック
2. **モデル選択**: 用途に応じてAIモデルを選択
3. **API Key**: OpenAI API Keyを入力
4. **データアップロード**: CSVファイルをアップロード
5. **分析実行**: 分析を実行
6. **結果確認**: 可視化と洞察を確認
7. **レポート**: 結果をダウンロード

## 🛠️ 開発者向け

### 環境設定
```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境のアクティベート
.venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### テスト実行
```bash
# テストランチャーを使用
launchers\run_tests.bat

# 直接実行
python -m pytest tests/ -v
```

### 開発用起動
```bash
# Streamlit開発サーバー
streamlit run src/ui/streamlit_app.py

# メインプログラム
python main.py
```

## 🌟 特徴

- **🎨 美しいUI**: プロフェッショナルなWebインターフェース
- **🤖 AI統合**: 複数のOpenAIモデルに対応
- **📊 高機能**: 包括的なデータ分析機能
- **🚀 簡単起動**: ワンクリックで起動
- **📱 使いやすい**: 直感的な操作
- **🔧 カスタマイズ**: 設定の柔軟な変更

## 📞 サポート

問題が発生した場合は、以下をお試しください：

1. **システム状態確認**: `launchers\GUI_Launcher.bat` → 「システム状態を確認」
2. **テスト実行**: `launchers\run_tests.bat` で動作確認
3. **ログ確認**: コンソール出力でエラーメッセージを確認

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

---

**🎯 今すぐ始める**: `🚀 START_GUI.bat` をダブルクリック！
