import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
import os
import platform

# --- [STEP 1] 한글 폰트 설정 (서버 환경 완벽 대응) ---
@st.cache_resource
def setup_korean_font():
    # 현재 운영체제 확인
    current_os = platform.system()
    
    if current_os == 'Windows':
        # 윈도우 환경
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif current_os == 'Darwin':
        # 맥 환경
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        # 스트림릿 클라우드(리눅스 서버) 환경
        # 1. 시스템에 설치된 나눔고딕 확인 (packages.txt 설치 시)
        nanum_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(nanum_path):
            fm.fontManager.addfont(nanum_path)
            plt.rcParams['font.family'] = 'NanumGothic'
        else:
            # 2. 만약 malgun.ttf 파일을 직접 업로드했을 경우 (파일명 소문자 주의)
            local_font = os.path.join(os.getcwd(), 'malgun.ttf')
            if os.path.exists(local_font):
                fm.fontManager.addfont(local_font)
                prop = fm.FontProperties(fname=local_font)
                plt.rcParams['font.family'] = prop.get_name()
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

# 폰트 설정 실행
setup_korean_font()

# --- [STEP 2] 앱 메인 화면 구성 ---
st.title("📊 국세청 근로소득 데이터 분석기")

# 파일 경로 (반려동물 데이터로 하실 경우 파일명을 "반려동물등록현황.csv"로 수정하세요)
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    # 데이터 로드 (한국 공공기관 데이터는 cp949 인코딩이 대부분입니다)
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("✅ 데이터가 성공적으로 로드되었습니다!")
    
    with st.expander("데이터 미리보기"):
        st.dataframe(df.head())

    st.subheader("📈 항목별 분포 그래프")

    # 수치형 데이터가 있는 열만 필터링 (그래프 그리기용)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_col = st.selectbox("분석할 항목을 선택하세요:", numeric_cols)

        # 그래프 생성
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df[selected_col].dropna(), ax=ax, color="#cc00ff", kde=True)

        # 제목 및 축 설정 (한글 폰트 적용됨)
        ax.set_title(f"[{selected_col}] 분포 확인", fontsize=15)
        ax.set_xlabel(selected_col)
        ax.set_ylabel("빈도수")

        st.pyplot(fig)
    else:
        st.warning("분석할 수 있는 수치형 데이터가 없습니다.")

except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}. GitHub에 파일이 있는지 확인하세요.") 
except Exception as e:
    st.error(f"❌ 데이터 처리 중 오류 발생: {e}")