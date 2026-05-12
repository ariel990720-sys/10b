import streamlit as st
import random

# 1. 網頁基本設定
st.set_page_config(page_title="10B 智慧座位抽籤系統", layout="wide")

# CSS 樣式美化
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
    # --- ⚙️ 【管理員自定義區】 ---
    
    # 條件 A：視力需求 (保證在前三排)
    # 如果這兩個人又是好朋友，就直接這樣排在一起放進來
    front_row_needs = ["12洪軒平", "4吳元希"] 
    
    # 條件 B：單純好朋友組 (連號抽出)
    partners = ["26劉苡樂", "9李忻懓"] 
    
    # 全班原始名單
    all_students = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "28簡向晨"
    ]
    
    # 邏輯處理：排除已在特殊名單的人，剩下的隨機洗牌
    others = [p for p in all_students if p not in front_row_needs and p not in partners]
    random.shuffle(others)
    
    # 最終組合：前排需求 + 好朋友組 + 隨機剩餘
    st.session_state.shuffled_list = front_row_needs + partners + others
    st.session_state.seated_count = 0
    st.session_state.seats = [None] * 28

# --- 介面呈現 ---
st.title("🏫 10B 教室座位圖")

# 側邊欄控制
with st.sidebar:
    st.header("⚙️ 控制面板")
    if st.button("🔄 重置並重新洗牌"):
        # 刪除狀態讓程式重新執行初始化
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
    st.write("---")
    st.write("**當前條件設定：**")
    st.write("- 視力需求組已排入優先池")
    st.write("- 好朋友組已設定連號")

# 抽籤按鈕
if st.session_state.seated_count < 28:
    if st.button(f"🎲 點擊抽出下一位 (已完成 {st.session_state.seated_count}/28)"):
        next_p = st.session_state.shuffled_list[st.session_state.seated_count]
        st.session_state.seats[st.session_state.seated_count] = next_p
        st.session_state.seated_count += 1
        if st.session_state.seated_count == 28:
            st.balloons() # 全抽完噴氣球
else:
    st.success("🎉 28 位同學已全部入座！")

# 視覺元件：黑板
st.markdown("""
    <div style="background-color: #1e3d2f; color: white; padding: 15px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 24px; font-weight: bold; width: 50%; margin: 0 auto 40px auto; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);">
        🎬 黑 板 ( 正 前 方 )
    </div>
""", unsafe_allow_html=True)

# 3. 繪製座位表 (佈局：5, 6, 6, 6, 5)
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
