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
        'gpt-4.1',
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
    
    @classmethod
    def get_available_models(cls) -> Dict[str, Dict[str, Any]]:
        """
        利用可能なモデルの詳細情報を取得
        
        Returns:
            モデル情報辞書
        """
        model_info = {
            'gpt-4.1': {
                'name': 'GPT-4.1',
                'description': '最新の高性能モデル',
                'cost': '高',
                'speed': '中',
                'quality': '最高',
                'recommended_for': ['重要な分析', '戦略提案']
            },
            'gpt-4.1-turbo': {
                'name': 'GPT-4.1 Turbo',
                'description': '高性能かつ高速なモデル',
                'cost': '高',
                'speed': '高',
                'quality': '最高',
                'recommended_for': ['リアルタイム分析', 'インタラクティブ利用']
            },
            'gpt-4-turbo': {
                'name': 'GPT-4 Turbo',
                'description': 'バランスの取れた高性能モデル',
                'cost': '中-高',
                'speed': '高',
                'quality': '高',
                'recommended_for': ['一般的な分析', '可視化インサイト']
            },
            'gpt-4o-mini': {
                'name': 'GPT-4o Mini',
                'description': '軽量で高速なモデル',
                'cost': '低-中',
                'speed': '最高',
                'quality': '中-高',
                'recommended_for': ['大量処理', '個別行処理']
            },
            'gpt-4o': {
                'name': 'GPT-4o',
                'description': '最適化された高性能モデル',
                'cost': '中',
                'speed': '高',
                'quality': '高',
                'recommended_for': ['総合分析', 'マルチモーダル']
            },
            'gpt-4': {
                'name': 'GPT-4',
                'description': '標準的な高品質モデル',
                'cost': '中',
                'speed': '中',
                'quality': '高',
                'recommended_for': ['標準分析', '戦略提案']
            },
            'gpt-3.5-turbo': {
                'name': 'GPT-3.5 Turbo',
                'description': '高速で経済的なモデル',
                'cost': '低',
                'speed': '最高',
                'quality': '中',
                'recommended_for': ['大量処理', '開発・テスト']
            },
            'gpt-3.5-turbo-16k': {
                'name': 'GPT-3.5 Turbo 16K',
                'description': '長文対応の経済的モデル',
                'cost': '低',
                'speed': '高',
                'quality': '中',
                'recommended_for': ['長文分析', '大量データ処理']
            }
        }
        return model_info
    
    @classmethod
    def set_model(cls, model_type: str, model_name: str) -> bool:
        """
        モデルを動的に設定
        
        Args:
            model_type: 'analysis', 'strategy', 'processing'
            model_name: 設定するモデル名
            
        Returns:
            設定成功フラグ
        """
        if model_name not in cls.AVAILABLE_MODELS:
            print(f"エラー: 無効なモデル名: {model_name}")
            return False
        
        if model_type == 'analysis':
            cls.ANALYSIS_MODEL = model_name
        elif model_type == 'strategy':
            cls.STRATEGY_MODEL = model_name
        elif model_type == 'processing':
            cls.PROCESSING_MODEL = model_name
        else:
            print(f"エラー: 無効なモデルタイプ: {model_type}")
            return False
        
        print(f"✓ {model_type}モデルを{model_name}に設定しました")
        return True
    
    @classmethod
    def get_model_recommendations(cls, use_case: str) -> list:
        """
        用途に応じたモデル推奨を取得
        
        Args:
            use_case: 'cost_effective', 'high_quality', 'high_speed', 'balanced'
            
        Returns:
            推奨モデルリスト
        """
        recommendations = {
            'cost_effective': ['gpt-3.5-turbo', 'gpt-4o-mini', 'gpt-3.5-turbo-16k'],
            'high_quality': ['gpt-4.1', 'gpt-4.1-turbo', 'gpt-4'],
            'high_speed': ['gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4.1-turbo'],
            'balanced': ['gpt-4o', 'gpt-4-turbo', 'gpt-4']
        }
        return recommendations.get(use_case, recommendations['balanced'])
