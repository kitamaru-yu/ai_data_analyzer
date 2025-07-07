import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import tempfile
import os

# 自作モジュールのインポート
import sys
import os

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from main import BusinessDataAnalyzer
from src.core.config import Config

# Streamlitページの設定
st.set_page_config(
    page_title="企業データ分析システム",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .status-warning {
        background: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

def main():
    # メインヘッダー
    st.markdown("""
    <div class="main-header">
        <h1>🏢 企業データ分析・可視化・戦略提案システム</h1>
        <p>AI を活用した高度なデータ分析と戦略提案</p>
    </div>
    """, unsafe_allow_html=True)
    
    # サイドバーでの設定
    st.sidebar.header("📝 システム設定")
    
    # モデル選択セクション
    st.sidebar.subheader("🤖 モデル選択")
    
    # 推奨モデルの表示
    use_case = st.sidebar.selectbox(
        "用途を選択",
        ["balanced", "high_quality", "cost_effective", "high_speed"],
        format_func=lambda x: {
            "balanced": "バランス重視",
            "high_quality": "高品質",
            "cost_effective": "コスト重視",
            "high_speed": "高速"
        }[x]
    )
    
    recommended_models = Config.get_model_recommendations(use_case)
    st.sidebar.info(f"推奨モデル: {', '.join(recommended_models[:3])}")
    
    # 分析モデルの選択
    selected_analysis_model = st.sidebar.selectbox(
        "分析用モデル",
        Config.AVAILABLE_MODELS,
        index=Config.AVAILABLE_MODELS.index(Config.ANALYSIS_MODEL) if Config.ANALYSIS_MODEL in Config.AVAILABLE_MODELS else 0
    )
    
    # 戦略モデルの選択
    selected_strategy_model = st.sidebar.selectbox(
        "戦略用モデル",
        Config.AVAILABLE_MODELS,
        index=Config.AVAILABLE_MODELS.index(Config.STRATEGY_MODEL) if Config.STRATEGY_MODEL in Config.AVAILABLE_MODELS else 0
    )
    
    # 処理モデルの選択
    selected_processing_model = st.sidebar.selectbox(
        "処理用モデル",
        Config.AVAILABLE_MODELS,
        index=Config.AVAILABLE_MODELS.index(Config.PROCESSING_MODEL) if Config.PROCESSING_MODEL in Config.AVAILABLE_MODELS else 0
    )
    
    # モデル設定の適用
    if st.sidebar.button("🔄 モデル設定を適用"):
        Config.set_model('analysis', selected_analysis_model)
        Config.set_model('strategy', selected_strategy_model)
        Config.set_model('processing', selected_processing_model)
        st.sidebar.success("✅ モデル設定を更新しました")
        st.rerun()
    
    # 現在の設定を表示
    st.sidebar.subheader("現在の設定")
    st.sidebar.text(f"分析モデル: {Config.ANALYSIS_MODEL}")
    st.sidebar.text(f"戦略モデル: {Config.STRATEGY_MODEL}")
    st.sidebar.text(f"処理モデル: {Config.PROCESSING_MODEL}")
    
    # OpenAI API Keyの入力
    st.sidebar.header("🔑 API設定")
    
    if Config.OPENAI_API_KEY:
        st.sidebar.markdown('<div class="status-success">✅ API Key: 環境変数から設定済み</div>', unsafe_allow_html=True)
        api_key = Config.OPENAI_API_KEY
    else:
        st.sidebar.markdown('<div class="status-warning">⚠️ API Keyを入力してください</div>', unsafe_allow_html=True)
        api_key = st.sidebar.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    if api_key:
        try:
            if st.session_state.analyzer is None:
                st.session_state.analyzer = BusinessDataAnalyzer(api_key=api_key)
            st.sidebar.markdown('<div class="status-success">✅ API Key設定完了</div>', unsafe_allow_html=True)
        except Exception as e:
            st.sidebar.markdown(f'<div class="status-error">❌ API Key設定エラー: {e}</div>', unsafe_allow_html=True)
            return
    else:
        st.sidebar.markdown('<div class="status-warning">⚠️ 分析を開始するにはAPI Keyが必要です</div>', unsafe_allow_html=True)
        
        # API Key取得方法の案内
        with st.sidebar.expander("📖 API Key取得方法"):
            st.markdown("""
            1. [OpenAI Platform](https://platform.openai.com/)にアクセス
            2. アカウントを作成/ログイン
            3. API Keys セクションで新しいキーを作成
            4. 作成されたキーをコピーして上記に貼り付け
            """)
        return
    
    # データアップロード
    st.sidebar.header("📂 データアップロード")
    uploaded_csv = st.sidebar.file_uploader("CSVファイルをアップロード", type=['csv'])
    uploaded_text = st.sidebar.file_uploader("テキストファイルをアップロード（オプション）", type=['txt'])
    
    if uploaded_csv is not None:
        # CSVファイルの読み込み
        st.session_state.df = pd.read_csv(uploaded_csv)
        
        # 一時ファイルとして保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            st.session_state.df.to_csv(tmp.name, index=False)
            csv_path = tmp.name
        
        # アナライザーにデータを読み込み
        st.session_state.analyzer.read_csv(csv_path)
        
        # テキストファイルの処理
        if uploaded_text is not None:
            text_content = uploaded_text.read().decode('utf-8')
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp.write(text_content)
                text_path = tmp.name
            st.session_state.analyzer.read_text_file(text_path)
        
        # メインコンテンツ
        if st.session_state.df is not None:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.header("📊 データ概要")
                st.dataframe(st.session_state.df.head(10))
                
                # 基本統計情報
                st.subheader("📈 基本統計")
                col_stats1, col_stats2 = st.columns(2)
                
                with col_stats1:
                    st.metric("データ行数", st.session_state.df.shape[0])
                    st.metric("データ列数", st.session_state.df.shape[1])
                
                with col_stats2:
                    st.metric("数値列数", len(st.session_state.df.select_dtypes(include=[np.number]).columns))
                    st.metric("カテゴリ列数", len(st.session_state.df.select_dtypes(include=['object']).columns))
            
            with col2:
                st.header("🔍 分析オプション")
                
                # データ構造分析
                if st.button("🔍 データ構造分析"):
                    with st.spinner("分析中..."):
                        structure = st.session_state.analyzer.analyze_data_structure()
                        st.session_state.structure_analysis = structure
                        st.success("✅ データ構造分析完了")
                
                # AI分析
                if st.button("🤖 AI詳細分析"):
                    with st.spinner("AI分析中..."):
                        ai_analysis = st.session_state.analyzer.ai_analyze_data()
                        st.session_state.ai_analysis = ai_analysis
                        st.success("✅ AI分析完了")
                
                # ビジネス戦略提案
                if st.button("💡 ビジネス戦略提案"):
                    with st.spinner("戦略提案中..."):
                        strategy = st.session_state.analyzer.generate_business_strategy()
                        st.session_state.strategy = strategy
                        st.success("✅ 戦略提案完了")
        else:
            # データがない場合のウェルカムメッセージ
            st.markdown("### 📥 データをアップロードして開始してください")
    
    # データがアップロードされていない場合のウェルカムメッセージ
    if st.session_state.df is None:
        # ウェルカムメッセージ
        st.markdown("""
        ## 👋 企業データ分析システムへようこそ！
        
        このシステムは、AI を活用して企業データを分析し、戦略的な洞察を提供します。
        
        ### 🚀 主な機能:
        
        #### 📊 データ分析
        - **基本統計分析**: データの概要、分布、傾向を把握
        - **相関分析**: 変数間の関係性を発見
        - **時系列分析**: 時間的な変化とトレンドを分析
        - **外れ値検出**: 異常値や特異なパターンを特定
        
        #### 🎨 データ可視化
        - **インタラクティブグラフ**: Plotlyを使用した高度な可視化
        - **統計チャート**: 分布図、散布図、相関マップ
        - **ダッシュボード**: エグゼクティブ向け総合ダッシュボード
        
        #### 🤖 AI 戦略提案
        - **データ洞察**: AIによる自動的な洞察抽出
        - **戦略提案**: ビジネス改善のための具体的な提案
        - **次のアクション**: 実行可能な行動計画
        
        ### 📝 使い方:
        1. **左側のサイドバーでAI モデルを選択**
        2. **CSVファイルをアップロード**
        3. **分析を実行**
        4. **結果を確認・ダウンロード**
        
        ### 🔧 現在の設定:
        """)
        
        # システム状態の表示
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🤖 AI モデル</h4>
                <p><strong>分析:</strong> {}</p>
                <p><strong>戦略:</strong> {}</p>
                <p><strong>処理:</strong> {}</p>
            </div>
            """.format(Config.ANALYSIS_MODEL, Config.STRATEGY_MODEL, Config.PROCESSING_MODEL), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 利用可能機能</h4>
                <p>✅ データ分析</p>
                <p>✅ 可視化</p>
                <p>✅ AI 戦略提案</p>
                <p>✅ レポート生成</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🔧 システム情報</h4>
                <p><strong>対応形式:</strong> CSV, TXT</p>
                <p><strong>利用可能モデル:</strong> {}</p>
                <p><strong>最大トークン:</strong> 2500</p>
            </div>
            """.format(len(Config.AVAILABLE_MODELS)), unsafe_allow_html=True)
        
        # サンプルデータの提供
        st.markdown("---")
        st.subheader("🎯 サンプルデータで試してみる")
        
        sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=12, freq='M'),
            'sales': [15000, 18000, 22000, 19000, 25000, 28000, 32000, 29000, 35000, 38000, 41000, 45000],
            'profit': [1500, 1800, 2200, 1900, 2500, 2800, 3200, 2900, 3500, 3800, 4100, 4500],
            'customers': [150, 180, 220, 190, 250, 280, 320, 290, 350, 380, 410, 450],
            'region': ['East', 'West', 'North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North', 'South']
        })
        
        if st.button("📝 サンプルデータをダウンロード"):
            csv = sample_data.to_csv(index=False)
            st.download_button(
                label="💾 sample_business_data.csv",
                data=csv,
                file_name='sample_business_data.csv',
                mime='text/csv'
            )
        
        with st.expander("👀 サンプルデータを確認"):
            st.dataframe(sample_data)
        
        # 可視化セクション
        st.header("📊 データ可視化")
        
        # データフレームの存在チェック
        if st.session_state.df is None:
            st.warning("📥 まずデータをアップロードしてください")
            return
            
        viz_tabs = st.tabs(["相関分析", "分布分析", "カテゴリ分析", "トレンド分析"])
        
        numeric_cols = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = st.session_state.df.select_dtypes(include=['object']).columns.tolist()
        
        with viz_tabs[0]:
            if len(numeric_cols) > 1:
                st.subheader("🔗 相関行列")
                corr_matrix = st.session_state.df[numeric_cols].corr()
                fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                               title="データの相関関係")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("相関分析には2つ以上の数値列が必要です")
        
        with viz_tabs[1]:
            if len(numeric_cols) > 0:
                st.subheader("📊 分布分析")
                selected_col = st.selectbox("分析する列を選択", numeric_cols)
                
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    fig_hist = px.histogram(st.session_state.df, x=selected_col, 
                                          title=f"{selected_col}の分布")
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col_viz2:
                    fig_box = px.box(st.session_state.df, y=selected_col, 
                                    title=f"{selected_col}の箱ひげ図")
                    st.plotly_chart(fig_box, use_container_width=True)
        
        with viz_tabs[2]:
            if len(categorical_cols) > 0:
                st.subheader("🏷️ カテゴリ分析")
                selected_cat = st.selectbox("分析するカテゴリを選択", categorical_cols)
                
                value_counts = st.session_state.df[selected_cat].value_counts()
                fig_bar = px.bar(x=value_counts.index, y=value_counts.values,
                               title=f"{selected_cat}の分布")
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with viz_tabs[3]:
            if len(numeric_cols) > 0:
                st.subheader("📈 トレンド分析")
                selected_trend = st.selectbox("トレンド分析する列を選択", numeric_cols)
                
                fig_line = px.line(st.session_state.df, y=selected_trend,
                                 title=f"{selected_trend}の推移")
                st.plotly_chart(fig_line, use_container_width=True)
        
        # 散布図分析
        if len(numeric_cols) >= 2:
            st.header("🎯 散布図分析")
            col_scatter1, col_scatter2 = st.columns(2)
            
            with col_scatter1:
                x_axis = st.selectbox("X軸", numeric_cols, key="x_axis")
            with col_scatter2:
                y_axis = st.selectbox("Y軸", numeric_cols, key="y_axis")
            
            if len(categorical_cols) > 0:
                color_by = st.selectbox("色分け（オプション）", ['なし'] + categorical_cols)
                if color_by != 'なし':
                    fig_scatter = px.scatter(st.session_state.df, x=x_axis, y=y_axis, 
                                           color=color_by, title=f"{x_axis} vs {y_axis}")
                else:
                    fig_scatter = px.scatter(st.session_state.df, x=x_axis, y=y_axis,
                                           title=f"{x_axis} vs {y_axis}")
            else:
                fig_scatter = px.scatter(st.session_state.df, x=x_axis, y=y_axis,
                                       title=f"{x_axis} vs {y_axis}")
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 分析結果の表示
        st.header("📋 分析結果")
        result_tabs = st.tabs(["AI分析結果", "ビジネス戦略"])
        
        with result_tabs[0]:
            if hasattr(st.session_state, 'ai_analysis') and st.session_state.ai_analysis:
                st.markdown("### 🤖 AI分析結果")
                st.markdown(st.session_state.ai_analysis)
            else:
                st.info("AI分析を実行してください")
        
        with result_tabs[1]:
            if hasattr(st.session_state, 'strategy') and st.session_state.strategy:
                st.markdown("### 💡 ビジネス戦略提案")
                st.markdown(st.session_state.strategy)
            else:
                st.info("ビジネス戦略提案を実行してください")
        
        # データダウンロード
        st.header("💾 結果のダウンロード")
        
        if st.button("📊 分析レポート生成"):
            report_content = "# 企業データ分析レポート\n\n"
            
            if hasattr(st.session_state, 'ai_analysis'):
                report_content += "## AI分析結果\n"
                report_content += st.session_state.ai_analysis + "\n\n"
            
            if hasattr(st.session_state, 'strategy'):
                report_content += "## ビジネス戦略提案\n"
                report_content += st.session_state.strategy + "\n\n"
            
            st.download_button(
                label="📄 レポートダウンロード",
                data=report_content,
                file_name="analysis_report.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
