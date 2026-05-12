import streamlit as st
import random

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位抽籤系統", layout="wide")

# CSS 美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 16px; height: 3em; border-radius: 10px; margin-bottom: 10px; }
    .seat-box {
        background-color: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; 
        color: #0d47a1; font-weight: bold; font-size: 18px; min-height: 60px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    /* 不同的特殊標記顏色 */
    .vision-mark { background-color: #ffe0b2 !important; border: 2px solid #fb8c00 !important; color: #ef6c00 !important; }
    .friend-mark { background-color: #fce4ec !important; border: 2px solid #f06292 !important; color: #ad1457 !important; }
    
    .empty-seat {
        background-color: #f5f5f5; border: 2px dashed #bdbdbd; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; color: #bdbdbd; min-height: 60px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. 初始化狀態
if 'draw_pool' not in st.session_state:
    st.session_state.vision_needs = ["1吳采軒", "21陳彥寧", "25葉明寬"]
    st.session_state.best_friends = ["5吳瑾瑜", "9李忻嬡"]
    
    full_names = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "9李忻嬡", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
    ]
    
    st.session_state.draw_pool = full_names.copy()
    random.shuffle(st.session_state.draw_pool)
    st.session_state.seats = [None] * 28
    st.session_state.current_seat_idx = 0

# --- 核心抽籤邏輯 ---
def draw_next():
    curr_idx = st.session_state.current_seat_idx
    if curr_idx >= 28: return

    vision_left = [p for p in st.session_state.vision_needs if p not in st.session_state.seats]
    friends_left = [p for p in st.session_state.best_friends if p not in st.session_state.seats]
    total_special_left = len(vision_left) + len(friends_left)
    
    seats_left_in_front = 17 - curr_idx
    chosen_person = None

    if curr_idx < 17 and seats_left_in_front <= total_special_left:
        if friends_left:
            chosen_person = friends_left[0]
        elif vision_left:
            chosen_person = vision_left[0]
    else:
        remaining_in_pool = [p for p in st.session_state.draw_pool if p not in st.session_state.seats]
        if remaining_in_pool:
            chosen_person = remaining_in_pool[0]

    if chosen_person:
        st.session_state.seats[curr_idx] = chosen_person
        st.session_state.current_seat_idx += 1
        
        # 好朋友連帶
        if chosen_person in st.session_state.best_friends:
            other_friend = [p for p in st.session_state.best_friends if p != chosen_person][0]
            if other_friend not in st.session_state.seats and st.session_state.current_seat_idx < 17:
                st.session_state.seats[st.session_state.current_seat_idx] = other_friend
                st.session_state.current_seat_idx += 1

        if st.session_state.current_seat_idx >= 28: st.balloons()

# --- 介面佈局 ---
with st.sidebar:
    st.header("⚙️ 控制中心")
    
    # 抽籤按鈕移至旁邊
    if st.session_state.current_seat_idx < 28:
        if st.button("🎲 抽出下一位"):
            draw_next()
        if st.button("⚡ 一次直接抽完"):
            while st.session_state.current_seat_idx < 28:
                draw_next()
    else:
        st.info("抽籤已完成")

    st.write("---")
    show_special = st.checkbox("🔍 顯示特別安排標記", value=False)
    
    if st.button("🔄 重置並重新洗牌"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    
    # 標記說明 (僅在開啟標記時顯示)
    if show_special:
        st.write("---")
        st.markdown("<span style='color:#ef6c00'>●</span> 橘色：視力需求", unsafe_allow_html=True)
        st.markdown("<span style='color:#ad1457'>●</span> 粉色：好朋友組", unsafe_allow_html=True)

# 右側主畫面
st.title("🏫 10B 尋夢班 座位抽籤系統")

# 視覺元件：黑板 (置中)
st.markdown('<div style="background-color: #1e3d2f; color: white; padding: 15px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 24px; font-weight: bold; width: 60%; margin: 0 auto 40px auto; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);">🎬 黑 板 ( 正 前 方 )</div>', unsafe_allow_html=True)

# 3. 繪製座位表 (佈局 5, 6, 6, 6, 5)
layout = [5, 6, 6, 6, 5]
idx = 0
for row_idx, count in enumerate(layout):
    cols = st.columns(count)
    for i in range(count):
        person = st.session_state.seats[idx]
        with cols[i]:
            if person:
                # 決定標記樣式
                active_class = "seat-box"
                if show_special:
                    if person in st.session_state.vision_needs:
                        active_class += " vision-mark"
                    elif person in st.session_state.best_friends:
                        active_class += " friend-mark"
                
                st.markdown(f'<div class="{active_class}">{person}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="empty-seat">{idx + 1}</div>', unsafe_allow_html=True)
        idx += 1
