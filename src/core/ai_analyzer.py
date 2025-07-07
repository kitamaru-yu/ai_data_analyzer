"""
AI分析機能モジュール
"""

import openai
import json
from typing import Dict, Any, Optional
from .config import Config

class AIAnalyzer:
    """AI分析クラス"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI API キー
        """
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API keyが設定されていません")
        
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def analyze_data_with_ai(self, data_info: Dict[str, Any], 
                           data_sample: str,
                           text_context: Optional[str] = None,
                           custom_prompt: Optional[str] = None) -> Optional[str]:
        """
        AIを使用したデータ分析
        
        Args:
            data_info: データの基本情報
            data_sample: データサンプル
            text_context: 追加のテキストコンテキスト
            custom_prompt: カスタムプロンプト
            
        Returns:
            分析結果テキスト
        """
        # テキストデータがある場合は含める
        context_text = ""
        if text_context:
            context_text = f"\n\n追加のテキスト情報:\n{text_context[:1000]}..."
        
        default_prompt = f"""
以下は企業データの分析結果です。このデータを詳しく分析し、ビジネス観点から重要な洞察を提供してください。

データの基本情報:
- 行数: {data_info['basic_info']['shape'][0]}
- 列数: {data_info['basic_info']['shape'][1]}
- 列名: {data_info['basic_info']['columns']}
- データ型: {data_info['basic_info']['data_types']}
- 欠損値: {data_info['basic_info']['missing_values']}

データサンプル:
{data_sample}

数値データの統計:
{json.dumps(data_info['numeric_summary'], indent=2, ensure_ascii=False)}

カテゴリデータの統計:
{json.dumps(data_info['categorical_summary'], indent=2, ensure_ascii=False)}

{context_text}

以下の観点から分析してください:
1. データの特徴と品質
2. 主要な傾向とパターン
3. 異常値や注目すべき点
4. ビジネス上の意味と示唆
5. 推奨される可視化方法
6. データドリブンな意思決定のための提言
"""
        
        prompt = custom_prompt or default_prompt
        model_config = Config.get_model_config('analysis')
        
        try:
            response = self.client.chat.completions.create(
                model=model_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは企業データ分析の専門家です。データを詳しく分析し、ビジネス価値のある洞察を提供してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=model_config['max_tokens'],
                temperature=model_config['temperature']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"AI分析エラー: {e}")
            return None
    
    def analyze_visualization_insights(self, data_info: Dict[str, Any], 
                                     visualization_paths: Dict[str, str]) -> Optional[str]:
        """
        可視化結果からインサイトを分析
        
        Args:
            data_info: データの基本情報
            visualization_paths: 可視化ファイルパス
            
        Returns:
            分析結果テキスト
        """
        prompt = f"""
以下のデータを分析して、可視化グラフから読み取れる重要なビジネスインサイトを提供してください：

データの基本情報:
{json.dumps(data_info, indent=2, ensure_ascii=False)}

作成された可視化:
{list(visualization_paths.keys())}

以下の観点から分析してください:
1. グラフから読み取れる主要なトレンドやパターン
2. 異常値や注目すべきデータポイント
3. データ間の関係性や相関
4. ビジネス上の意味と示唆
5. データの品質や完全性に関する観察
6. 可視化から導かれる具体的なアクション
"""
        
        model_config = Config.get_model_config('analysis')
        
        try:
            response = self.client.chat.completions.create(
                model=model_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは企業データ分析の専門家です。可視化されたデータから重要なビジネスインサイトを抽出してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=model_config['max_tokens'],
                temperature=model_config['temperature']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"可視化インサイト分析エラー: {e}")
            return None
    
    def generate_business_strategy(self, all_analysis: str) -> Optional[str]:
        """
        ビジネス戦略を生成
        
        Args:
            all_analysis: 全分析結果
            
        Returns:
            戦略提案テキスト
        """
        prompt = f"""
以下の企業データ分析結果を基に、具体的なビジネス戦略と次に取るべき行動を提案してください：

{all_analysis}

以下の項目で詳細な提案を作成してください:

1. 現状の課題・機会の特定
2. 推奨される具体的な行動計画（優先度付き）
3. 各行動のメリット・デメリット・懸念点
4. 期待される成果・KPI（可能な場合は数値目標）
5. 実装の難易度と必要リソース
6. 短期・中期・長期の戦略ロードマップ
7. リスク管理と対応策
8. 成功のための重要な成功要因（KSF）

提案は実行可能で、具体的な数値目標を含む形で作成してください。
また、各提案項目に対して実装の優先度（高・中・低）を明記してください。
"""
        
        model_config = Config.get_model_config('strategy')
        
        try:
            response = self.client.chat.completions.create(
                model=model_config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは企業戦略コンサルタントです。データ分析結果から実践的で具体的なビジネス戦略を提案してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=model_config['max_tokens'],
                temperature=model_config['temperature']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"戦略生成エラー: {e}")
            return None
    
    def process_individual_rows(self, data_series, prompt_template: str) -> str:
        """
        個別行の処理
        
        Args:
            data_series: 処理対象のデータ
            prompt_template: プロンプトテンプレート
            
        Returns:
            処理結果テキスト
        """
        prompt = prompt_template.format(data=data_series)
        model_config = Config.get_model_config('processing')
        
        try:
            response = self.client.chat.completions.create(
                model=model_config['model'],
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=model_config['max_tokens'],
                temperature=model_config['temperature']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"処理エラー: {e}"
