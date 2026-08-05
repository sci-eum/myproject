import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# [1] 페이지 기본 설정
st.set_page_config(layout="wide", page_title="화학과 AIDT 메인", page_icon="🏠")

# [2] SQLite3 데이터베이스 및 테이블 자동 생성 함수
def init_db():
    conn = sqlite3.connect('myproject.db')
    cursor = conn.cursor()
    # 1. users 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    # 2. learning_history 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            m1 INTEGER, m2 INTEGER, m3 INTEGER, m4 INTEGER, m5 INTEGER,
            m6 INTEGER, m7 INTEGER, m8 INTEGER, m9 INTEGER, m10 INTEGER,
            score INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 비밀번호 암호화 함수 (SHA-256)
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# 로그인 검증 함수
def login_user(userid, password):
    conn = sqlite3.connect('myproject.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE userid =? AND password =?', (userid, password))
    data = cursor.fetchall()
    conn.close()
    return data

# 회원가입 처리 함수
def add_user(userid, password):
    conn = sqlite3.connect('myproject.db')
    cursor = conn.cursor()
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO users(userid, password, created_at) VALUES (?,?,?)', (userid, password, now))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False  # 아이디 중복 발생 시
    conn.close()
    return success

# [3] 세션 상태 관리 (로그인 유무 확인용)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "userid" not in st.session_state:
    st.session_state["userid"] = ""

# [4] 사이드바 로그인 / 회원가입 UI 구축
st.sidebar.title("🔐 계정 관리 시스템")
menu = ["로그인", "회원가입"]
choice = st.sidebar.selectbox("작업 선택", menu)

if not st.session_state["logged_in"]:
    if choice == "로그인":
        st.sidebar.subheader("로그인")
        login_id = st.sidebar.text_input("아이디(User ID)", key="login_id")
        login_pw = st.sidebar.text_input("비밀번호", type="password", key="login_pw")
        
        if st.sidebar.button("로그인 실행"):
            hashed_pw = make_hashes(login_pw)
            result = login_user(login_id, hashed_pw)
            if result:
                st.session_state["logged_in"] = True
                st.session_state["userid"] = login_id
                st.sidebar.success(f"🎉 {login_id}님 환영합니다!")
                st.rerun()
            else:
                st.sidebar.error("❌ 아이디 또는 비밀번호가 틀렸습니다.")
                
    elif choice == "회원가입":
        st.sidebar.subheader("새 계정 생성")
        new_id = st.sidebar.text_input("사용할 아이디", key="new_id")
        new_pw = st.sidebar.text_input("사용할 비밀번호", type="password", key="new_pw")
        
        if st.sidebar.button("회원가입 완료"):
            if new_id.strip() == "" or new_pw.strip() == "":
                st.sidebar.warning("⚠️ 빈칸을 입력할 수 없습니다.")
            else:
                hashed_pw = make_hashes(new_pw)
                if add_user(new_id, hashed_pw):
                    st.sidebar.success("✅ 회원가입 성공! 로그인 해주세요.")
                else:
                    st.sidebar.error("❌ 이미 존재하는 아이디입니다.")

else:
    st.sidebar.success(f"현재 접속 계정: **{st.session_state['userid']}**")
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["userid"] = ""
        st.rerun()


# [5] 메인 콘텐츠 화면 제어 (로그인 사용자 전용)
if st.session_state["logged_in"]:
    url = 'https://www.youtube.com/watch?v=U57LVkQVf4o'
    imgpath = 'https://th.bing.com/th/id/OIP.iTjZvAhKf_dbA9ArjvERaAHaEK?w=304&h=180&c=7&r=0&o=7&dpr=1.1&pid=1.7&rm=3'
    imgpath1 = './img/maxresdefault.jpg'

    st.title('This is my first webapp!!')
    st.subheader('화학과 AIDT')
    
    # 1차시 영상 탭
    col1, col2 = st.columns((4,1))
    with col1:
        with st.expander('1차시_동영상', expanded=True):
            st.title('동영상 시청......')
            st.subheader('동영상 시청 좀 하라고')
            st.write('라고 말해도 안할거지?')
            st.video(url)
    with col2:
        with st.expander('Tips...'):
            st.subheader('Tips...')
            st.image(imgpath)
            st.write('This is a term....')

    # 2차시 이미지 탭
    coll1, coll2 = st.columns((3,3))
    with coll1:
        with st.expander('2차시_이미지'):
            st.title('이미지 시청......')
            st.subheader('이미지 시청 좀 하라고')
            st.write('라고 말해도 안할거지?')
            try:
                st.image(imgpath1)
            except:
                st.info("로컬 테스트용 이미지 경로가 지정되어 있습니다.")
    with coll2:
        with st.expander('Tips...'):
            st.subheader('Tips...')
            st.image(imgpath)
            st.write('This is a term....')

    # 3차시 개념 정리 탭
    colll1, colll2 = st.columns((1,1))
    with colll1:
        with st.expander('3차시_개념'):
            st.title('머신러닝의 개념')
            st.markdown("""
            - **정의**: 데이터와 정답을 입력받아 컴퓨터가 스스로 규칙(패턴)을 학습하는 인공지능의 한 분야
            - **특징**: 명시적인 프로그래밍 없이도 새로운 데이터에 대한 예측 및 판단이 가능함
            - **핵심 요소**:
                - **데이터(Data)**: 학습의 기반이 되는 입력값 및 타깃값
                - **모델(Model)**: 데이터의 패턴을 수학적으로 표현한 알고리즘
                - **학습(Training)**: 오차를 줄여나가는 알고리즘 최적화 과정
            - **주요 워크플로우**: 데이터 수집 ➔ 전처리 ➔ 모델 선택 ➔ 학습 ➔ 평가 ➔ 배포
            """)

    with colll2:
        with st.expander('Tips...'):
            st.subheader('Tips...')
            st.markdown("""
            💡 **핵심 하위 개념 삼총사**
            
            - **지도 학습 (Supervised)**
              - 문제와 정답을 모두 주고 학습
              - 예측(회귀), 분류(로지스틱)에 활용
            
            - **비지도 학습 (Unsupervised)**
              - 정답 없이 데이터만 주고 학습
              - 군집화(Clustering), 차원 축소
            
            - **강화 학습 (Reinforcement)**
              - 보상과 벌칙을 통해 스스로 최적화
              - 게임 AI, 로봇 제어에 활용
            """)
else:
    st.info("🔒 서비스를 이용하시려면 왼쪽 사이드바에서 **로그인**을 먼저 진행해 주세요. 계정이 없다면 회원가입을 하실 수 있습니다.")
