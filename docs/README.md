# 企業データ分析・可視化・戦略提案システム

## 🏗️ アーキテクチャ

このシステムは以下のモジュール構成で設計されています：

```
📦 business-data-analyzer/
├── 📁 core modules/
│   ├── config.py           # システム設定管理
│   ├── data_analyzer.py    # データ分析機能
│   ├── visualizer.py       # データ可視化機能
│   └── ai_analyzer.py      # AI分析機能
├── 📁 applications/
│   ├── main.py             # コマンドライン版
│   └── streamlit_app.py    # Webアプリ版
├── 📁 data/
│   ├── business_data.csv   # サンプル企業データ
│   ├── market_context.txt  # 市場コンテキスト
│   └── sample_data.csv     # 基本サンプルデータ
├── 📁 docs/
│   └── USAGE_GUIDE.md      # 使用ガイド
└── 📁 config/
    ├── .env                # 環境変数
    └── requirements.txt    # 依存関係
```

## 🚀 機能概要

### 🔧 設定可能なモデル
環境変数で以下のOpenAIモデルを選択可能：
- **gpt-4o** - 最新の高性能モデル
- **gpt-4** - バランスの取れた高品質モデル  
- **gpt-3.5-turbo** - 高速・コスト効率モデル

### 📊 データ分析機能
- **構造分析**: データ品質、型、欠損値の詳細分析
- **統計分析**: 相関分析、分布分析、異常値検出
- **AI分析**: GPTを使用した高度なパターン認識
- **ビジネスインサイト**: 企業観点からの洞察抽出

### 📈 可視化機能
- **相関行列**: ヒートマップによる変数間関係の可視化
- **分布分析**: ヒストグラム + 密度曲線
- **散布図**: インタラクティブな関係性分析
- **カテゴリ分析**: 棒グラフによる分布表示
- **ダッシュボード**: 統合的な可視化パネル

### 💡 戦略提案機能
- **現状分析**: データドリブンな課題・機会特定
- **行動計画**: 優先度付きアクションプラン
- **成果予測**: KPIと数値目標の設定
- **リスク分析**: 実装時の懸念点と対策
- **ロードマップ**: 短期・中期・長期戦略

## ⚙️ 環境設定

### 1. 基本セットアップ
```bash
# リポジトリをクローン
git clone <repository-url>
cd business-data-analyzer

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 2. 環境変数設定
`.env`ファイルを編集：
```bash
# OpenAI API設定
OPENAI_API_KEY=your_actual_api_key_here

# モデル選択 (推奨設定)
ANALYSIS_MODEL=gpt-4        # 詳細分析用
STRATEGY_MODEL=gpt-4        # 戦略提案用  
PROCESSING_MODEL=gpt-3.5-turbo  # 個別処理用

# パラメータ調整
MAX_TOKENS_ANALYSIS=2000
MAX_TOKENS_STRATEGY=2500
MAX_TOKENS_PROCESSING=500
TEMPERATURE=0.7
```

### 3. モデル選択ガイド

| モデル | 特徴 | 用途 | コスト |
|--------|------|------|--------|
| **gpt-4o** | 最新・最高性能 | 重要な分析・戦略 | 高 |
| **gpt-4** | バランス型 | 通常の分析 | 中 |
| **gpt-3.5-turbo** | 高速・効率的 | 大量処理・開発 | 低 |

## 🖥️ 使用方法

### コマンドライン版
```bash
# 基本起動
python main.py

# または便利なバッチファイル
run_system.bat
```

### Webアプリ版
```bash
streamlit run streamlit_app.py
```
ブラウザで `http://localhost:8501` にアクセス

## 📝 開発・カスタマイズ

### モジュール構成
```python
# 設定管理
from config import Config

# データ分析
from data_analyzer import DataAnalyzer

# 可視化
from visualizer import DataVisualizer

# AI分析
from ai_analyzer import AIAnalyzer

# メインシステム
from main import BusinessDataAnalyzer
```

