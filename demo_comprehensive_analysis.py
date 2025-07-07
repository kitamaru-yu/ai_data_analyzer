"""
包括的企業データ分析のサンプルスクリプト
このスクリプトは新しい豊富なテストデータを使用してシステムの全機能をデモンストレーションします
"""

import pandas as pd
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.data_analyzer import DataAnalyzer
from src.core.visualizer import DataVisualizer
from src.core.ai_analyzer import AIAnalyzer
from src.core.config import Config

def load_comprehensive_data():
    """包括的なテストデータを読み込み"""
    print("🔄 包括的企業データを読み込み中...")
    
    # メインの企業データ
    main_data = pd.read_csv('data/comprehensive_business_data.csv')
    print(f"✓ メインデータ: {main_data.shape[0]}社, {main_data.shape[1]}指標")
    
    # 時系列データ
    time_series = pd.read_csv('data/time_series_data.csv')
    print(f"✓ 時系列データ: {time_series.shape[0]}レコード")
    
    # 部門別データ
    dept_data = pd.read_csv('data/department_analysis.csv')
    print(f"✓ 部門データ: {dept_data.shape[0]}部門")
    
    # 顧客データ
    customer_data = pd.read_csv('data/customer_data.csv')
    print(f"✓ 顧客データ: {customer_data.shape[0]}顧客")
    
    # 市場分析コンテキスト
    with open('data/market_analysis_context.txt', 'r', encoding='utf-8') as f:
        market_context = f.read()
    
    return main_data, time_series, dept_data, customer_data, market_context

