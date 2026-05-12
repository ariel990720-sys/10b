import streamlit as st
import random
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位系統", layout="wide")

# CSS 美化
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 16px; height: 3em; border-radius: 10px; margin-bottom: 10px; }
    .seat { border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 10px; font-weight: bold; min-height: 65px; display: flex; align-items: center; justify-content: center; }
    .normal { background-color: #e3f2fd; border: 2px solid #2196f3; color: #0d47a1; }
    .vision { background-color: #ffe0b2; border: 2px solid #fb8c00; color: #ef6c00; }
    .friend { background-color: #fce4ec; border: 2px solid #f06292; color: #ad1457; }
    .empty  { background-color: #f5f5f5; border: 2px dashed #bdbdbd; color: #bdbdbd; }
    .blocked { background-color: #eeeeee; border: 1px solid #e0e0e0; color: #9e9e9e; font-size: 12px; }
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
    
    # 所有人公平洗牌
    st.session_state.pool = all_names.copy()
    random.shuffle(st.session_state.pool)
    
    # 初始化 30 個格子 (6 欄 * 5 列)
    st.session_state.seats = [None] * 30
    st.session_state.count = 0 
    
    # 定義禁區索引：0 (左上角), 29 (右下角)
    st.session_state.blocked_indices = [0, 29]

# 3. 核心抽籤邏輯 (加入 6x5 邏輯與禁區跳過)
def draw_next():
    # 找出下一個「不是禁區」且「還沒坐人」的位置索引
    curr_idx = 0
    while curr_idx < 30 and (curr_idx in st.session_state.blocked_indices or st.session_state.seats[curr_idx] is not None):
        curr_idx += 1
    
    if curr_idx >= 30: return

    # 判斷保底邏輯：前三排為 index 0~17 (即便有禁區，我們仍以前三排作為視力組防線)
    vision_left = [p for p in st.session_state.vision_list if p not in st.session_state.seats]
    friends_left = [p for p in st.session_state.best_friends if p not in st.session_state.seats]
    
    # 剩下還能坐人的前三排位置數 (扣除禁區與已坐的人)
    available_front = [i for i in range(18) if i not in st.session_state.blocked_indices and st.session_state.seats[i] is None]
    
    chosen = None
    # 如果前排剩餘位置剛好等於需要保底的人數
    if curr_idx < 18 and len(available_front) <= (len(vision_left) + len(friends_left)):
        chosen = friends_left[0] if friends_left else vision_left[0]
    else:
        pool_left = [p for p in st.session_state.pool if p not in st.session_state.seats]
        if pool_left: chosen = pool_left[0]

    if chosen:
        st.session_state.seats[curr_idx] = chosen
        st.session_state.count += 1
        
        # 好友連帶邏輯 (自動填入下一個非禁區位置)
        if chosen in st.session_state.best_friends:
            other = [p for p in st.session_state.best_friends if p != chosen][0]
            if other not in st.session_state.seats:
                next_idx = curr_idx + 1
                while next_idx < 30 and next_idx in st.session_state.blocked_indices:
                    next_idx += 1
                if next_idx < 30:
                    st.session_state.seats[next_idx] = other
                    st.session_state.count += 1

# 4. 側邊控制面板
with st.sidebar:
    st.header("⚙️ 控制中心")
    if st.session_state.count < 28:
        if st.button("🎲 抽一位"): draw_next()
        if st.button("⚡ 全部抽完"):
            while st.session_state.count < 28: draw_next()
    
    show_mark = st.checkbox("🔍 顯示特殊安排標記")
    
    if st.button("🔄 重置系統"):
        st.session_state.clear()
        st.rerun()

    if st.session_state.count > 0:
        st.write("---")
        st.subheader("💾 存檔與導出")
        df = pd.DataFrame({"位置": range(1, 31), "學生": st.session_state.seats})
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載座位表 (CSV)", csv, "10B_座位表.csv", "text/csv")

# 5. 主畫面：6 x 5 佈局渲染
st.title("🏫 10B 尋夢班 座位系統 (6×5 版)")
st.markdown('<div style="background-color:#1e3d2f;color:white;text-align:center;padding:10px;border-radius:10px;margin-bottom:30px;">🎬 黑板 (前方)</div>', unsafe_allow_html=True)

# 採用 5 列，每列 6 個格子的方式渲染
for row in range(5):
    cols = st.columns(6)
    for col in range(6):
        idx = row * 6 + col
        with cols[col]:
            if idx in st.session_state.blocked_indices:
                st.markdown('<div class="seat blocked">🚫 禁區</div>', unsafe_allow_html=True)
            else:
                name = st.session_state.seats[idx]
                if name:
                    style = "normal"
                    if show_mark:
                        if name in st.session_state.vision_list: style = "vision"
                        if name in st.session_state.best_friends: style = "friend"
                    st.markdown(f'<div class="seat {style}">{name}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="seat empty">{idx + 1}</div>', unsafe_allow_html=True)

if st.session_state.count >= 28:
    st.balloons()
