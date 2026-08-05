# streamlit webapp의 pages 경로 밑에 서브 페이지로 다음을 생성해주세요.
# 머신러닝의 개념에 대해 학습할 콘텐츠 생성
# 간단하게 머신러닝의 개념을 실습할 수 있는 시뮬레이터 포함(mock data를 생성해서(분류 데이터) 직접 실습하도록 함)

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.linear_model import SGDClassifier
from sklearn.inspection import DecisionBoundaryDisplay

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝의 개념 학습",
    page_icon="🤖",
    layout="wide"
)

# 2. 타이틀 및 소개
st.title("🤖 0. 머신러닝의 개념 이해하기")
st.markdown("""
머신러닝(Machine Learning)은 사람이 직접 규칙을 프로그래밍하는 대신, **컴퓨터가 데이터로부터 스스로 규칙을 학습**하도록 하는 기술입니다.
""")

st.write("---")

# 3. 이론 학습 콘텐츠 (Tab 구조 활용)
tab1, tab2 = st.tabs(["📚 머신러닝이란?", "🎯 분류(Classification) 개념"])

with tab1:
    st.subheader("💡 전통적 프로그래밍 vs 머신러닝")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💻 **전통적 프로그래밍**\n\n`데이터` + `규칙(코드)` ➡️ **[해답]**")
    with col2:
        st.success("🧠 **머신러닝**\n\n`데이터` + `해답(레이블)` ➡️ **[규칙(모델)]**")
        
    st.markdown("""
    *   **핵심 요약:** 머신러닝은 수많은 데이터 안에서 인간이 미처 발견하지 못한 복잡한 패턴과 규칙을 수학적 알고리즘으로 찾아냅니다.
    """)

with tab2:
    st.subheader("🎯 이진 분류(Binary Classification)란?")
    st.markdown("""
    *   주어진 데이터를 바탕으로 두 개의 그룹(예: **0 또는 1**, **양성 또는 음성**) 중 하나로 정답을 맞히는 문제입니다.
    *   **예시:** 스팸 메일 차단(스팸 / 정상), 이메일 분류, 암 여부 진단 등
    *   아래 시뮬레이터에서 컴퓨터가 데이터들 사이의 **정확한 경계선(Decision Boundary)**을 어떻게 찾아나가는지 직접 확인해보세요!
    """)

st.write("---")

# 4. 실시간 머신러닝 시뮬레이터 (Mock Data 활용)
st.header("🎮 실시간 머신러닝 시뮬레이터")
st.caption("인공데이터(Mock Data)를 생성하고 알고리즘이 경계선을 학습하는 과정을 시뮬레이션합니다.")

# 사이드바 / 컨트롤러 설정
st.sidebar.header("⚙️ 시뮬레이터 설정")

# 데이터 형태 선택
data_type = st.sidebar.selectbox(
    "데이터 분포 형태",
    ["선형 분리형 (Blobs)", "곡선 분리형 (Moons)"]
)

# 하이퍼파라미터 조절 스라이더
n_samples = st.sidebar.slider("데이터 개수 (샘플 수)", min_value=50, max_value=300, value=150, step=50)
learning_rate = st.sidebar.select_slider(
    "학습률 (Learning Rate)", 
    options=[0.001, 0.01, 0.1, 1.0], 
    value=0.1
)
max_iter = st.sidebar.slider("학습 반복 횟수 (Epochs)", min_value=1, max_value=50, value=5, step=1)

# [Mock Data 생성]
@st.cache_data(show_spinner=False)
def generate_mock_data(data_type, n_samples):
    if data_type == "선형 분리형 (Blobs)":
        X, y = make_blobs(n_samples=n_samples, centers=2, random_state=42, cluster_std=1.5)
    else:
        X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=42)
    return X, y

X, y = generate_mock_data(data_type, n_samples)

# [머신러닝 모델 학습]
# 시각적인 변화를 뚜렷하게 보기 위해 경사하강법 기반의 SGDClassifier 사용
model = SGDClassifier(
    loss="log_loss", 
    learning_rate="constant", 
    eta0=learning_rate, 
    max_iter=max_iter, 
    random_state=42
)
model.fit(X, y)

# 모델 정확도 평가
accuracy = model.score(X, y) * 100

# 결과 레이아웃 구성
col_chart, col_metrics = st.columns([2, 1])

with col_chart:
    # 데이터 및 결정 경계 시각화
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # 학습된 결정 경계 그리기
    try:
        DecisionBoundaryDisplay.from_estimator(
            model, X, grid_resolution=200, response_method="predict",
            cmap="RdYlBu", alpha=0.3, ax=ax
        )
    except Exception:
        pass # 초반 에러 방지
        
    # 데이터 산점도 그리기
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap="RdYlBu", edgecolor="k", s=40)
    ax.set_title(f"모델의 데이터 분류 패턴 ({data_type})", fontsize=11)
    ax.set_xlabel("특성 X1")
    ax.set_ylabel("특성 X2")
    
    st.pyplot(fig)

with col_metrics:
    st.subheader("📊 학습 결과 리포트")
    st.metric(label="현재 모델 정확도 (Accuracy)", value=f"{accuracy:.1f} %")
    
    # 상태 메시지 제공
    if accuracy >= 90:
        st.success("🎯 모델이 데이터를 아주 잘 분류하고 있습니다!")
    elif accuracy >= 70:
        st.warning("⚠️ 조금 더 학습이 필요하거나 파라미터 조절이 필요합니다.")
    else:
        st.error("❌ 정답률이 낮습니다. 반복 횟수를 늘리거나 데이터 형태를 확인하세요.")

    # 학습 데이터 프레임 미리보기
    st.markdown("**생성된 인공 데이터(일부)**")
    df = pd.DataFrame(X, columns=["특성_X1", "특성_X2"])
    df["정답_Label"] = y
    st.dataframe(df.head(5), use_container_width=True)

# 💡 실습 가이드라인 제공
st.info("""
💡 **이렇게 실습해보세요!**
1. 왼쪽 사이드바에서 **'학습 반복 횟수(Epochs)'를 1부터 천천히 늘려보세요.** 반복할수록 배경 색상(결정 경계)이 정답 데이터들을 올바르게 갈라놓기 시작합니다.
2. 데이터 분포를 **'곡선 분리형 (Moons)'**으로 바꾸어 보세요. 현재 사용된 선형 모델로는 완벽하게 분리하기 어렵다는 점을 통해 **'더 복잡한 머신러닝 알고리즘(딥러닝 등)'의 필요성**을 체감할 수 있습니다.
""")