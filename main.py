"""
企業データ分析・可視化・戦略提案システム
メインモジュール
"""

import pandas as pd
import os
from typing import Optional, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# 自作モジュールのインポート
from config import Config
from data_analyzer import DataAnalyzer
from visualizer import DataVisualizer
from ai_analyzer import AIAnalyzer

class BusinessDataAnalyzer:
    """企業データ分析・可視化・戦略提案システム"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: OpenAI API キー
        """
        # 設定の妥当性チェック
        if not Config.validate_config():
            raise ValueError("設定に問題があります。.envファイルを確認してください。")
        
        # 各モジュールを初期化
        self.ai_analyzer = AIAnalyzer(api_key)
        self.data_analyzer = None
        self.visualizer = None
        
        # データ保存用
        self.df = None
        self.text_data = None
        self.analysis_results = {}
        
        # 設定を表示
        Config.display_config()
    
    def read_csv(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        企業データCSVファイルを読み込む
        
        Args:
            file_path: CSVファイルパス
            
        Returns:
            読み込んだDataFrame
        """
        try:
            self.df = pd.read_csv(file_path)
            print(f"CSVファイルを読み込みました: {file_path}")
            print(f"データの形状: {self.df.shape}")
            print(f"列名: {list(self.df.columns)}")
            print(f"データ型: {self.df.dtypes.to_dict()}")
            
            # 分析器と可視化器を初期化
            self.data_analyzer = DataAnalyzer(self.df, self.text_data)
            self.visualizer = DataVisualizer(self.df)
            
            return self.df
        except Exception as e:
            print(f"CSVファイルの読み込みエラー: {e}")
            return None
    
    def read_text_file(self, file_path: str) -> Optional[str]:
        """
        テキストファイルを読み込む
        
        Args:
            file_path: テキストファイルパス
            
        Returns:
            読み込んだテキストデータ
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_data = file.read()
            print(f"テキストファイルを読み込みました: {file_path}")
            print(f"文字数: {len(self.text_data)}")
            
            # データ分析器にテキストデータを設定
            if self.data_analyzer:
                self.data_analyzer.text_data = self.text_data
            
            return self.text_data
        except Exception as e:
            print(f"テキストファイルの読み込みエラー: {e}")
            return None
    
    def analyze_data_structure(self) -> Optional[Dict[str, Any]]:
        """
        データ構造を分析
        
        Returns:
            分析結果
        """
        if not self.data_analyzer:
            print("データが読み込まれていません。")
            return None
        
        analysis = self.data_analyzer.analyze_data_structure()
        self.analysis_results['data_structure'] = analysis
        return analysis
    
    def ai_analyze_data(self, custom_prompt: Optional[str] = None) -> Optional[str]:
        """
        AIによるデータ分析
        
        Args:
            custom_prompt: カスタムプロンプト
            
        Returns:
            分析結果テキスト
        """
        if not self.data_analyzer:
            print("データが読み込まれていません。")
            return None
        
        # データの基本情報を取得
        data_info = self.data_analyzer.analyze_data_structure()
        data_sample = self.df.head(10).to_string()
        
        # AI分析を実行
        analysis_result = self.ai_analyzer.analyze_data_with_ai(
            data_info=data_info,
            data_sample=data_sample,
            text_context=self.text_data,
            custom_prompt=custom_prompt
        )
        
        if analysis_result:
            self.analysis_results['ai_analysis'] = analysis_result
        
        return analysis_result
    
    def create_visualizations(self, chart_type: str = 'auto', 
                            columns: Optional[list] = None) -> Optional[Dict[str, str]]:
        """
        データの可視化を作成
        
        Args:
            chart_type: グラフタイプ
            columns: 使用する列名
            
        Returns:
            作成されたファイルパス辞書
        """
        if not self.visualizer:
            print("データが読み込まれていません。")
            return None
        
        visualizations = self.visualizer.create_visualizations(chart_type, columns)
        self.analysis_results['visualizations'] = visualizations
        
        return visualizations
    
    def analyze_visualization_insights(self, visualization_paths: Dict[str, str]) -> Optional[str]:
        """
        可視化結果を分析してインサイトを生成
        
        Args:
            visualization_paths: 可視化ファイルパス辞書
            
        Returns:
            インサイト分析結果
        """
        if not self.data_analyzer:
            print("データが読み込まれていません。")
            return None
        
        # データの統計情報を取得
        stats_info = self.data_analyzer.analyze_data_structure()
        
        # AI分析を実行
        insights = self.ai_analyzer.analyze_visualization_insights(
            data_info=stats_info,
            visualization_paths=visualization_paths
        )
        
        if insights:
            self.analysis_results['visualization_insights'] = insights
        
        return insights
    
    def generate_business_strategy(self) -> Optional[str]:
        """
        ビジネス戦略を生成
        
        Returns:
            戦略提案テキスト
        """
        if not self.analysis_results:
            print("分析結果がありません。まず分析を実行してください。")
            return None
        
        # 全ての分析結果を統合
        all_analysis = ""
        for key, value in self.analysis_results.items():
            all_analysis += f"\n{key}: {value}\n"
        
        # AI戦略生成を実行
        strategy = self.ai_analyzer.generate_business_strategy(all_analysis)
        
        if strategy:
            self.analysis_results['business_strategy'] = strategy
        
        return strategy
    
    def process_rows(self, column_name: str, prompt_template: str) -> Optional[pd.DataFrame]:
        """
        CSVの各行に対してAI処理を実行
        
        Args:
            column_name: 処理対象の列名
            prompt_template: プロンプトテンプレート
            
        Returns:
            処理結果が追加されたDataFrame
        """
        if self.df is None:
            print("CSVファイルが読み込まれていません。")
            return None
        
        if column_name not in self.df.columns:
            print(f"列 '{column_name}' が見つかりません。")
            return None
        
        results = []
        
        for index, row in self.df.iterrows():
            try:
                result = self.ai_analyzer.process_individual_rows(
                    data_series=row[column_name],
                    prompt_template=prompt_template
                )
                results.append(result)
                print(f"行 {index+1} 処理完了")
                
            except Exception as e:
                print(f"行 {index+1} でエラー: {e}")
                results.append(f"エラー: {e}")
        
        # 結果を新しい列として追加
        self.df['AI_Result'] = results
        return self.df
    
    def save_results(self, output_path: str) -> bool:
        """
        結果をCSVファイルとして保存
        
        Args:
            output_path: 出力ファイルパス
            
        Returns:
            保存成功フラグ
        """
        if self.df is None:
            print("保存するデータがありません。")
            return False
        
        try:
            self.df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"結果を保存しました: {output_path}")
            return True
        except Exception as e:
            print(f"保存エラー: {e}")
            return False
    
    def save_analysis_report(self, output_path: str) -> bool:
        """
        分析レポートを保存
        
        Args:
            output_path: 出力ファイルパス
            
        Returns:
            保存成功フラグ
        """
        if not self.analysis_results:
            print("分析結果がありません。")
            return False
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("企業データ分析レポート\n")
                f.write("=" * 50 + "\n\n")
                
                # 設定情報を含める
                f.write("使用設定:\n")
                f.write(f"- 分析モデル: {Config.ANALYSIS_MODEL}\n")
                f.write(f"- 戦略モデル: {Config.STRATEGY_MODEL}\n")
                f.write(f"- 処理モデル: {Config.PROCESSING_MODEL}\n\n")
                
                for key, value in self.analysis_results.items():
                    f.write(f"{key.upper()}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"{value}\n\n")
            
            print(f"分析レポートを保存しました: {output_path}")
            return True
        except Exception as e:
            print(f"保存エラー: {e}")
            return False
def main():
    """
    企業データ分析システムのメイン関数
    """
    print("=" * 60)
    print("企業データ分析・可視化・戦略提案システム")
    print("=" * 60)
    
    # システムの初期化
    try:
        analyzer = BusinessDataAnalyzer()
        print("✓ システムが正常に初期化されました")
    except Exception as e:
        print(f"✗ システム初期化エラー: {e}")
        return
    
    # データの読み込み
    print("\n=== データの読み込み ===")
    csv_file = input("CSVファイルのパスを入力してください: ")
    
    df = analyzer.read_csv(csv_file)
    if df is None:
        print("CSVファイルの読み込みに失敗しました。")
        return
    
    # テキストファイルの読み込み（オプション）
    text_choice = input("追加のテキストファイルを読み込みますか？ (y/n): ")
    if text_choice.lower() == 'y':
        text_file = input("テキストファイルのパスを入力してください: ")
        analyzer.read_text_file(text_file)
    
    # データの概要を表示
    print("\n=== データの概要 ===")
    print(df.head())
    print(f"\nデータ型:\n{df.dtypes}")
    print(f"\n欠損値:\n{df.isnull().sum()}")
    
    # 処理メニュー
    while True:
        print("\n=== 処理メニュー ===")
        print("1. データ構造分析")
        print("2. AI による詳細分析")
        print("3. データ可視化")
        print("4. 可視化インサイト分析")
        print("5. ビジネス戦略提案")
        print("6. 分析レポート保存")
        print("7. 個別行処理")
        print("8. 設定表示")
        print("9. 終了")
        
        choice = input("選択してください (1-9): ")
        
        if choice == "1":
            print("\n=== データ構造分析中... ===")
            structure_analysis = analyzer.analyze_data_structure()
            if structure_analysis:
                print("\n✓ データ構造分析完了")
                print(f"基本情報: {structure_analysis['basic_info']}")
        
        elif choice == "2":
            print("\n=== AI分析中... ===")
            ai_analysis = analyzer.ai_analyze_data()
            if ai_analysis:
                print("\n=== AI分析結果 ===")
                print(ai_analysis)
        
        elif choice == "3":
            print("\n=== データ可視化 ===")
            print("1. 散布図 (scatter)")
            print("2. 棒グラフ (bar)")
            print("3. 線グラフ (line)")
            print("4. ダッシュボード (dashboard)")
            print("5. 自動選択 (auto)")
            
            chart_choice = input("グラフタイプを選択してください (1-5): ")
            chart_types = {
                '1': 'scatter', 
                '2': 'bar', 
                '3': 'line', 
                '4': 'dashboard',
                '5': 'auto'
            }
            chart_type = chart_types.get(chart_choice, 'auto')
            
            print(f"\n=== {chart_type}グラフを作成中... ===")
            visualizations = analyzer.create_visualizations(chart_type=chart_type)
            if visualizations:
                print("✓ 可視化完了")
                for name, path in visualizations.items():
                    print(f"  - {name}: {path}")
        
        elif choice == "4":
            print("\n=== 可視化インサイト分析中... ===")
            if 'visualizations' in analyzer.analysis_results:
                insights = analyzer.analyze_visualization_insights(
                    analyzer.analysis_results['visualizations']
                )
                if insights:
                    print("\n=== 可視化インサイト ===")
                    print(insights)
            else:
                print("まず可視化を実行してください。")
        
        elif choice == "5":
            print("\n=== ビジネス戦略提案中... ===")
            strategy = analyzer.generate_business_strategy()
            if strategy:
                print("\n=== ビジネス戦略提案 ===")
                print(strategy)
        
        elif choice == "6":
            output_path = input("レポートファイル名を入力してください (.txt): ")
            analyzer.save_analysis_report(output_path)
        
        elif choice == "7":
            print("\n利用可能な列:")
            for i, col in enumerate(df.columns):
                print(f"{i+1}. {col}")
            
            try:
                col_choice = input("処理する列の番号を入力: ")
                col_index = int(col_choice) - 1
                column_name = df.columns[col_index]
                
                prompt_template = input("プロンプトテンプレートを入力 (データは{data}で参照): ")
                
                print(f"\n=== 列 '{column_name}' を処理中... ===")
                result_df = analyzer.process_rows(column_name, prompt_template)
                
                if result_df is not None:
                    save_choice = input("結果を保存しますか? (y/n): ")
                    if save_choice.lower() == 'y':
                        output_path = input("出力ファイル名を入力: ")
                        analyzer.save_results(output_path)
            
            except (ValueError, IndexError):
                print("無効な選択です。")
        
        elif choice == "8":
            Config.display_config()
        
        elif choice == "9":
            print("システムを終了します。")
            break
        
        else:
            print("無効な選択です。1-9の数字を入力してください。")

if __name__ == "__main__":
    main()
