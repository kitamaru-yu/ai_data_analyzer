"""
データ分析機能のテスト
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# テスト対象モジュールのインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.data_analyzer import DataAnalyzer
from src.core.config import Config

class TestDataAnalyzer(unittest.TestCase):
    """データ分析機能のテストクラス"""
    
    def setUp(self):
        """テストの前処理"""
        # テスト用のサンプルデータを作成
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=100),
            'sales': np.random.randint(1000, 10000, 100),
            'profit': np.random.randint(100, 1000, 100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'region': np.random.choice(['East', 'West', 'North', 'South'], 100)
        })
        
        self.analyzer = DataAnalyzer(self.sample_data)
    
    def test_init(self):
        """初期化のテスト"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 100)
    
    def test_basic_stats(self):
        """基本統計のテスト"""
        stats = self.analyzer.get_basic_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('stats', stats)
        self.assertIn('column_info', stats)
        self.assertIn('missing_values', stats)
    
    def test_correlation_analysis(self):
        """相関分析のテスト"""
        corr_data = self.analyzer.get_correlation_analysis()
        self.assertIsInstance(corr_data, dict)
        self.assertIn('correlation_matrix', corr_data)
        self.assertIn('insights', corr_data)
    
    def test_categorical_analysis(self):
        """カテゴリカル分析のテスト"""
        cat_data = self.analyzer.get_categorical_analysis()
        self.assertIsInstance(cat_data, dict)
        self.assertIn('category_counts', cat_data)
        self.assertIn('region_counts', cat_data)
    
    def test_time_series_analysis(self):
        """時系列分析のテスト"""
        ts_data = self.analyzer.get_time_series_analysis()
        self.assertIsInstance(ts_data, dict)
        self.assertIn('trends', ts_data)
        self.assertIn('seasonality', ts_data)
    
    def test_outlier_detection(self):
        """外れ値検出のテスト"""
        outliers = self.analyzer.detect_outliers()
        self.assertIsInstance(outliers, dict)
        self.assertIn('outlier_summary', outliers)
        self.assertIn('outlier_data', outliers)
    
    def test_summary_insights(self):
        """サマリー洞察のテスト"""
        summary = self.analyzer.get_summary_insights()
        self.assertIsInstance(summary, dict)
        self.assertIn('key_insights', summary)
        self.assertIn('data_overview', summary)
        self.assertIn('recommendations', summary)

if __name__ == '__main__':
    unittest.main()
