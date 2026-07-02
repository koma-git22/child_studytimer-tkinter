import streamlit as st
import time
import os
from PIL import Image

# 1. ページの基本設定（かわいらしいピンク背景風に設定）
st.set_page_config(page_title="親子スケジュール応援アプリ", layout="centered")

# CSSを使って元のアプリの可愛い背景色（#FFF0F0）とデザインを再現
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF0F0;
    }
    .title-text {
        font-size: 32px;
        font-weight: bold;
        color: #333333;
        text-align: center;
        margin-bottom: 20px;
    }
    .timer-text-normal {
        font-size: 64px;
        font-weight: bold;
        color: #333333;
        text-align: center;
    }
    .timer-text-alert {
        font-size: 64px;
        font-weight: bold;
        color: #FF6B8B;
        text-align: center;
    }
    .timer-text-success {
        font-size: 48px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 状態管理（Streamlitでタイマーの状態を記憶する仕組み）
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 1200
if "current_seconds" not in st.session_state:
    st.session_state.current_seconds = 1200
if "running" not in st.session_state:
    st.session_state.running = False
if "completed" not in st.session_state:
    st.session_state.completed = False
if "is_time_up" not in st.session_state:
    st.session_state.is_time_up = False

# 3. タイトル文字の切り替え表示
title_placeholder = st.empty()
if st.session_state.completed:
    if st.session_state.is_time_up:
        title_placeholder.markdown('<div class="title-text">✨ さいごまで ✨</div>', unsafe_allow_html=True)
    else:
        title_placeholder.markdown('<div class="title-text">✨ よくできました！ ✨</div>', unsafe_allow_html=True)
else:
    title_placeholder.markdown('<div class="title-text">⏰ あさのじゅんび ⏰</div>', unsafe_allow_html=True)

# 4. 時間を選ぶボタンエリア（タイマー作動前 ＆ 完了前のみ有効）
if not st.session_state.running and not st.session_state.completed and st.session_state.current_seconds == st.session_state.total_seconds:
    st.write("⏱️ じかんを えらんでね")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("5分", use_container_width=True):
            st.session_state.total_seconds = 300
            st.session_state.current_seconds = 300
            st.rerun()
    with col2:
        if st.button("20分", use_container_width=True):
            st.session_state.total_seconds = 1200
            st.session_state.current_seconds = 1200
            st.rerun()
    with col3:
        if st.button("30分", use_container_width=True):
            st.session_state.total_seconds = 1800
            st.session_state.current_seconds = 1800
            st.rerun()

# 5. カウントダウンタイマー表示用の置き場
timer_placeholder = st.empty()

# 残り時間に応じた文字色の判定とタイマーの文字を生成する関数
def get_timer_html():
    if st.session_state.completed:
        if st.session_state.is_time_up:
            return '<div class="timer-text-success">がんばったね</div>'
        else:
            return '<div class="timer-text-success">やったね！</div>'
    
    mins, secs = divmod(st.session_state.current_seconds, 60)
    time_str = f"{mins:02d}:{secs:02d}"
    
    # 残り10%以下で文字色をピンクにする判定
    if st.session_state.current_seconds <= (st.session_state.total_seconds * 0.1):
        return f'<div class="timer-text-alert">{time_str}</div>'
    else:
        return f'<div class="timer-text-normal">{time_str}</div>'

timer_placeholder.markdown(get_timer_html(), unsafe_allow_html=True)

# 6. プログレスバー（進捗バー）
ratio = st.session_state.current_seconds / st.session_state.total_seconds
progress_bar = st.progress(ratio)

# 7. キャラクター画像の自動探索と表示（★エラーの起きない安全な「中央寄せ」に修正しました！）
current_dir = os.path.dirname(os.path.abspath(__file__))
path_large = os.path.join(current_dir, "pan.JPG")
path_small = os.path.join(current_dir, "pan.jpg")
image_path = path_large if os.path.exists(path_large) else (path_small if os.path.exists(path_small) else None)

if image_path:
    img = Image.open(image_path)
    img.thumbnail((300, 100)) # 300x100のサイズに小さくする
    
    # 左右に余白を作り、真ん中に300px幅の画像を安全に配置
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(img, use_container_width=True)
else:
    st.info("🍞 キャラクター画像 (pan.jpg) をプログラムと同じフォルダに置いてね！")

# 8. ご褒美スタンプの表示（できたーー！！を押したあと）
if st.session_state.completed:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin: 0;'>⭐️⭐️⭐️</h1>", unsafe_allow_html=True)

st.write("---")

# 9. 操作ボタンエリア
# できたーー！！ボタン
if not st.session_state.completed:
    if st.button("🎉 できたーー！！", type="primary", use_container_width=True):
        st.session_state.running = False
        st.session_state.completed = True
        st.rerun()

# 親用のスタート / 一時停止ボタン
if not st.session_state.completed:
    button_label = "いちじていし" if st.session_state.running else ("さいかいする！" if st.session_state.current_seconds < st.session_state.total_seconds else "よーい、スタート！")
    if st.button(button_label, use_container_width=True):
        st.session_state.running = not st.session_state.running
        st.rerun()

# もういちどやる（リセット）ボタン
if st.session_state.completed or st.session_state.current_seconds < st.session_state.total_seconds:
    if st.button("🔄 もういちど やる", use_container_width=True):
        st.session_state.current_seconds = st.session_state.total_seconds
        st.session_state.running = False
        st.session_state.completed = False
        st.session_state.is_time_up = False
        st.rerun()

# 10. タイマーカウントダウンの実処理
if st.session_state.running and st.session_state.current_seconds > 0:
    time.sleep(1)
    st.session_state.current_seconds -= 1
    
    # タイムアップ（0秒）になったときの判定
    if st.session_state.current_seconds == 0:
        st.session_state.running = False
        st.session_state.completed = True
        st.session_state.is_time_up = True
        
    st.rerun()
