import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
import os
import platform

# --- 폰트 설정 (로컬/클라우드 자동 대응) ---
@st.cache_resource
def set_korean_font():
    # 1. 리눅스(Streamlit Cloud) 환경일 때
    if platform.system() != 'Windows' and platform.system() != 'Darwin':
        # packages.txt를 통해 설치된 나눔 폰트 경로
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams['font.family'] = 'NanumGothic'
        else:
            # 만약 폰트 파일 malgun.ttf를 직접 올렸을 경우 대비
            local_font = os.path.join(os.getcwd(), 'malgun.ttf')
            if os.path.exists(local_font):
                fm.fontManager.addfont(local_font)
                prop = fm.FontProperties(fname=local_font)
                plt.rcParams['font.family'] = prop.get_name()
    
    # 2. 윈도우 환경일 때
    elif platform.system() == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
        
    # 3. 맥 환경일 때
    elif platform.system() == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'

    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

st.title("📊 국세청 근로소득 데이터 분석기")

# 파일 경로 (파일이 같은 폴더에 있어야 함)
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try : 
    # 데이터 로드 (cp949 인코딩)
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("데이터가 성공적으로 로드되었습니다!")
    
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    st.subheader("항목별 분포 그래프")

    # 수치형 데이터가 있는 열만 선택지로 제공
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_cols)

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df[selected_col].dropna(), ax=ax, color="#cc00ff", kde=True)

    ax.set_title(f"[{selected_col}] 분포 확인", fontsize=15)
    ax.set_xlabel(selected_col)
    ax.set_ylabel("빈도수")

    st.pyplot(fig)      

except FileNotFoundError:
    st.error(f"'{file_path}' 파일을 찾을 수 없습니다. GitHub에 파일이 업로드되었는지 확인해주세요.") 
except Exception as e:
    st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")