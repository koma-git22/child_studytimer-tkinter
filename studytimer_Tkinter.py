# =====================================================================
# 親子スケジュール応援アプリ (あさのじゅんび)
# Copyright (c) 2026 [あなたの名前、またはGitHubのアカウント名]
# This software is released under the MIT License.
# http://opensource.org
# =====================================================================

import tkinter as tk
import time
import threading
from PIL import Image, ImageTk

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("親子スケジュール応援アプリ")
        self.root.geometry("400x650")
        self.root.configure(bg="#FFF0F0")

        # 状態管理
        self.total_seconds = 1200  
        self.current_seconds = self.total_seconds
        self.running = False
        self.started = False  
        self.jump_count = 0
        self.is_time_up = False  
        self.start_btn_disabled = False  

        # タイトル文字
        self.title_label = tk.Label(
            root, text="⏰ あさのじゅんび ⏰", 
            font=("Helvetica", 24, "bold"), fg="#333333", bg="#FFF0F0"
        )
        self.title_label.pack(pady=15)

        # 時間をえらぶエリアの作成
        self.select_frame = tk.Frame(root, bg="#FFF0F0")
        self.select_frame.pack(pady=5)

        self.time_options = {"5分": 300, "20分": 1200, "30分": 1800}
        self.btn_canvases = {}  

        for label, seconds in self.time_options.items():
            btn = tk.Canvas(self.select_frame, width=70, height=35, bg="#FFF0F0", highlightthickness=0, cursor="hand2")
            btn.pack(side="left", padx=5)
            btn.bind("<Button-1>", lambda event, s=seconds: self.set_custom_time(s))
            self.btn_canvases[seconds] = btn  

        # カウントダウンタイマー
        self.timer_label = tk.Label(
            root, text="20:00",
            font=("Helvetica", 48, "bold"), fg="#333333", bg="#FFF0F0"
        )
        self.timer_label.pack(pady=10)

        # 手作りの角丸プログレスバー（Canvas）
        self.bar_width = 300
        self.bar_height = 20
        self.progress_canvas = tk.Canvas(
            root, width=self.bar_width, height=self.bar_height, bg="#FFF0F0", highlightthickness=0
        )
        self.progress_canvas.pack(pady=15)

        # キャラクター表示
        self.canvas = tk.Canvas(root, width=300, height=150, bg="#FFF0F0", highlightthickness=0)
        self.canvas.pack(pady=15)
        
        # --- 画像の読み込み ---
        image_path = "/Users/kitamuramaho/Downloads/pan.jpg"
        
        img = Image.open(image_path)
        img.thumbnail((300, 100)) 
        self.char_img = ImageTk.PhotoImage(img)
        
        self.char_id = self.canvas.create_image(
            150, 150, image=self.char_img, anchor="s"
        )
        
        # ご褒美スタンプ
        self.stamp_id = self.canvas.create_text(
            150, 25, text="⭐⭐️⭐️", font=("Helvetica", 40), state="hidden"
        )

        # できたーー！！ボタン（角丸）
        self.btn_canvas = tk.Canvas(root, width=250, height=60, bg="#FFF0F0", highlightthickness=0, cursor="hand2")
        self.btn_canvas.pack(pady=15)
        
        self.create_round_rect(self.btn_canvas, 0, 0, 250, 60, radius=30, fill="#E91E63", outline="")
        self.btn_canvas.create_text(125, 30, text="できたー！！", fill="white", font=("Helvetica", 20, "bold"))
        self.btn_canvas.bind("<Button-1>", lambda event: self.on_complete())

        # 親用のスタートボタン（角丸キャンバス）
        self.start_btn_canvas = tk.Canvas(root, width=220, height=45, bg="#FFF0F0", highlightthickness=0, cursor="hand2")
        self.start_btn_canvas.pack(pady=10)
        
        self.create_round_rect(self.start_btn_canvas, 0, 0, 220, 45, radius=22, fill="#9E9E9E", outline="")
        self.start_btn_text_id = self.start_btn_canvas.create_text(
            110, 22, text="よーい、スタート！", fill="white", font=("Helvetica", 14, "bold")
        )
        self.start_btn_canvas.bind("<Button-1>", lambda event: self.toggle_timer())

        self.set_custom_time(self.total_seconds)

    def create_round_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def set_custom_time(self, selected_seconds):
        if self.started:
            return
        
        self.total_seconds = selected_seconds
        self.current_seconds = selected_seconds
        
        mins, secs = divmod(self.current_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        
        for text_label, seconds in self.time_options.items():
            btn = self.btn_canvases[seconds]
            btn.delete("all")  
            btn_color = "#9E9E9E" if seconds == selected_seconds else "#BCAAA4"
            self.create_round_rect(btn, 0, 0, 70, 35, radius=15, fill=btn_color, outline="")
            btn.create_text(35, 17, text=text_label, fill="white", font=("Helvetica", 11, "bold"))
        
        self.refresh_ui()

    def update_timer(self):
        while self.current_seconds > 0 and self.running:
            time.sleep(1)
            if not self.running:
                break
            self.current_seconds -= 1
            self.root.after(0, self.refresh_ui)
        
        if self.current_seconds == 0:
            self.root.after(0, self.time_up_ui)

    def refresh_ui(self):
        mins, secs = divmod(self.current_seconds, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        self.progress_canvas.delete("all")
        ratio = self.current_seconds / self.total_seconds
        current_width = self.bar_width * ratio

        if self.current_seconds <= (self.total_seconds * 0.1):
            bar_color = "#FF5252"
            text_color = "#D32F2F"
        else:
            bar_color = "#4FC3F7"
            text_color = "#333333"

        self.timer_label.config(fg=text_color)

        if current_width > self.bar_height:
            self.create_round_rect(self.progress_canvas, 0, 0, self.bar_width, self.bar_height, radius=10, fill="#E0E0E0", outline="")
            self.create_round_rect(self.progress_canvas, 0, 0, current_width, self.bar_height, radius=10, fill=bar_color, outline="")
        else:
            self.create_round_rect(self.progress_canvas, 0, 0, self.bar_width, self.bar_height, radius=10, fill="#E0E0E0", outline="")

    def time_up_ui(self):
        self.running = False
        self.is_time_up = True  
        self.timer_label.config(text="00:00", fg="#D32F2F") 
        self.refresh_ui()
        
        self.start_btn_disabled = True
        self.start_btn_canvas.delete("all")
        self.create_round_rect(self.start_btn_canvas, 0, 0, 220, 45, radius=22, fill="#E0E0E0", outline="")
        self.start_btn_canvas.create_text(110, 22, text="よーい、スタート！", fill="#BDBDBD", font=("Helvetica", 14, "bold"))

    def toggle_timer(self):
        # 終了判定テキストをひらがなの「ね」に変更
        if "ね" in self.timer_label.cget("text"):
            return

        if self.running:
            self.running = False
            self.start_btn_canvas.itemconfig(self.start_btn_text_id, text="さいかいする！")
        else:
            if self.current_seconds > 0:
                self.running = True
                self.started = True  
                self.start_btn_canvas.itemconfig(self.start_btn_text_id, text="いちじていし")
                threading.Thread(target=self.update_timer, daemon=True).start()

    def on_complete(self):
        if not self.started or "ね" in self.timer_label.cget("text"):
            return

        self.running = False
        self.start_btn_disabled = True
        
        self.start_btn_canvas.delete("all")
        self.create_round_rect(self.start_btn_canvas, 0, 0, 220, 45, radius=22, fill="#E0E0E0", outline="")
        self.start_btn_canvas.create_text(110, 22, text="よーい、スタート！", fill="#BDBDBD", font=("Helvetica", 14, "bold"))
        
        self.jump_count = 0
        self.animate_loop()

    def animate_loop(self):
        if self.jump_count < 20:
            direction = -10 if (self.jump_count % 10) < 5 else 10
            self.canvas.move(self.char_id, 0, direction)
            self.jump_count += 1
            self.root.after(30, self.animate_loop)
        else:
            self.canvas.itemconfig(self.stamp_id, state="normal")
            
            # ### 【修正箇所】メッセージのテキストをご指定のひらがな表記に変更しました ###
            if self.is_time_up:
                self.title_label.config(text="✨ さいごまで ✨")
                self.timer_label.config(text="がんばったね", fg="#2E7D32")
            else:
                self.title_label.config(text="✨ よくできました！ ✨")
                self.timer_label.config(text="やったね！", fg="#2E7D32")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
