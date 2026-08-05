import os
import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝 의 사례",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 머신러닝 문제 해결 사례")
st.write("아래 화면에서 직접 개발한 머신러닝 활용 및 문제 해결 사례를 확인할 수 있습니다.")

# 2. reaction.html 파일 경로 설정 및 읽기
# 팁: reaction.html 파일은 이 파이썬 파일과 같은 위치(pages/) 또는 프로젝트 루트 경로에 있어야 합니다.
# 2. reaction.html 파일 경로 설정 및 읽기
from pathlib import Path

# 현재 파일(pages/...)의 부모의 부모 폴더(최상위 root)를 기준으로 절대 경로 계산
BASE_DIR = Path(__file__).resolve().parent.parent
html_file_path = BASE_DIR / "htmls" / "reaction.html"

# os.path.exists 검사를 위해 문자열 경로도 생성
html_file_path_str = str(html_file_path)

if html_file_path.exists():
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 3. iframe 스크롤 및 크기 설정을 위한 CSS 래퍼 추가
    # 기본 크기인 1024x768을 유지하되, 내부 콘텐츠가 크면 상하좌우 스크롤바가 생기도록 합니다.
    scrolling_html = f"""
    <div style="
        width: 1024px; 
        height: 768px; 
        overflow: auto; 
        border: 1px solid #ccc;
        border-radius: 5px;
    ">
        {html_content}
    </div>
    """
    
    # 4. Streamlit 컴포넌트를 통해 HTML 렌더링
    components.html(scrolling_html, width=1050, height=800, scrolling=False)

else:
    st.error(f"❌ '{html_file_path_str}' 파일을 찾을 수 없습니다. 파일이 올바른 경로에 있는지 확인해 주세요.")
    st.info("현재 설정된 경로: " + os.path.abspath(html_file_path_str))


if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 3. iframe 스크롤 및 크기 설정을 위한 CSS 래퍼 추가
    # 기본 크기인 1024x768을 유지하되, 내부 콘텐츠가 크면 상하좌우 스크롤바가 생기도록 합니다.
    scrolling_html = f"""
    <div style="
        width: 1024px; 
        height: 768px; 
        overflow: auto; 
        border: 1px solid #ccc;
        border-radius: 5px;
    ">
        {html_content}
    </div>
    """
    
    # 4. Streamlit 컴포넌트를 통해 HTML 렌더링
    # 컴포넌트 자체의 영역은 스크롤 박스보다 살짝 크게 잡아 잘림을 방지합니다.
    components.html(scrolling_html, width=1050, height=800, scrolling=False)

else:
    st.error(f"❌ '{html_file_path}' 파일을 찾을 수 없습니다. 파일이 올바른 경로에 있는지 확인해 주세요.")
    st.info("현재 설정된 경로: " + os.path.abspath(html_file_path))
