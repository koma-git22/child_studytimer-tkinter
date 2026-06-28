import tkinter as tk
from tkinter import ttk
import time
import threading

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("親子スケジュール応援アプリ")
        # スマホ風の画面サイズに固定
        self.root.geometry("400x650")
        self.root.configure(bg="#FFF0F0") # 薄い赤・ピンク系の背景

        # 状態管理
        self.total_seconds = 900  # テスト用に20秒
        self.current_seconds = self.total_seconds
        self.running = False
        self.jump_count = 0  # アニメーション用のカウンター

        # スタイル設定
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # 赤色のプログレスバーを設定
        self.style.configure("Red.Horizontal.TProgressbar", foreground="#D32F2F", background="#FF5252")

        # ---------------------------------------------------------
        # UIコンポーネント（画面の部品）
        # ---------------------------------------------------------
        
        # タイトル文字
        self.title_label = tk.Label(
            root, text="⏰ あさのじゅんび ⏰", 
            font=("Helvetica", 24, "bold"), fg="#333333", bg="#FFF0F0"
        )
        self.title_label.pack(pady=20)

        # カウントダウンタイマー（好きな色の「赤」）
        self.timer_label = tk.Label(
            root, text="15:00", # 表示変更
            font=("Helvetica", 48, "bold"), fg="#D32F2F", bg="#FFF0F0"
        )
        self.timer_label.pack(pady=10)

        # 視覚的な残り時間バー
        self.progress = ttk.Progressbar(
            root, orient="horizontal", length=300, mode="determinate", style="Red.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=10)
        self.progress["maximum"] = self.total_seconds
        self.progress["value"] = self.total_seconds

        # キャラクター表示（キャンバスを使ってジャンプさせます）
        self.canvas = tk.Canvas(root, width=300, height=150, bg="#FFF0F0", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # パンダコパンダをイメージした絵文字（後から画像に差し替え可能）
        self.char_id = self.canvas.create_text(
            150, 100, text="🐼✨🐾", font=("Helvetica", 50)
        )
        
        # ご褒美スタンプ（最初は隠しておく）
        self.stamp_id = self.canvas.create_text(
            150, 40, text="⭐⭐️⭐️", font=("Helvetica", 40), state="hidden"
        )

        # 【Mac用エラー対策】できたーー！！ボタン（大きな赤ボタンをキャンバスで作成）
        self.btn_canvas = tk.Canvas(root, width=250, height=60, bg="#FFF0F0", highlightthickness=0)
        self.btn_canvas.pack(pady=20)
        # 赤い背景を描く
        self.btn_canvas.create_rectangle(0, 0, 250, 60, fill="#D32F2F", outline="")
        # 白い文字を載せる
        self.btn_canvas.create_text(125, 30, text="できたーー！！", fill="white", font=("Helvetica", 20, "bold"))
        # クリックされたら「on_complete」を動かす設定
        self.btn_canvas.bind("<Button-1>", lambda event: self.on_complete())

        # 親用スタートボタン（エラーが起きないシンプルなテキストボタン）
        self.start_button = tk.Button(
            root, text="【親用】よーい、スタート！", font=("Helvetica", 12),
            fg="#666666", bg="#FFF0F0", relief="flat", command=self.start_timer
        )
        self.start_button.pack(pady=10)

    # ---------------------------------------------------------
    # 動き（ロジック）の実装
    # ---------------------------------------------------------
    
    def update_timer(self):
        while self.current_seconds > 0 and self.running:
            time.sleep(1)
            self.current_seconds -= 1
            
            # 画面の更新（メインスレッドにお願いする）
            self.root.after(0, self.refresh_ui)
        
        if self.current_seconds == 0:
            self.root.after(0, self.time_up_ui)

    def refresh_ui(self):
        mins, secs = divmod(self.current_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        self.progress["value"] = self.current_seconds

    def time_up_ui(self):
        self.timer_label.config(text="じかんきれ！", fg="#888888")

    def start_timer(self):
        if not self.running and self.current_seconds > 0:
            self.running = True
            # タイマーを別スレッドで裏で動かす（フリーズ防止）
            threading.Thread(target=self.update_timer, daemon=True).start()

    def on_complete(self):
        self.running = False  # タイマー停止
        self.jump_count = 0   # カウンターをリセット

        # アニメーションループをメインスレッドで実行
        self.animate_loop()

    def animate_loop(self):
        if self.jump_count < 5:
            # 最初の5回は上に動かす
            self.canvas.move(self.char_id, 0, -10)
            self.jump_count += 1
            # 30ミリ秒後にまたこの関数を呼び出す
            self.root.after(30, self.animate_loop)
        elif self.jump_count < 10:
            # 次の5回は下に戻す
            self.canvas.move(self.char_id, 0, 10)
            self.jump_count += 1
            self.root.after(30, self.animate_loop)
        else:
            # アニメーションが終わったらスタンプを表示
            self.canvas.itemconfig(self.stamp_id, state="normal") # 星を表示
            self.title_label.config(text="✨ よくできました！ ✨")
            self.timer_label.config(text="やったね！", fg="#2E7D32")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()


                
#         # 1.キャラクターが上にぴょんと跳ねるアニメーション
#         def junp_animation():
#             # 上に動く
#             for _ in range(5):
#                 self.canvas.move(self.char_id, 0, -10)
#                 self.root.update()
#                 time.sleep(0.03)
#             # 下に戻る
#             for _ in range(5):
#                 self.canvas.move(self.char_id, 0, 10)
#                 self.root.update()
#                 time.sleep(0.03)
                
#             # 2.アニメーション後にスタンプと文字を切り替え
#             self.canvas.itemconfig(self.stamp_id, state='normal')   # 星を表示
#             self.title_label.config(text='✨ よくできました！ ✨')
#             self.timer_label.config(text='やったね！', fg='#2E7D32')
            
#         # アニメーションを別スレッドで滑らかに動かす
#         threading.Thread(target=jump_animation, daemon=True).start()
        
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = ScheduleApp(root)
#     root.mainloop()
    
