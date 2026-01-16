import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
import os

# --- [최종 병기: 시스템 폰트 강제 추출] ---
@st.cache_resource
def force_korean_font():
    # 1. 일단 시스템에 있는 모든 폰트 목록을 가져옵니다.
    font_list = fm.findSystemFonts()
    
    # 2. 그 중에서 이름에 'Nanum', 'Gothic', 'Malgun', 'Apple'이 들어간 걸 하나 찾습니다.
    target_font = None
    for f in font_list:
        fname = f.lower()
        if 'nanum' in fname or 'gothic' in fname or 'malgun' in fname:
            target_font = f
            break
            
    # 3. 찾은 폰트가 있다면 적용하고, 없으면 에러 없이 영어로만 나오게 합니다.
    if target_font:
        font_name = fm.FontProperties(fname=target_font).get_name()
        plt.rc('font', family=font_name)
    
    plt.rcParams['axes.unicode_minus'] = False

force_korean_font()

# --- [앱 메인 로직] ---
st.title("📊 국세청 데이터 분석기")

# 파일명 정확히 확인해주세요!
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("데이터 로드 성공!")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("항목 선택:", numeric_cols)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col].dropna(), ax=ax, color="#cc00ff")
        
        # 제목을 영어로 설정 (한글 폰트가 안 깔려도 에러가 안 나게 하기 위함)
        ax.set_title(f"Graph of {selected_col}")
        st.pyplot(fig)
except Exception as e:
    st.error(f"오류가 났어요: {e}")