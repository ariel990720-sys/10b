import streamlit as st
import random
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位系統", layout="wide")

# CSS 美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 16px; height: 3em; border-radius: 10px; margin-bottom: 10px; }
    .seat { border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 10px; font-weight: bold; min-height: 65px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
    .normal { background-color: #e3f2fd; border: 2px solid #2196f3; color: #0d47a1; }
    .vision { background-color: #ffe0b2; border: 2px solid #fb8c00; color: #ef6c00; }
    .friend { background-color: #fce4ec; border: 2px solid #f06292; color: #ad1457; }
    .empty  { background-color: #fdfdfd; border: 1px dashed #e0e0e0; }
    .blocked { visibility: hidden; } 
    
    /* 💡 隱藏上帝開關的 CSS：讓它幾乎透明，且標題點點幾乎看不見 */
    .stCheckbox { opacity: 0.02; } 
    .stCheckbox:hover { opacity: 0.1; }
    
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
    available_front = [i for i in range(18) if i not in st.session_state.blocked_indices and st.session_state.seats[i]