### カスタムプロンプトの追加
```python
# カスタム分析プロンプト
custom_prompt = """
あなたの業界特有の分析観点:
- 業界KPIの評価
- 競合比較分析  
- 規制環境の考慮
"""

# 実行
result = analyzer.ai_analyze_data(custom_prompt=custom_prompt)
```

### 新しい可視化の追加
```python
# visualizer.py に新しいメソッドを追加
def create_custom_visualization(self, output_path='custom.html'):
    # カスタム可視化ロジック
    pass
```

## 🐛 Git管理

### 基本的なワークフロー
```bash
# 変更の確認
git status

# 変更をステージング
git add .

# コミット
git commit -m "機能追加: 新しい分析手法の実装"

# プッシュ
git push origin main
```

### ブランチ戦略
```bash
# 新機能開発
git checkout -b feature/new-analysis-method

# 修正作業
git checkout -b hotfix/model-configuration

# マージ
git checkout main
git merge feature/new-analysis-method
```

## 📊 サンプルデータ

### 企業データサンプル
`business_data.csv` には以下の指標が含まれます：
- **Company**: 企業名
- **Revenue**: 売上高
- **Employees**: 従業員数
- **Industry**: 業界
- **Profit**: 利益
- **Market_Share**: 市場シェア
- **Customer_Satisfaction**: 顧客満足度
- **Growth_Rate**: 成長率

### 使用例
```python
# システム初期化
analyzer = BusinessDataAnalyzer()

# データ読み込み
df = analyzer.read_csv('business_data.csv')

# 分析実行
structure = analyzer.analyze_data_structure()
ai_analysis = analyzer.ai_analyze_data()
visualizations = analyzer.create_visualizations('dashboard')
strategy = analyzer.generate_business_strategy()
```

## 🛠️ トラブルシューティング

### よくある問題と解決策

**1. モジュールインポートエラー**
```bash
# Python パスの確認
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**2. API Key エラー**
```bash
# .env ファイルの確認
cat .env | grep OPENAI_API_KEY
```

**3. メモリ不足**
```python
# データサイズを制限
df_sample = df.sample(n=1000)  # 1000件にサンプリング
```

**4. 可視化ファイルが開けない**
```python
# ブラウザで直接開く
import webbrowser
webbrowser.open('ai_recommended_charts.html')
```

## 📈 パフォーマンス最適化

### API使用量の最適化
```python
# 軽量モデルを使用
Config.PROCESSING_MODEL = 'gpt-3.5-turbo'

# トークン数を調整  
Config.MAX_TOKENS_ANALYSIS = 1000

# バッチ処理
results = []
for batch in data_batches:
    result = analyzer.process_batch(batch)
    results.extend(result)
```

### メモリ使用量の最適化
```python
# チャンク処理
for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process_chunk(chunk)
```

## 🔒 セキュリティ

### API Key管理
- `.env`ファイルをGitにコミットしない
- 本番環境では環境変数を使用
- 定期的なキーローテーション

### データプライバシー
- 機密データの匿名化
- ローカル処理の推奨
- ログファイルの適切な管理

## 🚀 今後の拡張計画

### v2.0 予定機能
- [ ] リアルタイムデータ連携
- [ ] 機械学習モデル統合
- [ ] 多言語対応
- [ ] クラウドデプロイ対応

### v3.0 予定機能  
- [ ] 業界別テンプレート
- [ ] 自動レポート生成
- [ ] API サーバー化
- [ ] チーム機能

## 📞 サポート

- **Issues**: [GitHub Issues](github-issues-url)
- **Discussions**: [GitHub Discussions](github-discussions-url)
- **Documentation**: [Wiki](wiki-url)

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

---

**企業のデータドリブンな意思決定を支援し、競争優位性の獲得に貢献するシステムです。**
