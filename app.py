import streamlit as st
import random

# 1. 網頁基本設定
st.set_page_config(page_title="10B 座位抽籤系統", layout="wide")

# 隱藏 Streamlit 預設選單與頁尾
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {max-width: 1200px; margin: 0 auto;}
    </style>
""", unsafe_allow_html=True)

st.title("🏫 10B 教室座位圖")

# 2. 完整名單
names = [
    "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
    "5吳瑾瑜", "9李忻懓", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
    "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
    "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
    "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
]

# 3. 抽籤按鈕
if st.button('🎲 開始隨機分配座位'):
    random.shuffle(names)
    st.balloons() # 噴氣球

    # --- 視覺元件：黑板 ---
    st.markdown("""
        <div style="background-color: #1e3d2f; color: white; padding: 20px; text-align: center; border-radius: 10px; border: 5px solid #5d4037; font-size: 28px; font-weight: bold; width: 60%; margin: 20px auto 50px auto; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
            🎬 黑 板 ( 正 前 方 )
        </div>
    """, unsafe_allow_html=True)

    # 4. 座位佈局設定 (5, 6, 6, 6, 5)
    layout = [5, 6, 6, 6, 5]
    current = 0
    
    # 依照佈局繪製座位
    for row_idx, count in enumerate(layout):
        # 建立欄位，並加上中間間隔縮排的效果
        cols = st.columns(count)
        row_people = names[current : current + count]
        current += count
        
        for i, person in enumerate(row_people):
            with cols[i]:
                # 自定義座位卡片樣式
                st.markdown(f"""
                    <div style="background-color: #e3f2fd; border: 2px solid #2196f3; border-radius: 8px; padding: 15px 5px; text-align: center; margin-bottom: 20px; color: #0d47a1; font-weight: bold; font-size: 18px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                        {person}
                    </div>
                """, unsafe_allow_html=True)

    # 註：原本下方的「抽籤完成」文字已依照要求刪除
