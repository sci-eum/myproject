import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# 1. 페이지 설정 및 로그인 검증
st.set_page_config(page_title="머신러닝 형성평가", page_icon="📝", layout="centered")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🔒 로그인한 사용자만 형성평가에 응시할 수 있습니다. 메인 화면(app.py)으로 이동해 로그인해주세요.")
    st.stop()

userid = st.session_state["userid"]

st.title("📝 3. 머신러닝 개념 형성평가")
st.write(f"현재 응시자 계정: **{userid}**")
st.markdown("총 10문항의 5지선다형 문제입니다. 시험 점수 결과는 데이터베이스에 회차별로 안전하게 누적 기록됩니다.")

st.write("---")

# 2. 문제 데이터셋 매핑 (번호 정수 매핑: ①=1, ②=2, ③=3, ④=4, ⑤=5)
quiz_data = [
    {
        "num": 1, "correct": 3,
        "question": "1. 다음 중 '전통적인 프로그래밍'과 '머신러닝'의 가장 큰 차이점을 올바르게 설명한 것은 무엇인가요?",
        "options": ["① 전통적 프로그래밍은 컴퓨터가 스스로 규칙을 찾아낸다.", "② 머신러닝은 인간이 직접 모든 조건문(If-Else)을 작성해야 한다.", "③ 전통적 프로그래밍은 데이터와 규칙을 입력하여 해답을 얻고, 머신러닝은 데이터와 해답을 입력하여 규칙을 학습한다.", "④ 머신러닝은 데이터를 전혀 필요로 하지 않는다.", "⑤ 두 방식은 작동 원리와 구조가 완벽히 동일하다."],
        "hint": "전통적인 방식은 사람이 만든 '규칙'이 먼저 들어가고, 머신러닝은 데이터로부터 '규칙'을 뽑아냅니다.",
        "explanation": "전통적 프로그래밍은 사람이 규칙을 제공하지만, 머신러닝은 데이터와 정답을 보고 알고리즘이 스스로 규칙(모델)을 찾아냅니다."
    },
    {
        "num": 2, "correct": 2,
        "question": "2. 머신러닝의 주요 유형 중, 데이터에 대한 '정답(Label)'이 주어지지 않은 상태에서 데이터의 숨겨진 패턴이나 구조를 찾아내는 학습 방법은 무엇인가요?",
        "options": ["① 지도 학습 (Supervised Learning)", "② 비지도 학습 (Unsupervised Learning)", "③ 강화 학습 (Reinforcement Learning)", "④ 지도 강화 학습 (Supervised Reinforcement Learning)", "⑤ 전이 학습 (Transfer Learning)"],
        "hint": "선생님(정답 레이블)의 가이드 없이 데이터 자체의 유사성만을 이용해 학습하는 방법입니다.",
        "explanation": "정답(레이블)이 없는 데이터로부터 군집화(Clustering)나 차원 축소 등을 수행하는 방식을 비지도 학습이라고 합니다."
    },
    {
        "num": 3, "correct": 4,
        "question": "3. 주어진 데이터를 기반으로 이메일이 '스팸'인지 '정상'인지 혹은 유한한 종류의 정답 중 하나를 예측하는 머신러닝 문제를 무엇이라고 하나요?",
        "options": ["① 회귀 (Regression)", "② 군집화 (Clustering)", "③ 차원 축소 (Dimension Reduction)", "④ 분류 (Classification)", "⑤ 연관 규칙 학습 (Association Rule Learning)"],
        "hint": "데이터들을 서로 다른 그룹(카테고리)으로 '나누는' 작업입니다.",
        "explanation": "데이터를 정해진 몇 개의 클래스(범주) 중 하나로 예측하여 할당하는 문제를 분류(Classification)라고 합니다."
    },
    {
        "num": 4, "correct": 1,
        "question": "4. 연속적인 숫자(예: 내년도 주택 가격, 내일의 기온 등)를 예측하는 머신러닝 문제를 무엇이라고 하나요?",
        "options": ["① 회귀 (Regression)", "② 분류 (Classification)", "③ 군집화 (Clustering)", "④ 이상 탐지 (Anomaly Detection)", "⑤ 텍스트 마이닝 (Text Mining)"],
        "hint": "카테고리가 아니라 '연속된 값' 혹은 '수치' 자체를 맞히는 지도학습의 일종입니다.",
        "explanation": "연속적인 수치형 타겟 변수를 예측하는 머신러닝 모델의 형태를 회귀(Regression)라고 합니다."
    },
    {
        "num": 5, "correct": 2,
        "question": "5. 모델이 학습 데이터에 너무 과도하게 맞춰져서, 학습 데이터는 잘 맞히지만 새로운 실제 데이터(테스트 데이터)에서는 엉뚱한 예측을 하는 현상을 뜻하는 용어는 무엇인가요?",
        "options": ["① 과소적합 (Underfitting)", "② 과적합 (Overfitting)", "③ 최적화 (Optimization)", "④ 정규화 (Normalization)", "⑤ 일반화 (Generalization)"],
        "hint": "데이터에 '과하게(Over)' 들어맞았다는 의미의 단어입니다.",
        "explanation": "학습 데이터에만 지나치게 최적화되어 실제 새로운 데이터에 대한 예측 성능이 떨어지는 현상을 과적합(Overfitting)이라고 합니다."
    },
    {
        "num": 6, "correct": 3,
        "question": "6. 다음 중 머신러닝에서 알고리즘이 자동으로 학습하지 못하여, 사용자가 직접 수동으로 설정해주어야 하는 주요 제어 매개변수를 뜻하는 용어는 무엇인가요?",
        "options": ["① 가중치 (Weights)", "② 편향 (Bias)", "③ 하이퍼파라미터 (Hyperparameter)", "④ 손실 함수 (Loss Function)", "⑤ 특징 변수 (Features)"],
        "hint": "시뮬레이터 사이드바에서 개발자가 직접 조절했던 '학습률'이나 '반복 횟수' 같은 값들을 말합니다.",
        "explanation": "모델이 스스로 학습하는 파라미터(가중치 등)와 달리, 사람이 직접 외부에서 지정해 주는 설정을 하이퍼파라미터라고 합니다."
    },
    {
        "num": 7, "correct": 2,
        "question": "7. 비지도 학습의 대표적인 예시로, 유사한 특성을 가진 데이터들을 하나의 그룹으로 묶어주는 기술은 무엇인가요?",
        "options": ["① 선형 회귀 (Linear Regression)", "② 군집화 (Clustering)", "③ 로지스틱 회귀 (Logistic Regression)", "④ 의사결정나무 (Decision Tree)", "⑤ 신경망 (Neural Network)"],
        "hint": "영어로 '포도송이'나 '무리'를 뜻하는 단어에서 유래했습니다.",
        "explanation": "별도의 정답 레이블 없이 데이터의 특징 공간상 거리를 기준으로 유사한 그룹을 형성하는 기법을 군집화(Clustering)라고 합니다."
    },
    {
        "num": 8, "correct": 3,
        "question": "8. 에이전트(Agent)가 환경과 상호작용하며 어떤 행동을 했을 때, 그 행동의 결과에 따라 '보상(Reward)' 또는 '벌점'을 부여하여 올바른 행동 방향을 학습하게 하는 방식은 무엇인가요?",
        "options": ["① 지도 학습 (Supervised Learning)", "② 비지도 학습 (Unsupervised Learning)", "③ 강화 학습 (Reinforcement Learning)", "④ 자율 학습 (Self-learning)", "⑤ 배치 학습 (Batch Learning)"],
        "hint": "알파고(AlphaGo)가 바둑을 이기기 위해 스스로 대국을 반복하며 '승리'라는 보상을 얻기 위해 학습한 방식입니다.",
        "explanation": "시시각각 변하는 환경에서 보상을 극대화하는 방향으로 행동 정책을 학습하는 기법을 강화 학습(Reinforcement Learning)이라고 합니다."
    },
    {
        "num": 9, "correct": 2,
        "question": "9. 머신러닝 시뮬레이터에서 보았던 개념으로, 예측값과 실제 정답 사이의 차이(오류)를 계산하여 모델이 얼마나 잘못하고 있는지를 숫자로 나타내는 함수는 무엇인가요?",
        "options": ["① 활성화 함수 (Activation Function)", "② 손실 함수 (Loss Function)", "③ 목적 함수 (Objective Function)", "④ 성능 함수 (Performance Function)", "⑤ 선형 함수 (Linear Function)"],
        "hint": "영어로 'Loss' 또는 'Cost' 함수라고 표현하며, 이 값이 0에 가까워질수록 좋은 모델입니다.",
        "explanation": "모델의 예측값과 실제 정답의 오차를 정의하는 함수로, 머신러닝 학습의 목표는 이 손실 함수의 값을 최소화하는 것입니다."
    },
    {
        "num": 10, "correct": 3,
        "question": "10. 머신러닝 모델의 성능을 평가할 때, 전체 데이터 중 모델이 올바르게 맞춘 데이터의 비율을 나타내는 지표는 무엇인가요?",
        "options": ["① 정밀도 (Precision)", "② 재현율 (Recall)", "③ 정확도 (Accuracy)", "④ F1-스코어 (F1-Score)", "⑤ 에러율 (Error Rate)"],
        "hint": "시뮬레이터 결과 리포트에서 몇 %의 확률로 맞췄는지 보여주었던 가장 직관적인 평가 지표입니다.",
        "explanation": "전체 예측 건수 중 정답을 맞춘 건수의 비율을 나타내는 정량적 평가지표를 정확도(Accuracy)라고 합니다."
    }
]

