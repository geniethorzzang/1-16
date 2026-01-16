import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
import os
import platform

# --- [1] 한글 폰트 설정 (환경 자동 감지) ---
@st.cache_resource
def setup_korean_font():
    # 윈도우 환경
    if platform.system() == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    # 맥 환경
    elif platform.system() == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    # 리눅스(스트림릿 클라우드) 환경
    else:
        # 1. 시스템에 나눔폰트가 설치되어 있는지 확인 (packages.txt 설치 시)
        nanum_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(nanum_path):
            fm.fontManager.addfont(nanum_path)
            plt.rcParams['font.family'] = 'NanumGothic'
        else:
            # 2. 혹시나 폰트 파일(malgun.ttf)을 직접 올렸을 경우 대비
            local_font = os.path.join(os.getcwd(), 'malgun.ttf')
            if os.path.exists(local_font):
                fm.fontManager.addfont(local_font)
                prop = fm.FontProperties(fname=local_font)
                plt.rcParams['font.family'] = prop.get_name()

    plt.rcParams['axes.unicode_minus'] = False

setup_korean_font()

# --- [2] 메인 앱 부분 ---
st.title("📊 데이터 통합 분석기")

# 파일 경로 (현재 사용중인 파일명으로 확인해주세요)
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

if os.path.exists(file_path):
    try:
        # 데이터 불러오기
        df = pd.read_csv(file_path, encoding='cp949')
        st.success("✅ 데이터가 성공적으로 로드되었습니다!")

        # --- 미리보기 기능 (다시 추가함!) ---
        st.subheader("🔍 데이터 미리보기")
        st.dataframe(df.head(10))  # 상위 10개 행 표시

        # --- 데이터 요약 정보 ---
        with st.expander("데이터 전체 정보 보기"):
            st.write(df.describe())

        # --- 그래프 분석 ---
        st.subheader("📈 통계 분포 그래프")
        
        # 숫자 데이터가 있는 열만 선택지로 제공
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_cols)

            # 그래프 그리기
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df[selected_col].dropna(), ax=ax, color="#cc00ff", kde=True)

            # 제목 및 축 설정
            ax.set_title(f"[{selected_col}] 데이터 분포 확인", fontsize=15)
            ax.set_xlabel(selected_col)
            ax.set_ylabel("빈도수")

            st.pyplot(fig)
        else:
            st.warning("분석 가능한 수치형 데이터가 없습니다.")

    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
else:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")