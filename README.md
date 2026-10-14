# visionapp261014


# 🏭 제조 품질 현황 대시보드 (AI 비전검사 PoC 사전 프로젝트)

본 프로젝트는 본격적인 AI 비전검사 모델 구현에 앞서, 검사 결과 데이터를 모니터링하고 시각화하는 웹 대시보드입니다.

## ✨ 주요 기능
- **CSV 파일 업로드**: 검사 결과 CSV 파일을 업로드하여 즉시 분석 (미업로드 시 기본 샘플 데이터 자동 로드)
- **핵심 KPI 요약**: 전체 검사 건수, 정상(OK) 수량, 불량(NG) 수량, 불량률(%) 카드 표시
- **데이터 시각화**: 날짜별 검사 추이(선그래프) 및 불량 유형별 빈도(막대그래프)
- **상세 조회 및 필터**: 날짜, 제품 ID, 판정 결과(OK/NG) 필터링 및 최근 검사 10건 표 제공

---

## 💻 로컬 실행 방법
```bash
# 1. 필수 라이브러리 설치
pip install -r requirements.txt

# 2. 대시보드 실행
streamlit run app.py
```

---

## 🚀 GitHub 업로드 및 Streamlit Community Cloud 배포 방법

### 1단계: GitHub에 코드 올리기
1. [GitHub](https://github.com/)에 로그인 후 우측 상단 `+` 버튼을 눌러 **New repository**를 클릭합니다.
2. Repository name에 `vision-dashboard`를 입력하고, **Public**으로 설정한 뒤 **Create repository**를 클릭합니다.
3. 생성된 페이지에서 **uploading an existing file** 링크를 클릭합니다. (Git 명령어 없이 웹에서 바로 올리는 가장 쉬운 방법입니다.)
4. 내 컴퓨터에서 만든 `app.py`, `requirements.txt`, `sample_data.csv`, `README.md` 파일 4개를 마우스로 끌어다 놓습니다.
5. 아래쪽 초록색 **Commit changes** 버튼을 누르면 GitHub 업로드가 완료됩니다.

### 2단계: Streamlit Community Cloud에 배포하기
1. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 **Continue with GitHub**를 눌러 로그인합니다.
2. 우측 상단의 **Create app** (또는 **New app**) 버튼을 클릭합니다.
3. **Deploy a public app from GitHub**를 선택합니다.
4. 아래 항목을 순서대로 선택 및 입력합니다:
   - **Repository**: 방금 만든 `내아이디/vision-dashboard` 선택
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 하단의 **Deploy!** 버튼을 클릭합니다.
6. 약 1~2분간 패키지 설치 화면이 지나가면, 전 세계 어디서나 접속 가능한 나만의 웹 대시보드 URL이 완성됩니다!
