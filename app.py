import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
import platform
import os

# --- [강력한 한글 폰트 설정] ---
def apply_font():
    try:
        if platform.system() == 'Windows':
            plt.rcParams['font.family'] = 'Malgun Gothic'
        elif platform.system() == 'Darwin':
            plt.rcParams['font.family'] = 'AppleGothic'
        else:
            # 스트림릿 클라우드(리눅스) 환경
            # 1. 시스템 폰트 경로 직접 지정
            path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
            if os.path.exists(path):
                # 폰트 추가 및 이름 설정
                font_name = fm.FontProperties(fname=path).get_name()
                plt.rc('font', family=font_name)
            else:
                # 폰트가 정말 없을 경우, 에러를 내지 않고 기본 폰트 사용
                st.warning("나눔 폰트를 찾을 수 없어 기본 폰트로 표시합니다. (packages.txt 확인 필요)")
    except Exception as e:
        st.error(f"폰트 설정 중 오류 발생: {e}")

    plt.rcParams['axes.unicode_minus'] = False

apply_font()

# --- [앱 메인 로직] ---
st.title("📊 국세청 근로소득 데이터 분석기")

file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path, encoding='cp949')
        st.success("✅ 데이터 로드 성공!")

        st.subheader("데이터 미리보기")
        st.dataframe(df.head())

        # 수치형 컬럼 선택
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("분석할 항목 선택:", numeric_cols)

            # 그래프 그리기
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df[selected_col].dropna(), ax=ax, color="#cc00ff", kde=True)
            
            # 제목에 한글이 들어가면 깨질 수 있으므로 영어로 먼저 테스트해보세요
            ax.set_title(f"Distribution of {selected_col}", fontsize=15)
            
            st.pyplot(fig)
        else:
            st.warning("분석 가능한 수치형 데이터가 없습니다.")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")