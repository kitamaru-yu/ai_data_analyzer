"""
データ分析機能モジュール
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, Optional
from config import Config

class DataAnalyzer:
    """データ分析クラス"""
    
    def __init__(self, df: pd.DataFrame, text_data: Optional[str] = None):
        """
        初期化
        
        Args:
            df: 分析対象のDataFrame
            text_data: 追加のテキストデータ
        """
        self.df = df
        self.text_data = text_data
        self.analysis_results = {}
    
    def analyze_data_structure(self) -> Dict[str, Any]:
        """
        データの構造を分析
        
        Returns:
            分析結果辞書
        """
        if self.df is None:
            return {}
        
        analysis = {
            'basic_info': {
                'shape': self.df.shape,
                'columns': list(self.df.columns),
                'data_types': self.df.dtypes.to_dict(),
                'missing_values': self.df.isnull().sum().to_dict(),
                'duplicate_rows': self.df.duplicated().sum()
            },
            'numeric_summary': {},
            'categorical_summary': {}
        }
        
        # 数値データの統計情報
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            analysis['numeric_summary'] = self.df[numeric_cols].describe().to_dict()
        
        # カテゴリデータの統計情報
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            analysis['categorical_summary'][col] = {
                'unique_values': self.df[col].nunique(),
                'top_values': self.df[col].value_counts().head(5).to_dict()
            }
        
        self.analysis_results['data_structure'] = analysis
        return analysis
    
    def get_correlation_analysis(self) -> Dict[str, Any]:
        """
        相関分析を実行
        
        Returns:
            相関分析結果
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return {}
        
        correlation_matrix = self.df[numeric_cols].corr()
        
        # 強い相関関係を特定
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # 強い相関の閾値
                    strong_correlations.append({
                        'variable1': correlation_matrix.columns[i],
                        'variable2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }
    
    def detect_outliers(self) -> Dict[str, Any]:
        """
        異常値を検出
        
        Returns:
            異常値検出結果
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            # IQR法による異常値検出
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float(outlier_count / len(self.df) * 100),
                    'bounds': {
                        'lower': float(lower_bound),
                        'upper': float(upper_bound)
                    }
                }
        
        return outliers
    
    def generate_data_summary(self) -> str:
        """
        データサマリーを生成
        
        Returns:
            データサマリー文字列
        """
        structure = self.analyze_data_structure()
        correlation = self.get_correlation_analysis()
        outliers = self.detect_outliers()
        
        summary = f"""
データ分析サマリー
==================

基本情報:
- 行数: {structure['basic_info']['shape'][0]}
- 列数: {structure['basic_info']['shape'][1]}
- 重複行数: {structure['basic_info']['duplicate_rows']}

データ品質:
- 欠損値のある列: {len([k for k, v in structure['basic_info']['missing_values'].items() if v > 0])}
- 異常値のある列: {len(outliers)}

相関分析:
- 強い相関関係: {len(correlation.get('strong_correlations', []))}件
"""
        
        # 強い相関関係の詳細
        if correlation.get('strong_correlations'):
            summary += "\n強い相関関係:\n"
            for corr in correlation['strong_correlations']:
                summary += f"- {corr['variable1']} vs {corr['variable2']}: {corr['correlation']:.3f}\n"
        
        # 異常値の詳細
        if outliers:
            summary += "\n異常値の詳細:\n"
            for col, info in outliers.items():
                summary += f"- {col}: {info['count']}件 ({info['percentage']:.1f}%)\n"
        
        return summary
    
    def get_business_insights(self) -> Dict[str, Any]:
        """
        ビジネス観点からの洞察を生成
        
        Returns:
            ビジネス洞察辞書
        """
        insights = {
            'data_quality_issues': [],
            'key_patterns': [],
            'business_opportunities': [],
            'risk_factors': []
        }
        
        # データ品質の問題
        structure = self.analyze_data_structure()
        missing_values = structure['basic_info']['missing_values']
        for col, count in missing_values.items():
            if count > 0:
                percentage = (count / self.df.shape[0]) * 100
                if percentage > 10:  # 10%以上の欠損値
                    insights['data_quality_issues'].append({
                        'column': col,
                        'issue': f'欠損値が{percentage:.1f}%存在',
                        'impact': 'high' if percentage > 30 else 'medium'
                    })
        
        # 主要パターンの特定
        correlation = self.get_correlation_analysis()
        for corr in correlation.get('strong_correlations', []):
            insights['key_patterns'].append({
                'pattern': f'{corr["variable1"]}と{corr["variable2"]}の強い相関',
                'strength': abs(corr['correlation']),
                'type': 'positive' if corr['correlation'] > 0 else 'negative'
            })
        
        return insights