# 사용자가 입력한 번호를 리스트로 받아오기 위한 변수 사전 정의
user_answers = {}

# 3. 루프를 돌며 문제 화면에 표시
for idx, item in enumerate(quiz_data):
    st.subheader(item["question"])
    
    # 5지선다 라디오 입력 박스
    choice = st.radio(
        f"정답 선택 (문항 {idx+1})",
        options=item["options"],
        index=None,
        key=f"quiz_choice_{idx}"
    )
    
    # 선택값 매핑 처리 (문자열 보기가 선택되었을 경우 인덱스 번호 + 1로 숫자를 확보해둠)
    if choice:
        selected_num = item["options"].index(choice) + 1
        user_answers[f"m{idx+1}"] = selected_num
    else:
        user_answers[f"m{idx+1}"] = 0 # 미입력 시 0번으로 초기화 처리
        
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("💡 힌트 보기"):
            st.info(item["hint"])
    with col2:
        with st.expander("🔓 정답 및 해설 보기"):
            st.success(f"**정답 정수 값**: {item['correct']}번 문항")
            st.markdown(f"**해설**: {item['explanation']}")
    st.write("---")

# 4. 제출 버튼 및 DB 데이터 적재 처리
if st.button("🚀 시험 답안 최종 제출 및 DB 저장", type="primary"):
    # 채점 프로세스 가동
    score = 0
    for idx, item in enumerate(quiz_data):
        if user_answers[f"m{idx+1}"] == item["correct"]:
            score += 10 # 문제당 10점 처리하여 100점 만점 설계
            
    # DB 저장 쿼리 빌드
    conn = sqlite3.connect('myproject.db')
    cursor = conn.cursor()
    
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query = """
        INSERT INTO learning_history (
            userid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(query, (
        userid, 
        user_answers["m1"], user_answers["m2"], user_answers["m3"], user_answers["m4"], user_answers["m5"],
        user_answers["m6"], user_answers["m7"], user_answers["m8"], user_answers["m9"], user_answers["m10"],
        score, now_time
    ))
    
    conn.commit()
    conn.close()
    
    st.balloons()
    st.success(f"📊 제출 완료! 이번 회차 점수는 **{score}점**입니다. 데이터베이스(myproject.db)에 성공적으로 저장되었습니다.")

# 5. 기존 응시 이력 데이터 이력 확인용 확장 테이블 로드
st.write("---")
st.subheader("📋 나의 다회차 형성평가 응시 기록")

conn = sqlite3.connect('myproject.db')
query_select = "SELECT created_at, score, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10 FROM learning_history WHERE userid = ? ORDER BY id DESC"
df_history = pd.read_sql_query(query_select, conn, params=(userid,))
conn.close()

if not df_history.empty:
    df_history.columns = ["응시 시간", "획득 점수", "1번", "2번", "3번", "4번", "5번", "6번", "7번", "8번", "9번", "10번"]
    st.dataframe(df_history, use_container_width=True)
else:
    st.info("아직 응시 기록이 없습니다. 위에서 정답을 선택하고 제출해 보세요!")
