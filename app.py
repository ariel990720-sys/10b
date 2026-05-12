import streamlit as st
import random
import pandas as pd  # 用於資料處理與下載

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位系統", layout="wide")

# CSS 美化 (保留所有顏色與樣式)
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 16px; height: 3em; border-radius: 10px; margin-bottom: 10px; }
    .seat { border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 10px; font-weight: bold; min-height: 60px; }
    .normal { background-color: #e3f2fd; border: 2px solid #2196f3; color: #0d47a1; }
    .vision { background-color: #ffe0b2; border: 2px solid #fb8c00; color: #ef6c00; }
    .friend { background-color: #fce4ec; border: 2px solid #f06292; color: #ad1457; }
    .empty  { background-color: #f5f5f5; border: 2px dashed #bdbdbd; color: #bdbdbd; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. 初始化狀態
if 'seats' not in st.session_state:
    st.session_state.vision_list = ["1吳采軒", "21陳彥寧", "25葉明寬"]
    st.session_state.friend_list = ["5吳瑾瑜", "9李忻嬡"]
    
    all_names = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "9李忻嬡", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
    ]
    
    st.session_state.pool = all_names.copy()
    random.shuffle(st.session_state.pool)
    st.session_state.seats = [None] * 28
    st.session_state.count = 0

# 3. 抽籤邏輯 (保留保底與好友連號)
def draw_next():
    idx = st.session_state.count
    if idx >= 28: return
    
    vision_left = [p for p in st.session_state.vision_list if p not in st.session_state.seats]
    friends_left = [p for p in st.session_state.friend_list if p not in st.session_state.seats]
    
    seats_left_front = 17 - idx
    needs_count = len(vision_left) + len(friends_left)
    
    chosen = None
    if idx < 17 and seats_left_front <= needs_count:
        chosen = friends_left[0] if friends_left else vision_left[0]
    else:
        pool_left = [p for p in st.session_state.pool if p not in st.session_state.seats]
        if pool_left: chosen = pool_left[0]

    if chosen:
        st.session_state.seats[idx] = chosen
        st.session_state.count += 1
        # 好友連號
        if chosen in st.session_state.friend_list:
            other = [p for p in st.session_state.friend_list if p != chosen][0]
            if other not in st.session_state.seats and st.session_state.count < 17:
                st.session_state.seats[st.session_state.count] = other
                st.session_state.count += 1

# 4. 側邊控制面板
with st.sidebar:
    st.header("⚙️ 控制面板")
    if st.session_state.count < 28:
        if st.button("🎲 抽一位"): draw_next()
        if st.button("⚡ 全部抽完"):
            while st.session_state.count < 28: draw_next()
    
    show_mark = st.checkbox("🔍 顯示特殊安排標記")
    
    if st.button("🔄 重置系統"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

    # --- 新功能：下載與保留存檔 ---
    if st.session_state.count > 0:
        st.write("---")
        st.subheader("💾 存檔功能")
        
        # 整理資料
        df = pd.DataFrame({
            "位置": [i+1 for i in range(28)],
            "學生姓名": st.session_state.seats
        })
        
        # 下載按鈕 (CSV)
        csv = df.to_csv(index=False).encode('utf-8-sig') # utf-8-sig 讓 Excel 開啟不亂碼
        st.download_button(
            label="📥 下載座位表 (Excel/CSV)",
            data=csv,
            file_name='10B_座位表.csv',
            mime='text/csv',
        )
        
        # 文字預覽 (方便快速複製)
        with st.expander("📝 查看文字清單"):
            text_list = ""
            for i, name in enumerate(st.session_state.seats):
                if name: text_list += f"{i+1}號: {name}\n"
            st.text_area("複製下方文字", text_list, height=200)

# 5. 主畫面座位圖
st.title("🏫 10B 尋夢班 座位系統")
st.markdown('<div style="background-color:#1e3d2f;color:white;text-align:center;padding:10px;border-radius:10px;margin-bottom:30px;">🎬 黑板 (前方)</div>', unsafe_allow_html=True)

layout = [5, 6, 6, 6, 5]
curr_idx = 0
for row_count in layout:
    cols = st.columns(row_count)
    for i in range(row_count):
        name = st.session_state.seats[curr_idx]
        with cols[i]:
            if name:
                style = "normal"
                if show_mark:
                    if name in st.session_state.vision_list: style = "vision"
                    if name in st.session_state.friend_list: style = "friend"
                st.markdown(f'<div class="seat {style}">{name}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="seat empty">{curr_idx + 1}</div>', unsafe_allow_html=True)
        curr_idx += 1

if st.session_state.count >= 28:
    st.balloons()
