"""
データ可視化モジュール
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any
from .config import Config
import warnings
warnings.filterwarnings('ignore')

class DataVisualizer:
    """データ可視化クラス"""
    
    def __init__(self, df: pd.DataFrame):
        """
        初期化
        
        Args:
            df: 可視化対象のDataFrame
        """
        self.df = df
        self.setup_plotting_style()
    
    def setup_plotting_style(self):
        """プロットスタイルを設定"""
        plt.rcParams['font.family'] = 'DejaVu Sans'
        sns.set_style(Config.PLOT_STYLE)
        sns.set_palette(Config.PLOT_PALETTE)
    
    def create_correlation_heatmap(self, output_path: str = 'correlation_matrix.png') -> bool:
        """
        相関行列ヒートマップを作成
        
        Args:
            output_path: 出力ファイルパス
            
        Returns:
            作成成功フラグ
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return False
        
        try:
            plt.figure(figsize=(12, 10))
            correlation_matrix = self.df[numeric_cols].corr()
            
            # マスクを作成（上三角を非表示）
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            
            sns.heatmap(
                correlation_matrix,
                mask=mask,
                annot=True,
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": .5}
            )
            
            plt.title('変数間の相関行列', fontsize=16, pad=20)
            plt.tight_layout()
            plt.savefig(output_path, dpi=Config.PLOT_DPI, bbox_inches='tight')
            plt.close()
            
            return True
        except Exception as e:
            print(f"相関行列作成エラー: {e}")
            return False
    
    def create_distribution_plots(self, output_path: str = 'distributions.png') -> bool:
        """
        分布図を作成
        
        Args:
            output_path: 出力ファイルパス
            
        Returns:
            作成成功フラグ
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return False
        
        try:
            # 列数に応じてレイアウトを調整
            n_cols = min(len(numeric_cols), 4)
            n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
            if n_rows == 1 and n_cols == 1:
                axes = [axes]
            elif n_rows == 1 or n_cols == 1:
                axes = axes.flatten()
            else:
                axes = axes.flatten()
            
            for i, col in enumerate(numeric_cols):
                if i < len(axes):
                    # ヒストグラムと密度曲線
                    self.df[col].hist(bins=30, ax=axes[i], alpha=0.7, density=True)
                    self.df[col].plot.density(ax=axes[i], color='red')
                    
                    axes[i].set_title(f'{col}の分布', fontsize=12)
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('密度')
                    axes[i].grid(True, alpha=0.3)
            
            # 余った軸を非表示
            for i in range(len(numeric_cols), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=Config.PLOT_DPI, bbox_inches='tight')
            plt.close()
            
            return True
        except Exception as e:
            print(f"分布図作成エラー: {e}")
            return False
    
    def create_interactive_scatter(self, x_col: str, y_col: str, 
                                 color_col: Optional[str] = None,
                                 output_path: str = 'scatter_plot.html') -> bool:
        """
        インタラクティブ散布図を作成
        
        Args:
            x_col: X軸の列名
            y_col: Y軸の列名
            color_col: 色分けする列名（オプション）
            output_path: 出力ファイルパス
            
        Returns:
            作成成功フラグ
        """
        try:
            if color_col and color_col in self.df.columns:
                fig = px.scatter(
                    self.df, 
                    x=x_col, 
                    y=y_col, 
                    color=color_col,
                    title=f'{x_col} vs {y_col}（{color_col}で色分け）',
                    hover_data=self.df.columns.tolist()
                )
            else:
                fig = px.scatter(
                    self.df, 
                    x=x_col, 
                    y=y_col,
                    title=f'{x_col} vs {y_col}',
                    hover_data=self.df.columns.tolist()
                )
            
            fig.update_layout(
                title_font_size=16,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                template='plotly_white'
            )
            
            fig.write_html(output_path)
            return True
        except Exception as e:
            print(f"散布図作成エラー: {e}")
            return False
    
    def create_category_bar_chart(self, category_col: str, 
                                output_path: str = 'bar_chart.html') -> bool:
        """
        カテゴリ別棒グラフを作成
        
        Args:
            category_col: カテゴリ列名
            output_path: 出力ファイルパス
            
        Returns:
            作成成功フラグ
        """
        try:
            value_counts = self.df[category_col].value_counts()
            
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f'{category_col}の分布',
                labels={'x': category_col, 'y': '件数'}
            )
            
            fig.update_layout(
                title_font_size=16,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                template='plotly_white'
            )
            
            fig.write_html(output_path)
            return True
        except Exception as e:
            print(f"棒グラフ作成エラー: {e}")
            return False
    
    def create_line_chart(self, y_col: str, x_col: Optional[str] = None,
                         output_path: str = 'line_chart.html') -> bool:
        """
        線グラフを作成
        
        Args:
            y_col: Y軸の列名
            x_col: X軸の列名（オプション、指定しない場合はインデックス）
            output_path: 出力ファイルパス
            
        Returns:
            作成成功フラグ
        """
        try:
            if x_col and x_col in self.df.columns:
                fig = px.line(
                    self.df,
                    x=x_col,
                    y=y_col,
                    title=f'{y_col}の推移（{x_col}軸）'
                )
            else:
                fig = px.line(
                    self.df,
                    y=y_col,
                    title=f'{y_col}の推移'
                )
            
            fig.update_layout(
                title_font_size=16,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                template='plotly_white'
            )
            
            fig.write_html(output_path)
            return True
        except Exception as e:
            print(f"線グラフ作成エラー: {e}")
            return False
    
    def create_comprehensive_dashboard(self, output_path: str = 'ai_recommended_charts.html') -> bool:
        """
        包括的なダッシュボードを作成
        
        Args:
            output_path: 出力ファイルパス
            
        Returns:
            作成成功フラグ
        """
        try:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
            
            # サブプロットを作成
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    '主要指標の分布',
                    '相関分析（散布図）',
                    'カテゴリ分析',
                    'トレンド分析'
                ),
                specs=[
                    [{"secondary_y": False}, {"secondary_y": False}],
                    [{"secondary_y": False}, {"secondary_y": False}]
                ]
            )
            
            # 1. 主要指標のヒストグラム
            if len(numeric_cols) > 0:
                fig.add_trace(
                    go.Histogram(
                        x=self.df[numeric_cols[0]],
                        name=numeric_cols[0],
                        showlegend=False
                    ),
                    row=1, col=1
                )
            
            # 2. 散布図（相関分析）
            if len(numeric_cols) >= 2:
                fig.add_trace(
                    go.Scatter(
                        x=self.df[numeric_cols[0]],
                        y=self.df[numeric_cols[1]],
                        mode='markers',
                        name=f'{numeric_cols[0]} vs {numeric_cols[1]}',
                        showlegend=False
                    ),
                    row=1, col=2
                )
            
            # 3. カテゴリ分析
            if len(categorical_cols) > 0:
                value_counts = self.df[categorical_cols[0]].value_counts()
                fig.add_trace(
                    go.Bar(
                        x=value_counts.index,
                        y=value_counts.values,
                        name=categorical_cols[0],
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            # 4. トレンド分析
            if len(numeric_cols) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(self.df))),
                        y=self.df[numeric_cols[0]],
                        mode='lines',
                        name=f'{numeric_cols[0]}トレンド',
                        showlegend=False
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                height=800,
                title_text="AIが推奨するデータ可視化ダッシュボード",
                title_font_size=18,
                template='plotly_white'
            )
            
            fig.write_html(output_path)
            return True
        except Exception as e:
            print(f"ダッシュボード作成エラー: {e}")
            return False
    
    def create_visualizations(self, chart_type: str = 'auto', 
                            columns: Optional[List[str]] = None) -> Dict[str, str]:
        """
        可視化を作成
        
        Args:
            chart_type: グラフタイプ（'scatter', 'bar', 'line', 'auto'）
            columns: 使用する列名のリスト
            
        Returns:
            作成されたファイルパスの辞書
        """
        visualizations = {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        # 基本的な統計グラフ
        if len(numeric_cols) > 1:
            if self.create_correlation_heatmap():
                visualizations['correlation'] = 'correlation_matrix.png'
        
        if len(numeric_cols) > 0:
            if self.create_distribution_plots():
                visualizations['distributions'] = 'distributions.png'
        
        # 指定されたグラフタイプに応じて作成
        if chart_type == 'scatter' and len(numeric_cols) >= 2:
            if self.create_interactive_scatter(numeric_cols[0], numeric_cols[1]):
                visualizations['scatter'] = 'scatter_plot.html'
        
        elif chart_type == 'bar' and len(categorical_cols) > 0:
            if self.create_category_bar_chart(categorical_cols[0]):
                visualizations['bar'] = 'bar_chart.html'
        
        elif chart_type == 'line' and len(numeric_cols) > 0:
            if self.create_line_chart(numeric_cols[0]):
                visualizations['line'] = 'line_chart.html'
        
        # 自動またはダッシュボード作成
        if chart_type in ['auto', 'dashboard']:
            if self.create_comprehensive_dashboard():
                visualizations['dashboard'] = 'ai_recommended_charts.html'
        
        return visualizations