def analyze_comprehensive_data():
    """包括的なデータ分析を実行"""
    print("\n🚀 === 包括的企業データ分析システム デモンストレーション ===\n")
    
    # データ読み込み
    main_data, time_series, dept_data, customer_data, market_context = load_comprehensive_data()
    
    print("\n📊 === 1. メイン企業データ分析 ===")
    
    # メインデータの分析
    analyzer = DataAnalyzer(main_data, market_context)
    
    # 基本構造分析
    print("\n🔍 データ構造分析中...")
    structure = analyzer.analyze_data_structure()
    print(f"✓ 分析対象: {structure['basic_info']['shape'][0]}社")
    print(f"✓ 分析指標: {structure['basic_info']['shape'][1]}項目")
    print(f"✓ 業界数: {main_data['Industry'].nunique()}")
    print(f"✓ 地域数: {main_data['Region'].nunique()}")
    
    # 相関分析
    print("\n🔗 相関関係分析中...")
    correlation = analyzer.get_correlation_analysis()
    strong_corr = correlation.get('strong_correlations', [])
    print(f"✓ 強い相関関係: {len(strong_corr)}組")
    for corr in strong_corr[:3]:  # 上位3件表示
        print(f"  - {corr['variable1']} ↔ {corr['variable2']}: {corr['correlation']:.3f}")
    
    # 異常値検出
    print("\n⚠️  異常値検出中...")
    outliers = analyzer.detect_outliers()
    print(f"✓ 異常値検出対象列: {len(outliers)}")
    for col, info in list(outliers.items())[:3]:  # 上位3件表示
        print(f"  - {col}: {info['count']}件 ({info['percentage']:.1f}%)")
    
    print("\n📈 === 2. 可視化生成 ===")
    
    # 可視化作成
    visualizer = DataVisualizer(main_data)
    
    print("\n🎨 包括的ダッシュボード作成中...")
    dashboard_success = visualizer.create_comprehensive_dashboard('demo_dashboard.html')
    if dashboard_success:
        print("✓ ダッシュボード作成完了: demo_dashboard.html")
    
    print("\n📊 相関ヒートマップ作成中...")
    heatmap_success = visualizer.create_correlation_heatmap('demo_correlation.png')
    if heatmap_success:
        print("✓ 相関ヒートマップ作成完了: demo_correlation.png")
    
    print("\n📈 分布図作成中...")
    dist_success = visualizer.create_distribution_plots('demo_distributions.png')
    if dist_success:
        print("✓ 分布図作成完了: demo_distributions.png")
    
    print("\n🎯 === 3. 時系列データ分析 ===")
    
    # 時系列分析
    ts_analyzer = DataAnalyzer(time_series)
    ts_structure = ts_analyzer.analyze_data_structure()
    print(f"✓ 時系列データ期間: {time_series['Date'].min()} ～ {time_series['Date'].max()}")
    print(f"✓ 追跡企業数: {time_series['Company'].nunique()}")
    
    # 時系列可視化
    ts_visualizer = DataVisualizer(time_series)
    scatter_success = ts_visualizer.create_interactive_scatter('Revenue', 'Growth_Rate', 'Company', 'demo_growth_analysis.html')
    if scatter_success:
        print("✓ 成長率分析作成完了: demo_growth_analysis.html")
    
    print("\n🏢 === 4. 部門別分析 ===")
    
    # 部門分析
    dept_analyzer = DataAnalyzer(dept_data)
    dept_structure = dept_analyzer.analyze_data_structure()
    print(f"✓ 分析部門数: {dept_data.shape[0]}")
    
    # 高ROI部門の特定
    high_roi_depts = dept_data[dept_data['ROI_Percentage'] > 15]
    print(f"✓ 高ROI部門（15%以上）: {len(high_roi_depts)}部門")
    for _, dept in high_roi_depts.iterrows():
        print(f"  - {dept['Department']}: ROI {dept['ROI_Percentage']:.1f}%")
    
    print("\n👥 === 5. 顧客データ分析 ===")
    
    # 顧客分析
    customer_analyzer = DataAnalyzer(customer_data)
    customer_structure = customer_analyzer.analyze_data_structure()
    print(f"✓ 顧客データ数: {customer_data.shape[0]}")
    print(f"✓ 平均満足度: {customer_data['Satisfaction_Score'].mean():.2f}")
    print(f"✓ 平均ロイヤリティ: {customer_data['Loyalty_Score'].mean():.2f}")
    
    # チャネル別分析
    channel_analysis = customer_data.groupby('Channel')['Purchase_Amount'].agg(['count', 'mean', 'sum'])
    print(f"✓ 最効果的チャネル: {channel_analysis['sum'].idxmax()}")
    
    print("\n🤖 === 6. AI分析実行 ===")
    
    # AI分析（API Keyが設定されている場合のみ）
    if Config.OPENAI_API_KEY:
        print("\n🧠 AI分析を実行中...")
        try:
            ai_analyzer = AIAnalyzer()
            
            # データサンプルを文字列として準備
            data_sample = main_data.head(5).to_string()
            
            # AI分析実行
            ai_insights = ai_analyzer.analyze_data_with_ai(
                structure, 
                data_sample, 
                market_context[:1000]  # コンテキストを制限
            )
            
            if ai_insights:
                print("✓ AI分析完了")
                print("\n🎯 主要洞察（AI生成）:")
                print(ai_insights[:500] + "..." if len(ai_insights) > 500 else ai_insights)
            else:
                print("⚠️ AI分析でエラーが発生しました")
                
        except Exception as e:
            print(f"⚠️ AI分析エラー: {e}")
    else:
        print("⚠️ OpenAI API Keyが設定されていないため、AI分析をスキップします")
        print("   .envファイルでOPENAI_API_KEYを設定してください")
    
    print("\n🎉 === 分析完了 ===")
    print("\n📂 生成されたファイル:")
    print("  - demo_dashboard.html (包括的ダッシュボード)")
    print("  - demo_correlation.png (相関ヒートマップ)")
    print("  - demo_distributions.png (分布図)")
    print("  - demo_growth_analysis.html (成長率分析)")
    
    print("\n💡 システムの強力な機能:")
    print("  ✓ 25指標 × 40社の包括的企業データ分析")
    print("  ✓ 時系列トレンド分析")
    print("  ✓ 相関関係の自動検出")
    print("  ✓ 異常値の智能的発見")
    print("  ✓ インタラクティブな可視化")
    print("  ✓ 部門別・顧客別の詳細分析")
    print("  ✓ AI駆動のビジネス洞察")
    
    print("\n🚀 Streamlit UIで更なる分析を実行:")
    print("   📊 START_WEB.bat を実行してWebアプリを起動")

if __name__ == "__main__":
    analyze_comprehensive_data()
