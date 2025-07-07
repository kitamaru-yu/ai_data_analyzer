import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import threading
import time

class DataAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("企業データ分析システム - GUI起動")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # Streamlitプロセス
        self.streamlit_process = None
        
        # メインフレーム
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # タイトル
        title_label = tk.Label(main_frame, text="🏢 企業データ分析システム", 
                              font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        # 説明
        desc_label = tk.Label(main_frame, text="AI を活用した高度なデータ分析と戦略提案", 
                             font=("Arial", 12), bg='#f0f0f0', fg='#666')
        desc_label.pack(pady=5)
        
        # ボタンフレーム
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=30)
        
        # Streamlit起動ボタン
        self.start_button = tk.Button(button_frame, text="🚀 GUI アプリケーションを起動", 
                                     command=self.start_streamlit, 
                                     font=("Arial", 14, "bold"),
                                     bg='#4CAF50', fg='white', 
                                     padx=20, pady=10,
                                     cursor='hand2')
        self.start_button.pack(pady=10)
        
        # 停止ボタン
        self.stop_button = tk.Button(button_frame, text="⏹️ アプリケーションを停止", 
                                    command=self.stop_streamlit, 
                                    font=("Arial", 14, "bold"),
                                    bg='#f44336', fg='white', 
                                    padx=20, pady=10,
                                    cursor='hand2',
                                    state='disabled')
        self.stop_button.pack(pady=10)
        
        # ブラウザ起動ボタン
        self.browser_button = tk.Button(button_frame, text="🌐 ブラウザで開く", 
                                       command=self.open_browser, 
                                       font=("Arial", 12),
                                       bg='#2196F3', fg='white', 
                                       padx=20, pady=8,
                                       cursor='hand2',
                                       state='disabled')
        self.browser_button.pack(pady=10)
        
        # ステータス
        self.status_label = tk.Label(main_frame, text="状態: 停止中", 
                                    font=("Arial", 10), bg='#f0f0f0', fg='#666')
        self.status_label.pack(pady=10)
        
        # 進捗バー
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(pady=10, fill='x')
        
        # 情報フレーム
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(pady=20, fill='x')
        
        info_text = tk.Text(info_frame, height=8, width=70, 
                           font=("Arial", 9), bg='#fff', fg='#333',
                           wrap=tk.WORD)
        info_text.pack(pady=10)
        
        info_content = """
📊 主な機能:
• データ分析: 基本統計、相関分析、時系列分析
• 可視化: インタラクティブグラフ、ダッシュボード
• AI戦略提案: 自動洞察抽出、ビジネス改善提案

🚀 使用方法:
1. 「GUI アプリケーションを起動」ボタンをクリック
2. ブラウザで http://localhost:8501 が開きます
3. CSVファイルをアップロードして分析開始

💡 Tips:
• OpenAI API Keyが必要です
• CSVファイルは企業データを推奨
• 分析結果はMarkdown形式でダウンロード可能
        """
        
        info_text.insert(tk.END, info_content)
        info_text.config(state='disabled')
        
        # 終了処理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start_streamlit(self):
        """Streamlitアプリケーションを起動"""
        try:
            self.status_label.config(text="状態: 起動中...", fg='#ff9800')
            self.start_button.config(state='disabled')
            self.progress.start()
            
            # 作業ディレクトリに移動
            os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Streamlitプロセスを起動
            self.streamlit_process = subprocess.Popen([
                "streamlit", "run", "src/ui/streamlit_app.py", 
                "--server.port", "8501",
                "--server.headless", "true"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            
            # 起動完了を待つ
            threading.Thread(target=self.wait_for_startup, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("エラー", f"起動に失敗しました: {e}")
            self.reset_ui()
    
    def wait_for_startup(self):
        """起動完了を待つ"""
        time.sleep(5)  # 起動を待つ
        
        self.root.after(0, self.startup_complete)
    
    def startup_complete(self):
        """起動完了後の処理"""
        self.progress.stop()
        self.status_label.config(text="状態: 実行中 (http://localhost:8501)", fg='#4CAF50')
        self.stop_button.config(state='normal')
        self.browser_button.config(state='normal')
        
        # 自動的にブラウザを開く
        self.open_browser()
    
    def stop_streamlit(self):
        """Streamlitアプリケーションを停止"""
        if self.streamlit_process:
            self.streamlit_process.terminate()
            self.streamlit_process = None
        
        self.reset_ui()
        messagebox.showinfo("情報", "アプリケーションを停止しました")
    
    def open_browser(self):
        """ブラウザでアプリケーションを開く"""
        webbrowser.open("http://localhost:8501")
    
    def reset_ui(self):
        """UIをリセット"""
        self.status_label.config(text="状態: 停止中", fg='#666')
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.browser_button.config(state='disabled')
        self.progress.stop()
    
    def on_closing(self):
        """終了時の処理"""
        if self.streamlit_process:
            self.streamlit_process.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisGUI(root)
    root.mainloop()
