import streamlit as st
import random
import time

# 設定網頁標題與排版
st.set_page_config(page_title="夏1_2 隨機座位抽籤", layout="wide")

st.title("🎲 夏1_2 班級隨機座位系統")
st.write("點擊下方按鈕開始隨機分配座位")

# 1. 完整名單
names = [
    "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
    "5吳瑾瑜", "9李忻懓", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
    "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
    "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
    "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
]

# 2. 抽籤按鈕
if st.button('🔥 開始隨機抽籤'):
    with st.spinner('正在洗牌中...'):
        time.sleep(1.5) # 增加緊張感
        random.shuffle(names)
    
    st.balloons() # 成功後噴出氣球特效
    
    # 3. 座位佈局 (5, 6, 6, 6, 5)
    layout = [5, 6, 6, 6, 5]
    current = 0
    
    st.markdown("---")
    st.header("🏫 教室座位圖 (講台在上方)")
    
    for i, count in enumerate(layout):
        row_people = names[current : current + count]
        current += count
        
        # 使用 Streamlit 的欄位功能 (columns) 讓座位橫向排列
        cols = st.columns(count)
        for idx, person in enumerate(row_people):
            with cols[idx]:
                # 建立一個漂亮的卡片樣式
                st.info(f"**{person}**")
    
    st.success("抽籤完成！祝大家這學期坐得開心。")
