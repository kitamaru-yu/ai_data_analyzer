#!/usr/bin/env python3
"""
企業データ分析システム - 包括的機能デモ
全機能を活用したリアルなビジネス分析シナリオ
"""

import sys
import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# パスの設定
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config import Config
from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer
from src.core.ai_analyzer import AIAnalyzer

def main():
    print("🚀 企業データ分析システム - 包括的機能デモ")
    print("=" * 60)
    
    # 設定の確認
    config = Config()
    print(f"📋 使用モデル: {config.ANALYSIS_MODEL}")
    print(f"🔑 API Key設定: {'✅' if config.OPENAI_API_KEY else '❌'}")
    print()
    
    # 1. 基本データの読み込みと分析
    print("1️⃣ 基本企業データ分析")
    print("-" * 30)
    
    try:
        # 拡張データの読み込み
        df_enhanced = pd.read_csv('data/enhanced_business_data.csv')
        print(f"✅ 拡張データ読み込み完了: {len(df_enhanced)}社、{len(df_enhanced.columns)}指標")
        
        # 基本統計分析
        analyzer = DataAnalyzer(df_enhanced)
        basic_stats = analyzer.get_basic_stats()
        print(f"📊 基本統計分析完了 - {len(basic_stats['stats'])}項目")
        
        # 相関分析
        correlation = analyzer.get_correlation_analysis()
        print(f"🔗 相関分析完了 - {len(correlation['insights'])}項目の洞察")
        
        # カテゴリカル分析
        categorical = analyzer.get_categorical_analysis()
        print(f"📈 カテゴリ分析完了 - {len(categorical['insights'])}項目の分析")
        
    except Exception as e:
        print(f"❌ 基本分析エラー: {e}")
    
    print()
    
    # 2. 時系列データ分析
    print("2️⃣ 時系列パフォーマンス分析")
    print("-" * 30)
    
    try:
        # 月次パフォーマンスデータの読み込み
        df_monthly = pd.read_csv('data/monthly_performance_data.csv')
        df_monthly['Date'] = pd.to_datetime(df_monthly['Date'])
        print(f"✅ 時系列データ読み込み完了: {len(df_monthly)}レコード")
        
        # 時系列分析
        analyzer_ts = DataAnalyzer(df_monthly)
        time_series = analyzer_ts.get_time_series_analysis()
        print(f"📈 時系列分析完了 - トレンド・季節性・予測を分析")
        
        # 異常値検出
        outliers = analyzer_ts.detect_outliers()
        print(f"🎯 異常値検出完了 - {len(outliers['outlier_data'])}件の異常値を特定")
        
    except Exception as e:
        print(f"❌ 時系列分析エラー: {e}")
    
    print()
    
    # 3. 高度な可視化
    print("3️⃣ インタラクティブ可視化")
    print("-" * 30)
    
    try:
        # 可視化エンジンの初期化
        visualizer = DataVisualizer(df_enhanced)
        
        # 分布図の作成
        dist_success = visualizer.create_distribution_plots('enhanced_distributions.png')
        print(f"📊 分布図作成: {'✅' if dist_success else '❌'}")
        
        # 相関ヒートマップ
        corr_success = visualizer.create_correlation_heatmap('enhanced_correlation.png')
        print(f"🔥 相関ヒートマップ: {'✅' if corr_success else '❌'}")
        
        # インタラクティブ散布図（収益 vs 成長率）
        scatter_success = visualizer.create_interactive_scatter(
            'Revenue', 'Growth_Rate', 'Industry', 'revenue_vs_growth.html'
        )
        print(f"💫 散布図（収益vs成長率）: {'✅' if scatter_success else '❌'}")
        
        # カテゴリ分析（業界別）
        category_success = visualizer.create_category_bar_chart(
            'Industry', 'industry_distribution.html'
        )
        print(f"📊 業界分布図: {'✅' if category_success else '❌'}")
        
        # 包括的ダッシュボード
        dashboard_success = visualizer.create_comprehensive_dashboard(
            'comprehensive_dashboard.html'
        )
        print(f"🎛️ 統合ダッシュボード: {'✅' if dashboard_success else '❌'}")
        
    except Exception as e:
        print(f"❌ 可視化エラー: {e}")
    
    print()
    
    # 4. AI分析とビジネス洞察
    print("4️⃣ AI分析とビジネス戦略")
    print("-" * 30)
    
    try:
        # 市場コンテキストの読み込み
        with open('data/enhanced_market_context.txt', 'r', encoding='utf-8') as f:
            market_context = f.read()
        print(f"📖 市場コンテキスト読み込み完了: {len(market_context)}文字")
        
        # AI分析エンジンの初期化
        ai_analyzer = AIAnalyzer()
        
        # 統合分析結果の準備
        analysis_results = {
            'basic_stats': basic_stats,
            'correlation': correlation,
            'categorical': categorical,
            'time_series': time_series,
            'outliers': outliers,
            'data_summary': {
                'total_companies': len(df_enhanced),
                'industries': df_enhanced['Industry'].nunique(),
                'avg_revenue': df_enhanced['Revenue'].mean(),
                'avg_growth': df_enhanced['Growth_Rate'].mean(),
                'top_performers': df_enhanced.nlargest(5, 'Growth_Rate')['Company'].tolist()
            }
        }
        
        print("🤖 AI分析を実行中...")
        
        # データ洞察の生成
        if config.OPENAI_API_KEY:
            insights = ai_analyzer.analyze_data_insights(analysis_results)
            print(f"💡 AI洞察生成完了: {len(insights)}文字")
            
            # ビジネス戦略の生成
            strategy = ai_analyzer.generate_business_strategy(insights, market_context)
            print(f"🎯 戦略提案生成完了: {len(strategy)}文字")
            
            # 次のアクション提案
            actions = ai_analyzer.suggest_next_actions(strategy)
            print(f"⚡ アクション提案完了: {len(actions)}文字")
            
            # モデル情報の表示
            model_info = ai_analyzer.get_model_info()
            print(f"🔧 使用モデル: {model_info['model']}")
            
            # レポートの保存
            with open('comprehensive_analysis_report.txt', 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("企業データ分析システム - 包括的分析レポート\n")
                f.write("=" * 80 + "\n\n")
                f.write("📊 AI分析による洞察\n")
                f.write("-" * 40 + "\n")
                f.write(insights + "\n\n")
                f.write("🎯 戦略提案\n")
                f.write("-" * 40 + "\n")
                f.write(strategy + "\n\n")
                f.write("⚡ 推奨アクション\n")
                f.write("-" * 40 + "\n")
                f.write(actions + "\n\n")
                f.write(f"分析実行日時: {pd.Timestamp.now()}\n")
                f.write(f"使用モデル: {model_info['model']}\n")
            
            print("📋 包括的レポート保存完了: comprehensive_analysis_report.txt")
            
        else:
            print("⚠️ OpenAI API Keyが設定されていません。AI分析をスキップします。")
            
    except Exception as e:
        print(f"❌ AI分析エラー: {e}")
    
    print()
    
    # 5. パフォーマンス分析
    print("5️⃣ システムパフォーマンス分析")
    print("-" * 30)
    
    try:
        # データセット情報
        print(f"📈 処理データ量:")
        print(f"  - 基本データ: {len(df_enhanced):,}行 × {len(df_enhanced.columns)}列")
        print(f"  - 時系列データ: {len(df_monthly):,}行 × {len(df_monthly.columns)}列")
        print(f"  - 総データポイント: {len(df_enhanced) * len(df_enhanced.columns) + len(df_monthly) * len(df_monthly.columns):,}")
        
        # 業界カバレッジ
        industries = df_enhanced['Industry'].unique()
        print(f"🏭 業界カバレッジ: {len(industries)}業界")
        for industry in sorted(industries):
            count = len(df_enhanced[df_enhanced['Industry'] == industry])
            print(f"  - {industry}: {count}社")
        
        # 地域カバレッジ
        regions = df_enhanced['Region'].unique()
        print(f"🌍 地域カバレッジ: {len(regions)}地域")
        for region in sorted(regions):
            count = len(df_enhanced[df_enhanced['Region'] == region])
            percentage = (count / len(df_enhanced)) * 100
            print(f"  - {region}: {count}社 ({percentage:.1f}%)")
        
        # 指標カバレッジ
        numeric_cols = df_enhanced.select_dtypes(include=['number']).columns
        categorical_cols = df_enhanced.select_dtypes(include=['object']).columns
        print(f"📊 指標カバレッジ:")
        print(f"  - 数値指標: {len(numeric_cols)}項目")
        print(f"  - カテゴリ指標: {len(categorical_cols)}項目")
        
    except Exception as e:
        print(f"❌ パフォーマンス分析エラー: {e}")
    
    print()
    print("🎉 包括的機能デモ完了!")
    print("=" * 60)
    print("📁 生成されたファイル:")
    files_to_check = [
        'enhanced_distributions.png',
        'enhanced_correlation.png', 
        'revenue_vs_growth.html',
        'industry_distribution.html',
        'comprehensive_dashboard.html',
        'comprehensive_analysis_report.txt'
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    print("\n💡 次のステップ:")
    print("  1. HTMLファイルをブラウザで開いて可視化を確認")
    print("  2. comprehensive_analysis_report.txt でAI分析結果を確認")
    print("  3. Streamlit UI (📊 START_WEB.bat) で対話的分析を実行")
    print("  4. 独自のデータを data/ フォルダに追加してテスト")

if __name__ == "__main__":
    main()
