"""
設定機能のテスト
"""

import unittest
import os
import sys

# テスト対象モジュールのインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.config import Config

class TestConfig(unittest.TestCase):
    """設定機能のテストクラス"""
    
    def test_available_models(self):
        """利用可能なモデルリストのテスト"""
        self.assertIsInstance(Config.AVAILABLE_MODELS, list)
        self.assertGreater(len(Config.AVAILABLE_MODELS), 0)
        self.assertIn('gpt-4', Config.AVAILABLE_MODELS)
        self.assertIn('gpt-3.5-turbo', Config.AVAILABLE_MODELS)
    
    def test_get_model_config(self):
        """モデル設定取得のテスト"""
        analysis_config = Config.get_model_config('analysis')
        self.assertIsInstance(analysis_config, dict)
        self.assertIn('model', analysis_config)
        self.assertIn('max_tokens', analysis_config)
        self.assertIn('temperature', analysis_config)
        
        strategy_config = Config.get_model_config('strategy')
        self.assertIsInstance(strategy_config, dict)
        self.assertIn('model', strategy_config)
        self.assertIn('max_tokens', strategy_config)
        self.assertIn('temperature', strategy_config)
        
        processing_config = Config.get_model_config('processing')
        self.assertIsInstance(processing_config, dict)
        self.assertIn('model', processing_config)
        self.assertIn('max_tokens', processing_config)
        self.assertIn('temperature', processing_config)
    
    def test_get_available_models(self):
        """利用可能なモデル取得のテスト"""
        models = Config.get_available_models()
        self.assertIsInstance(models, list)
        self.assertEqual(models, Config.AVAILABLE_MODELS)
    
    def test_set_model(self):
        """モデル設定のテスト"""
        original_model = Config.ANALYSIS_MODEL
        
        # 有効なモデルの設定
        result = Config.set_model('analysis', 'gpt-4')
        self.assertTrue(result)
        self.assertEqual(Config.ANALYSIS_MODEL, 'gpt-4')
        
        # 無効なモデルの設定
        result = Config.set_model('analysis', 'invalid-model')
        self.assertFalse(result)
        
        # 無効なモデルタイプの設定
        result = Config.set_model('invalid-type', 'gpt-4')
        self.assertFalse(result)
        
        # 元の設定に戻す
        Config.ANALYSIS_MODEL = original_model
    
    def test_get_model_recommendations(self):
        """モデル推奨取得のテスト"""
        cost_effective = Config.get_model_recommendations('cost_effective')
        self.assertIsInstance(cost_effective, list)
        self.assertGreater(len(cost_effective), 0)
        
        high_quality = Config.get_model_recommendations('high_quality')
        self.assertIsInstance(high_quality, list)
        self.assertGreater(len(high_quality), 0)
        
        high_speed = Config.get_model_recommendations('high_speed')
        self.assertIsInstance(high_speed, list)
        self.assertGreater(len(high_speed), 0)
        
        balanced = Config.get_model_recommendations('balanced')
        self.assertIsInstance(balanced, list)
        self.assertGreater(len(balanced), 0)
        
        # 不明な用途の場合はbalancedを返す
        unknown = Config.get_model_recommendations('unknown')
        self.assertEqual(unknown, balanced)
    
    def test_validate_config(self):
        """設定検証のテスト"""
        # 実際の検証は環境に依存するため、メソッドの存在確認のみ
        self.assertTrue(hasattr(Config, 'validate_config'))
        self.assertTrue(callable(Config.validate_config))

if __name__ == '__main__':
    unittest.main()
