import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정 (그래프 깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우 사용자용
plt.rcParams['axes.unicode_minus'] = False

st.title("📊 국세청 근로소득 데이터 분석기")
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try : 
    # 1. 인코딩 옵션 추가 (cp949 또는 euc-kr)
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("데이터가 성공적으로 로드되었습니다!")
    
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    st.subheader("항목별 분포 그래프")

    column_names = df.columns.tolist()
    selected_col = st.selectbox("분석할 항목을 선택하세요:", column_names)

    # 2. 그래프 그리기 (ax=ax 오타 수정)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df[selected_col].dropna(), ax=ax, color="#cc00ff")

    ax.set_title(f"[{selected_col}] 분포 확인")
    ax.set_xlabel(selected_col)
    ax.set_ylabel("빈도수")

    st.pyplot(fig)      

except FileNotFoundError: # 3. 에러 이름 수정
    st.error(f"'{file_path}' 데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요.") 
except Exception as e:
    st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")