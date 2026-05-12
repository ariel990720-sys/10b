import streamlit as st
import random

# 1. 網頁基本設定
st.set_page_config(page_title="10B 自定義抽籤系統", layout="wide")

# CSS 美化
st.markdown("""
    <style>
    .stButton>button {width: 100%; font-size: 20px; height: 3em; background-color: #f0f2f6;}
    .seat-box {
        background-color: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; 
        color: #0d47a1; font-weight: bold; font-size: 16px; min-height: 60px;
    }
    .empty-seat {
        background-color: #f5f5f5; border: 2px dashed #bdbdbd; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; color: #bdbdbd; min-height: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 初始化狀態 (防止重新整理就重來)
if 'shuffled_names' not in st.session_state:
    # 原始名單
    base_names = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "9李忻懓", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
    ]
    # --- 💡 在這裡設定「固定條件」 ---
    # 例如：想要 1 吳采軒 固定在第一個位置 (第一排左一)
    # 這裡我們預設不固定，讓程式隨機
    random.shuffle(base_names)
    st.session_state.shuffled_names = base_names
    st.session_state.seated_count = 0  # 目前已入座人數
    st.session_state.seats = [None] * 28 # 28個座位狀況

st.title("🎲 10B 逐位抽籤系統")

# 側邊欄設定條件 (選配)
with st.sidebar:
    st.header("⚙️ 抽籤設定")
    if st.button("🔄 重置所有座位"):
        st.session_state.shuffled_names = random.sample(st.session_state.shuffled_names, 28)
        st.session_state.seated_count = 0
        st.session_state.seats = [None] * 28
        st.rerun()
    st.info("提示：點擊右側按鈕一個一個抽出同學。")

# 抽籤按鈕
if st.session_state.seated_count < 28:
    if st.button(f"🔥 抽出下一位同學 (已抽 {st.session_state.seated_count}/28)"):
        # 取得下一位同學
        next_person = st.session_state.shuffled_names[st.session_state.seated_count]
        st.session_state.seats[st.session_state.seated_count] = next_person
        st.session_state.seated_count += 1
        st.success(f"🎊 最新抽中：{next_person}")
else:
    st.warning("所有位置已入座完畢！")

# --- 視覺元件：黑板 ---
st.markdown("""
    <div style="background-color: #1e3d2f; color: white; padding: 15px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 24px; font-weight: bold; width: 50%; margin: 0 auto 30px auto;">
        🎬 黑 板 ( 正 前 方 )
    </div>
""", unsafe_allow_html=True)

# 3. 繪製座位表
layout = [5, 6, 6, 6, 5]
current_seat_idx = 0

for row_idx, count in enumerate(layout):
    cols = st.columns(count)
    for i in range(count):
        person = st.session_state.seats[current_seat_idx]
        with cols[i]:
            if person:
                st.markdown(f'<div class="seat-box">{person}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="empty-seat">第{current_seat_idx+1}號位</div>', unsafe_allow_html=True)
        current_seat_idx += 1
