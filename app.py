import streamlit as st
import random
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位系統", layout="wide")

# CSS 美化：拿掉所有不必要的標籤樣式
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 16px; height: 3em; border-radius: 10px; margin-bottom: 10px; }
    .seat { border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 10px; font-weight: bold; min-height: 65px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
    .normal { background-color: #e3f2fd; border: 2px solid #2196f3; color: #0d47a1; }
    .vision { background-color: #ffe0b2; border: 2px solid #fb8c00; color: #ef6c00; }
    .friend { background-color: #fce4ec; border: 2px solid #f06292; color: #ad1457; }
    .empty  { background-color: #fdfdfd; border: 1px dashed #e0e0e0; } /* 💡 抽籤前完全空白的格子 */
    .blocked { visibility: hidden; } 
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. 初始化狀態
if 'seats' not in st.session_state:
    st.session_state.vision_list = ["1吳采軒", "21陳彥寧", "25葉明寬"]
    st.session_state.best_friends = ["5吳瑾瑜", "9李忻嬡"]
    
    all_names = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "9李忻嬡", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
    ]
    
    st.session_state.pool = all_names.copy()
    random.shuffle(st.session_state.pool)
    st.session_state.seats = [None] * 30
    st.session_state.count = 0 
    st.session_state.blocked_indices = [0, 29]

# 3. 核心抽籤函數
def draw_next():
    idx = 0
    while idx < 30 and (idx in st.session_state.blocked_indices or st.session_state.seats[idx] is not None):
        idx += 1
    if idx >= 30: return

    vision_left = [p for p in st.session_state.vision_list if p not in st.session_state.seats]
    friends_left = [p for p in st.session_state.best_friends if p not in st.session_state.seats]
    available_front = [i for i in range(18) if i not in st.session_state.blocked_indices and st.session_state.seats[i] is None]
    
    chosen = None
    if idx < 18 and len(available_front) <= (len(vision_left) + len(friends_left)):
        chosen = friends_left[0] if friends_left else vision_left[0]
    else:
        pool_left = [p for p in st.session_state.pool if p not in st.session_state.seats]
        if pool_left: chosen = pool_left[0]

    if chosen:
        st.session_state.seats[idx] = chosen
        st.session_state.count += 1
        if chosen in st.session_state.best_friends:
            other = [p for p in st.session_state.best_friends if p != chosen][0]
            if other not in st.session_state.seats:
                next_idx = idx + 1
                while next_idx < 30 and next_idx in st.session_state.blocked_indices:
                    next_idx += 1
                if next_idx < 30:
                    st.session_state.seats[next_idx] = other
                    st.session_state.count += 1

# 4. 側邊欄介面
with st.sidebar:
    st.header("⚙️ 控制中心")
    if st.session_state.count < 28:
        if st.button("🎲 抽出下一位"): draw_next()
        if st.button("⚡ 一次直接抽完"):
            while st.session_state.count < 28: draw_next()
    
    show_mark = st.checkbox("🔍 顯示特別安排標記", value=False)
    if st.button("🔄 重置並重新洗牌"):
        st.session_state.clear()
        st.rerun()

    if st.session_state.count > 0:
        st.write("---")
        report = ""
        for i, name in enumerate(st.session_state.seats):
            if i not in st.session_state.blocked_indices:
                report += f"位置{i+1}: {name if name else '(空)'}\n"
        st.text_area("📋 複製文字存檔到 Google 文件", report, height=150)

# 5. 主畫面：座位圖
st.title("🏫 10B 尋夢班 座位抽籤系統")

# 黑板
st.markdown('<div style="background-color: #1e3d2f; color: white; padding: 10px; text-align: center; border-radius: 8px; font-size: 24px; font-weight: bold; width: 40%; margin: 0 auto 30px auto;">🎬 黑 板</div>', unsafe_allow_html=True)

for row in range(5):
    cols = st.columns(6)
    for col in range(6):
        idx = row * 6 + col
        with cols[col]:
            if idx in st.session_state.blocked_indices:
                st.markdown('<div class="seat blocked"></div>', unsafe_allow_html=True)
            else:
                name = st.session_state.seats[idx]
                style = "normal"
                if show_mark and name:
                    if name in st.session_state.vision_list: style = "vision"
                    if name in st.session_state.best_friends: style = "friend"
                
                if name:
                    # 💡 只顯示名字
                    st.markdown(f'<div class="seat {style}">{name}</div>', unsafe_allow_html=True)
                else:
                    # 💡 抽籤前完全空白，連標籤都沒有
                    st.markdown(f'<div class="seat empty"></div>', unsafe_allow_html=True)

if st.session_state.count >= 28:
    st.balloons()
