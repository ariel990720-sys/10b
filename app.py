import streamlit as st
import random

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位抽籤系統", layout="wide")

# CSS 美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 20px; height: 3em; background-color: #f0f2f6; border-radius: 10px; }
    .seat-box {
        background-color: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; 
        color: #0d47a1; font-weight: bold; font-size: 18px; min-height: 60px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .empty-seat {
        background-color: #f5f5f5; border: 2px dashed #bdbdbd; border-radius: 8px; 
        padding: 15px 5px; text-align: center; margin-bottom: 10px; color: #bdbdbd; min-height: 60px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. 初始化狀態與名單管理
if 'shuffled_list' not in st.session_state:
    # --- 【在這裡修改名單】 ---
    
    # 條件 1：視力不好且又是好朋友 (保證排在一起且坐前排)
    vip_partners = ["5吳瑾瑜", "9李忻嬡"] 
    
    # 條件 2：單純視力需求 (保證在前三排)
    vision_only = ["1吳采軒", "21陳彥寧", "25葉明寬"] 
    
    # 全班原始名單 (統一使用：9李忻嬡)
    full_names = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "9李忻嬡", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
    ]

    # --- 自動排隊邏輯 ---
    random.shuffle(vision_only)
    front_pool = vip_partners + vision_only 
    
    # 找出剩下的人並隨機洗牌
    assigned_already = set(front_pool)
    others = [p for p in full_names if p not in assigned_already]
    random.shuffle(others)
    
    # 最終組合名單：視力組排最前面，剩下的隨機
    st.session_state.shuffled_list = front_pool + others
    st.session_state.seated_count = 0
    st.session_state.seats = [None] * 28

# --- 介面呈現 ---
st.title("🏫 10B 尋夢班 座位抽籤系統")

with st.sidebar:
    st.header("⚙️ 控制面板")
    if st.button("🔄 重置並重新洗牌"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# 抽籤按鈕
if st.session_state.seated_count < 28:
    if st.button(f"🎲 抽出下一位同學 ({st.session_state.seated_count}/28)"):
        next_p = st.session_state.shuffled_list[st.session_state.seated_count]
        st.session_state.seats[st.session_state.seated_count] = next_p
        st.session_state.seated_count += 1
        if st.session_state.seated_count == 28:
            st.balloons() # 全部抽完會噴氣球，但不會顯示額外文字

# 視覺元件：黑板
st.markdown("""
    <div style="background-color: #1e3d2f; color: white; padding: 15px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 24px; font-weight: bold; width: 50%; margin: 0 auto 40px auto; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);">
        🎬 黑 板 ( 正 前 方 )
    </div>
""", unsafe_allow_html=True)

# 3. 繪製座位表 (5, 6, 6, 6, 5)
layout = [5, 6, 6, 6, 5]
idx = 0
for row_idx, count in enumerate(layout):
    cols = st.columns(count)
    for i in range(count):
        person = st.session_state.seats[idx]
        with cols[i]:
            if person:
                st.markdown(f'<div class="seat-box">{person}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="empty-seat">{idx + 1}</div>', unsafe_allow_html=True)
        idx += 1
