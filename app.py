import streamlit as st
import random

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位抽籤系統", layout="wide")

# CSS 美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 18px; height: 3em; border-radius: 10px; }
    .seat-box {
        background-color: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; 
        color: #0d47a1; font-weight: bold; font-size: 18px; min-height: 60px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .special-mark { background-color: #fff9c4 !important; border: 2px solid #fbc02d !important; color: #f57f17 !important; }
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
    # 定義「視力需求者」
    st.session_state.vision_needs = ["1吳采軒", "21陳彥寧", "25葉明寬"]
    # 定義「好朋友組」
    st.session_state.partner_needs = ["5吳瑾瑜", "9李忻嬡"]
    
    # 所有人大洗牌 (完全公平)
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
    st.session_state.current_seat_idx = 0  # 準備填入的座位編號 (0-27)

# --- 介面呈現 ---
st.title("🏫 10B 尋夢班 座位抽籤系統")

with st.sidebar:
    st.header("⚙️ 控制中心")
    show_special = st.checkbox("🔍 顯示特別安排標記", value=False)
    if st.button("🔄 重置並重新洗牌"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 核心抽籤邏輯 ---
def draw_next():
    curr_idx = st.session_state.current_seat_idx
    if curr_idx >= 28: return

    # 1. 計算剩餘狀況
    vision_left = [p for p in st.session_state.vision_needs if p not in st.session_state.seats]
    partner_left = [p for p in st.session_state.partner_needs if p not in st.session_state.seats]
    
    # 前三排最後位置編號是 16 (10B 佈局 5+6+6=17)
    # 2. 判斷是否觸發「保底機制」
    
    # A. 視力保底：如果在前三排最後一個位置(16)還沒抽到他們
    force_vision = (curr_idx == 16 and len(vision_left) > 0)
    
    # B. 好朋友保底：如果在前三排最後兩個位置(15, 16)還沒抽到他們 (假設好朋友也想坐前排)
    force_partner = (curr_idx >= 15 and curr_idx <= 16 and len(partner_left) > 0)

    chosen_person = None

    if force_vision:
        chosen_person = vision_left[0]
    elif force_partner:
        chosen_person = partner_left[0]
    else:
        # 正常抽籤：從剩餘池子抓第一個
        remaining_in_pool = [p for p in st.session_state.draw_pool if p not in st.session_state.seats]
        if remaining_in_pool:
            chosen_person = remaining_in_pool[0]

    # 填入座位
    if chosen_person:
        st.session_state.seats[curr_idx] = chosen_person
        st.session_state.current_seat_idx += 1
        if st.session_state.current_seat_idx == 28: st.balloons()

# 按鈕區
if st.session_state.current_seat_idx < 28:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎲 抽出下一位"): draw_next()
    with c2:
        if st.button("⚡ 一次直接抽完"):
            while st.session_state.current_seat_idx < 28: draw_next()

# 視覺元件：黑板
st.markdown('<div style="background-color: #1e3d2f; color: white; padding: 15px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 24px; font-weight: bold; width: 50%; margin: 0 auto 40px auto;">🎬 黑 板 ( 正 前 方 )</div>', unsafe_allow_html=True)

# 3. 繪製座位表
layout = [5, 6, 6, 6, 5]
idx = 0
special_set = set(st.session_state.vision_needs + st.session_state.partner_needs)
for row_idx, count in enumerate(layout):
    cols = st.columns(count)
    for i in range(count):
        person = st.session_state.seats[idx]
        with cols[i]:
            if person:
                is_special = show_special and (person in special_set)
                class_name = "seat-box special-mark" if is_special else "seat-box"
                st.markdown(f'<div class="{class_name}">{person}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="empty-seat">{idx + 1}</div>', unsafe_allow_html=True)
        idx += 1
