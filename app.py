import streamlit as st
import random
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="10B 尋夢班 座位系統", layout="wide")

# CSS 美化：調整座位樣式，並讓禁區變成透明
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 16px; height: 3em; border-radius: 10px; margin-bottom: 10px; }
    .seat { border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 10px; font-weight: bold; min-height: 65px; display: flex; align-items: center; justify-content: center; }
    .normal { background-color: #e3f2fd; border: 2px solid #2196f3; color: #0d47a1; } /* 藍色 */
    .vision { background-color: #ffe0b2; border: 2px solid #fb8c00; color: #ef6c00; } /* 橘色 */
    .friend { background-color: #fce4ec; border: 2px solid #f06292; color: #ad1457; } /* 粉色 */
    .empty  { background-color: #f5f5f5; border: 2px dashed #bdbdbd; color: #bdbdbd; } /* 灰色虛線 */
    .blocked { visibility: hidden; } /* 💡 關鍵：這會讓格子佔位置，但完全隱形 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. 初始化狀態 (建立名單、洗牌)
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
    
    # 隨機洗牌
    st.session_state.pool = all_names.copy()
    random.shuffle(st.session_state.pool)
    
    # 建立 30 個空格 (6x5)
    st.session_state.seats = [None] * 30
    st.session_state.count = 0 
    
    # 定義哪幾個索引要留白 (0 是左上, 29 是右下)
    st.session_state.blocked_indices = [0, 29]

# 3. 核心抽籤函數
def draw_next():
    # 找下一個可以坐的位置 (跳過禁區與已有人的位子)
    idx = 0
    while idx < 30 and (idx in st.session_state.blocked_indices or st.session_state.seats[idx] is not None):
        idx += 1
    
    if idx >= 30: return

    vision_left = [p for p in st.session_state.vision_list if p not in st.session_state.seats]
    friends_left = [p for p in st.session_state.best_friends if p not in st.session_state.seats]
    
    # 檢查前三排 (索引 0-17) 剩下的空位
    available_front = [i for i in range(18) if i not in st.session_state.blocked_indices and st.session_state.seats[i] is None]
    
    chosen = None
    # 保底機制：位置快不夠了就強制抽特殊需求同學
    if idx < 18 and len(available_front) <= (len(vision_left) + len(friends_left)):
        chosen = friends_left[0] if friends_left else vision_left[0]
    else:
        # 正常隨機抽
        pool_left = [p for p in st.session_state.pool if p not in st.session_state.seats]
        if pool_left: chosen = pool_left[0]

    if chosen:
        st.session_state.seats[idx] = chosen
        st.session_state.count += 1
        
        # 好朋友連號：抽到一個，另一個自動坐隔壁
        if chosen in st.session_state.best_friends:
            other = [p for p in st.session_state.best_friends if p != chosen][0]
            if other not in st.session_state.seats:
                next_idx = idx + 1
                while next_idx < 30 and next_idx in st.session_state.blocked_indices:
                    next_idx += 1
                if next_idx < 30:
                    st.session_state.seats[next_idx] = other
                    st.session_state.count += 1

# 4. 側邊欄介面
with st.sidebar:
    st.header("⚙️ 控制中心")
    if st.session_state.count < 28:
        if st.button("🎲 抽出下一位"): draw_next()
        if st.button("⚡ 一次直接抽完"):
            while st.session_state.count < 28: draw_next()
    
    show_mark = st.checkbox("🔍 顯示特別安排標記", value=False)
    
    if st.button("🔄 重置並重新洗牌"):
        st.session_state.clear()
        st.rerun()

    if st.session_state.count > 0:
        st.write("---")
        df = pd.DataFrame({"位置": range(1, 31), "學生
