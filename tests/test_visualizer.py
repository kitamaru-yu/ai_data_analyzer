"""
可視化機能のテスト
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# テスト対象モジュールのインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.visualizer import DataVisualizer

class TestDataVisualizer(unittest.TestCase):
    """可視化機能のテストクラス"""
    
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
        
        self.visualizer = DataVisualizer(self.sample_data)
    
    def test_init(self):
        """初期化のテスト"""
        self.assertIsNotNone(self.visualizer)
        self.assertIsNotNone(self.visualizer.df)
        self.assertEqual(len(self.visualizer.df), 100)
    
    def test_create_distribution_plots(self):
        """分布プロットのテスト"""
        try:
            plots = self.visualizer.create_distribution_plots()
            self.assertIsInstance(plots, list)
            self.assertGreater(len(plots), 0)
        except Exception as e:
            self.fail(f"分布プロット作成でエラーが発生: {e}")
    
    def test_create_correlation_heatmap(self):
        """相関ヒートマップのテスト"""
        try:
            heatmap = self.visualizer.create_correlation_heatmap()
            self.assertIsNotNone(heatmap)
        except Exception as e:
            self.fail(f"相関ヒートマップ作成でエラーが発生: {e}")
    
    def test_create_categorical_plots(self):
        """カテゴリカルプロットのテスト"""
        try:
            plots = self.visualizer.create_categorical_plots()
            self.assertIsInstance(plots, list)
            self.assertGreater(len(plots), 0)
        except Exception as e:
            self.fail(f"カテゴリカルプロット作成でエラーが発生: {e}")
    
    def test_create_time_series_plots(self):
        """時系列プロットのテスト"""
        try:
            plots = self.visualizer.create_time_series_plots()
            self.assertIsInstance(plots, list)
            self.assertGreater(len(plots), 0)
        except Exception as e:
            self.fail(f"時系列プロット作成でエラーが発生: {e}")
    
    def test_create_outlier_plots(self):
        """外れ値プロットのテスト"""
        try:
            plots = self.visualizer.create_outlier_plots()
            self.assertIsInstance(plots, list)
            self.assertGreater(len(plots), 0)
        except Exception as e:
            self.fail(f"外れ値プロット作成でエラーが発生: {e}")
    
    def test_create_advanced_plots(self):
        """高度プロットのテスト"""
        try:
            plots = self.visualizer.create_advanced_plots()
            self.assertIsInstance(plots, list)
            self.assertGreater(len(plots), 0)
        except Exception as e:
            self.fail(f"高度プロット作成でエラーが発生: {e}")
    
    def test_create_executive_dashboard(self):
        """エグゼクティブダッシュボードのテスト"""
        try:
            dashboard = self.visualizer.create_executive_dashboard()
            self.assertIsNotNone(dashboard)
        except Exception as e:
            self.fail(f"エグゼクティブダッシュボード作成でエラーが発生: {e}")

if __name__ == '__main__':
    unittest.main()
