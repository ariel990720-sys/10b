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
    # ---  【在這裡修改名單】 ---
    
    #條件 1：視力不好且又是好朋友 (這組人會優先排在一起且坐前排)
    vip_partners = ["5吳瑾瑜", "9李忻嬡"] 
    
    #條件 2：單純視力需求 (保證在前三排，位置隨機)
    vision_only = ["1吳采軒", "21陳彥寧","25葉明寬"] 
    
    # 全班原始名單 (用於自動過濾)
    full_names = [
        "20黃柏瑞", "14郭承叡", "3吳亭葦", "7宋禹潔", "15張谷杉",
        "5吳瑾瑜", "9李忻懓", "29顏子旅", "10李維", "17張楚楚", "16陳永軍",
        "26劉苡樂", "1吳采軒", "18游朝翔", "22黃翔澤", "21陳彥寧", "25葉明寬",
        "11李沁恩", "24劉品佑", "23黃祺方", "2任為謙", "30黨宜安", "27謝欣妤",
        "13林霏", "8李羿宸", "4吳元希", "12洪軒平", "28簡向晨"
    ]

    # ---  自動排隊邏輯  ---
    # 先把視力需求名單洗牌
    random.shuffle(vision_only)
    
    # 合併所有優先前排的人
    front_pool = vip_partners + vision_only 
    
    # 找出剩下的人並隨機洗牌
    assigned_already
