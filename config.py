"""
システム設定管理モジュール
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# 環境変数を読み込み
load_dotenv()

class Config:
    """システム設定クラス"""
    
    # OpenAI API設定
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    # 分析用モデル設定
    ANALYSIS_MODEL = os.getenv('ANALYSIS_MODEL', 'gpt-4')
    STRATEGY_MODEL = os.getenv('STRATEGY_MODEL', 'gpt-4')
    PROCESSING_MODEL = os.getenv('PROCESSING_MODEL', 'gpt-3.5-turbo')
    
    # API パラメータ
    MAX_TOKENS_ANALYSIS = int(os.getenv('MAX_TOKENS_ANALYSIS', '2000'))
    MAX_TOKENS_STRATEGY = int(os.getenv('MAX_TOKENS_STRATEGY', '2500'))
    MAX_TOKENS_PROCESSING = int(os.getenv('MAX_TOKENS_PROCESSING', '500'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # 利用可能なモデル一覧
    AVAILABLE_MODELS = [
        'gpt-4.1'
        'gpt-4.1-turbo',
        'gpt-4-turbo',
        'gpt-4o-mini',
        'gpt-4o',
        'gpt-4',
        'gpt-3.5-turbo',
        'gpt-3.5-turbo-16k'
    ]
    
    # 可視化設定
    PLOT_DPI = 300
    PLOT_STYLE = 'whitegrid'
    PLOT_PALETTE = 'husl'
    
    @classmethod
    def get_model_config(cls, model_type: str) -> Dict[str, Any]:
        """
        モデル設定を取得
        
        Args:
            model_type: 'analysis', 'strategy', 'processing'
            
        Returns:
            モデル設定辞書
        """
        config_map = {
            'analysis': {
                'model': cls.ANALYSIS_MODEL,
                'max_tokens': cls.MAX_TOKENS_ANALYSIS,
                'temperature': cls.TEMPERATURE
            },
            'strategy': {
                'model': cls.STRATEGY_MODEL,
                'max_tokens': cls.MAX_TOKENS_STRATEGY,
                'temperature': cls.TEMPERATURE + 0.1  # 戦略提案は少し創造的に
            },
            'processing': {
                'model': cls.PROCESSING_MODEL,
                'max_tokens': cls.MAX_TOKENS_PROCESSING,
                'temperature': cls.TEMPERATURE
            }
        }
        
        return config_map.get(model_type, config_map['analysis'])
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        設定の妥当性をチェック
        
        Returns:
            設定が有効かどうか
        """
        if not cls.OPENAI_API_KEY:
            print("エラー: OPENAI_API_KEYが設定されていません")
            return False
        
        if cls.OPENAI_MODEL not in cls.AVAILABLE_MODELS:
            print(f"警告: 未知のモデルが指定されています: {cls.OPENAI_MODEL}")
            print(f"利用可能なモデル: {', '.join(cls.AVAILABLE_MODELS)}")
        
        return True
    
    @classmethod
    def display_config(cls):
        """現在の設定を表示"""
        print("=== システム設定 ===")
        print(f"分析モデル: {cls.ANALYSIS_MODEL}")
        print(f"戦略モデル: {cls.STRATEGY_MODEL}")
        print(f"処理モデル: {cls.PROCESSING_MODEL}")
        print(f"温度パラメータ: {cls.TEMPERATURE}")
        print(f"最大トークン数 (分析): {cls.MAX_TOKENS_ANALYSIS}")
        print(f"最大トークン数 (戦略): {cls.MAX_TOKENS_STRATEGY}")
        print(f"最大トークン数 (処理): {cls.MAX_TOKENS_PROCESSING}")
        print("=" * 20)
