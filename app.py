import streamlit as st
import random

st.set_page_config(page_title="10B 專業抽籤系統", layout="wide")

# CSS 美化 (維持之前的質感)
st.markdown("""
    <style>
    .seat-box { background-color: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; padding: 15px 5px; text-align: center; margin-bottom: 10px; color: #0d47a1; font-weight: bold; font-size: 16px; min-height: 60px; }
    .empty-seat { background-color: #f5f5f5; border: 2px dashed #bdbdbd; border-radius: 8px; padding: 15px 5px; text-align: center; margin-bottom: 10px; color: #bdbdbd; min-height: 60px; }
    .special-seat { border: 2px solid #ff9800; background-color: #fff3e0; color: #e65100; }
    </style>
""", unsafe_allow_html=True)

# 1. 初始化狀態
if 'shuffled_list' not in st.session_state:
    # --- ⚙️ 在這裡設定特殊條件 ---
    
    # A. 必須在前三排的人 (前 17 個位置)
    front_row_needs = ["12洪軒平", "4吳元希"] # 範例：這兩位視力不好
    
    # B. 想要坐在一起的一組人 (會連續抽出)
    partners = ["26劉苡樂", "9李忻懓"] # 範例：這兩位要一起坐
    
    # C. 其他所有人 (自動排除掉上面已經設定的人)
    others = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "28簡向晨"
    ]
    # 先把 others 洗牌
    random.shuffle(others)
    
    # 組合邏輯：
    # 1. 先把視力不好的人放進前三排的隨機位置
    # 2. 把好朋友組合塞在一起
    # 這裡我們用一個簡單的「抽籤池」
    full_pool = front_row_needs + partners + others
    # (注意：這裡只是範例邏輯，最公平的做法是手動在名單調整順序)
    
    st.session_state.shuffled_list = full_pool 
    st.session_state.seated_count = 0
    st.session_state.seats = [None] * 28

st.title("🎲 10B 智慧座位系統")

# 2. 功能按鈕
with st.sidebar:
    st.header("⚙️ 管理員面板")
    if st.button("🔄 重置並重新洗牌"):
        del st.session_state['shuffled_list']
        st.rerun()
    st.write("---")
    st.write("**特殊需求說明：**")
    st.write("1. 視力需求者已優先排入前三排池。")
    st.write("2. 好朋友組合已設定為連號抽出。")

if st.session_state.seated_count < 28:
    if st.button(f"🔥 抽出下一位 (第 {st.session_state.seated_count + 1} 位)"):
        next_p = st.session_state.shuffled_list[st.session_state.seated_count]
        st.session_state.seats[st.session_state.seated_count] = next_p
        st.session_state.seated_count += 1
        st.success(f"🎊 最新抽中：{next_p}")

# --- 視覺：黑板 ---
st.markdown('<div style="background-color: #1e3d2f; color: white; padding: 15px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 24px; font-weight: bold; width: 50%; margin: 0 auto 30px auto;">🎬 黑 板 ( 正 前 方 )</div>', unsafe_allow_html=True)

# 3. 繪製座位
layout = [5, 6, 6, 6, 5]
idx = 0
for row_idx, count in enumerate(layout):
    cols = st.columns(count)
    for i in range(count):
        person = st.session_state.seats[idx]
        with cols[i]:
            if person:
                # 如果是特殊需求的人，給他一個不同的顏色橘色 (optional)
                style = "seat-box special-seat" if idx < 5 else "seat-box" 
                st.markdown(f'<div class="{style}">{person}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="empty-seat">?</div>', unsafe_allow_html=True)
        idx += 1
