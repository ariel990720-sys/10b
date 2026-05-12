import streamlit as st
import random
import pandas as pd

# 1. 網頁外觀 (CSS)
st.set_page_config(page_title="10B 座位系統 - 實體表格版", layout="wide")
st.markdown("""
    <style>
    .seat { border-radius: 5px; padding: 10px; text-align: center; margin: 5px; font-weight: bold; min-height: 50px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
    .normal { background-color: #ffffff; border: 2px solid #333; color: #000; }
    .vision { background-color: #fff3e0; border: 2px solid #ff9800; }
    .friend { background-color: #fce4ec; border: 2px solid #f06292; }
    .label-text { font-size: 12px; color: #666; margin-bottom: 2px; }
    .aisle { width: 40px; } /* 走道寬度 */
    </style>
""", unsafe_allow_html=True)

# 2. 初始化 (與之前相同，確保公平抽籤)
if 'seats_map' not in st.session_state:
    st.session_state.vision_list = ["1吳采軒", "21陳彥寧", "25葉明寬"]
    st.session_state.friend_list = ["5吳瑾瑜", "9李忻嬡"]
    all_names = ["20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉", "5吳瑾瑜", "9李忻嬡", "29顏子旅", "10李維", "17張楚楚", "16陳永軍", "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬", "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤", "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"]
    
    st.session_state.pool = all_names.copy()
    random.shuffle(st.session_state.pool)
    
    # 這裡我們用一個「字典」來存，Key 是你原本表格的代號 (例如 下1, 下2)
    st.session_state.seats_map = {} 
    st.session_state.count = 0

# 3. 抽籤邏輯：將抽到的人「填入」指定的代號位置
# 依照你圖片的順序定義位置清單
座位順序 = [
    "下1", "下2", "下3", "下4", "下5", "下6", 
    "下7", "下8", "下9", "下10", "下11", "下12",
    # ...以此類推，直到 28 個
]

def 執行抽籤():
    if st.session_state.count >= 28: return
    
    # 目前要填入的目標位置標籤 (例如 "下1")
    target_label = 座位順序[st.session_state.count]
    
    # [保底邏輯保留] (略，同前幾版)
    # ... (為了簡潔，這裡假設正常抽籤，若要保底則依據 index 判斷)
    
    # 簡單示範：從池子抓人
    if st.session_state.pool:
        person = st.session_state.pool.pop(0)
        st.session_state.seats_map[target_label] = person
        st.session_state.count += 1

# 4. 側邊欄
with st.sidebar:
    if st.button("🎲 抽一位"): 執行抽籤()
    if st.button("🔄 重置"): st.session_state.clear(); st.rerun()

# 5. 主畫面：模擬你原本的表格排版
st.title("🏫 10B 實體座位表對照")

# 定義顯示函數，模擬表格的一個格子
def 畫格子(標籤):
    人名 = st.session_state.seats_map.get(標籤, "")
    if 人名:
        st.markdown(f'<div class="label-text">{標籤}</div><div class="seat normal">{人名}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="label-text">{標籤}</div><div class="seat" style="border:1px dashed #ccc;">待抽</div>', unsafe_allow_html=True)

# 模擬 10B 教室排版 (左 3 欄, 走道, 右 3 欄)
for row in range(5): # 假設 5 列
    c1, c2, c3, aisle, c4, c5, c6 = st.columns([1,1,1,0.5,1,1,1])
    
    # 這裡的邏輯可以根據你圖片的「下1、下2」具體編號來填入
    with c1: 畫格子(f"下{row*6 + 1}")
    with c2: 畫格子(f"下{row*6 + 2}")
    with c3: 畫格子(f"下{row*6 + 3}")
    with aisle: st.write("") # 走道
    with c4: 畫格子(f"下{row*6 + 4}")
    with c5: 畫格子(f"下{row*6 + 5}")
    with c6: 畫格子(f"下{row*6 + 6}")
