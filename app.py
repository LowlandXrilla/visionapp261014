import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="제조 품질 현황 대시보드",
    page_icon="🏭",
    layout="wide"
)

# 2. 기본 샘플 데이터 생성 함수 (CSV 미업로드 시 사용)
def load_sample_data():
    data = [
        {"inspection_date": "2026-10-01", "product_id": "P001", "result": "OK", "defect_type": "None", "confidence": 0.98},
        {"inspection_date": "2026-10-01", "product_id": "P002", "result": "NG", "defect_type": "Scratch", "confidence": 0.91},
        {"inspection_date": "2026-10-01", "product_id": "P001", "result": "OK", "defect_type": "None", "confidence": 0.95},
        {"inspection_date": "2026-10-02", "product_id": "P003", "result": "OK", "defect_type": "None", "confidence": 0.96},
        {"inspection_date": "2026-10-02", "product_id": "P004", "result": "NG", "defect_type": "Crack", "confidence": 0.88},
        {"inspection_date": "2026-10-02", "product_id": "P002", "result": "NG", "defect_type": "Scratch", "confidence": 0.85},
        {"inspection_date": "2026-10-03", "product_id": "P001", "result": "OK", "defect_type": "None", "confidence": 0.99},
        {"inspection_date": "2026-10-03", "product_id": "P003", "result": "NG", "defect_type": "Stain", "confidence": 0.92},
        {"inspection_date": "2026-10-03", "product_id": "P004", "result": "OK", "defect_type": "None", "confidence": 0.94},
        {"inspection_date": "2026-10-04", "product_id": "P002", "result": "OK", "defect_type": "None", "confidence": 0.97},
        {"inspection_date": "2026-10-04", "product_id": "P001", "result": "NG", "defect_type": "Dent", "confidence": 0.89},
        {"inspection_date": "2026-10-04", "product_id": "P003", "result": "NG", "defect_type": "Scratch", "confidence": 0.93},
        {"inspection_date": "2026-10-05", "product_id": "P004", "result": "OK", "defect_type": "None", "confidence": 0.96},
        {"inspection_date": "2026-10-05", "product_id": "P001", "result": "OK", "defect_type": "None", "confidence": 0.98},
        {"inspection_date": "2026-10-05", "product_id": "P002", "result": "NG", "defect_type": "Crack", "confidence": 0.90},
    ]
    return pd.DataFrame(data)

# 3. 화면 상단 제목 및 부제
st.title("🏭 제조 품질 현황 대시보드")
st.subheader("AI 비전검사 PoC 준비를 위한 품질 데이터 모니터링")
st.markdown("---")

# 4. 사이드바: CSV 파일 업로드
st.sidebar.header("📂 데이터 및 필터 설정")
uploaded_file = st.sidebar.file_uploader("검사 결과 CSV 업로드", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        # 한글 엑셀에서 저장된 CSV(cp949 인코딩) 대응
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="cp949")
    st.sidebar.success("업로드된 CSV 데이터를 사용합니다.")
else:
    df = load_sample_data()
    st.sidebar.info("현재 기본 샘플 데이터를 표시 중입니다.")

# 데이터 전처리 (날짜 형식 변환 및 결측치 처리)
# pandas에서 "None" 문자열을 결측치(NaN)로 읽는 것을 방지하기 위해 문자열로 채움
df["defect_type"] = df["defect_type"].fillna("None").astype(str)
df["inspection_date"] = pd.to_datetime(df["inspection_date"]).dt.date

# 5. 사이드바: 필터 설정 (날짜, 제품, 검사 결과)
st.sidebar.subheader("🔍 데이터 필터")

# 날짜 필터
min_date = df["inspection_date"].min()
max_date = df["inspection_date"].max()
date_range = st.sidebar.date_input(
    "검사 날짜 범위",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 제품 필터
product_list = sorted(df["product_id"].unique().tolist())
selected_products = st.sidebar.multiselect(
    "제품 ID 선택",
    options=product_list,
    default=product_list
)

# 검사 결과 필터
result_list = sorted(df["result"].unique().tolist())
selected_results = st.sidebar.multiselect(
    "검사 결과 (OK / NG)",
    options=result_list,
    default=result_list
)

# 필터 적용하기
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0] if isinstance(date_range, tuple) else date_range

filtered_df = df[
    (df["inspection_date"] >= start_date) &
    (df["inspection_date"] <= end_date) &
    (df["product_id"].isin(selected_products)) &
    (df["result"].isin(selected_results))
]

# 업로드 데이터 미리보기 (접기/펴기 가능)
with st.expander("📋 원본/필터링 데이터 미리보기 (클릭하여 열기)"):
    st.dataframe(filtered_df, use_container_width=True)

# 필터링 결과가 비어있을 경우 예외 처리
if filtered_df.empty:
    st.warning("선택한 필터 조건에 해당하는 데이터가 없습니다. 사이드바 필터를 조정해 주세요.")
    st.stop()

# 6. 상단: KPI 카드 표시
total_count = len(filtered_df)
ok_count = len(filtered_df[filtered_df["result"] == "OK"])
ng_count = len(filtered_df[filtered_df["result"] == "NG"])
defect_rate = (ng_count / total_count * 100) if total_count > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 검사", f"{total_count:,} 건")
col2.metric("정상 (OK)", f"{ok_count:,} 건")
col3.metric("불량 (NG)", f"{ng_count:,} 건")
col4.metric("불량률", f"{defect_rate:.1f} %")

st.markdown("---")

# 7. 중단: 날짜별 검사 현황 그래프 & 불량 유형별 그래프
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 날짜별 검사 현황 (OK vs NG)")
    # 날짜별 OK, NG 건수 집계
    daily_summary = filtered_df.groupby(["inspection_date", "result"]).size().unstack(fill_value=0)
    st.line_chart(daily_summary)

with chart_col2:
    st.subheader("📊 불량 유형별 건수")
    # NG 데이터 중 'None'을 제외한 실제 불량 유형만 집계
    ng_only_df = filtered_df[(filtered_df["result"] == "NG") & (filtered_df["defect_type"] != "None")]
    if not ng_only_df.empty:
        defect_counts = ng_only_df["defect_type"].value_counts()
        st.bar_chart(defect_counts)
    else:
        st.info("선택된 조건 내 불량(NG) 데이터가 없습니다.")

st.markdown("---")

# 8. 하단: 최근 검사 데이터 테이블 (최근 10건, OK/NG 시각적 구분)
st.subheader("🕒 최근 검사 결과 10건")

# 날짜 기준 최신순 정렬 후 상위 10건 추출
recent_10_df = filtered_df.sort_values(by="inspection_date", ascending=False).head(10).copy()

# OK/NG 구분을 직관적으로 보여주기 위한 상태 컬럼 추가
recent_10_df["판정 상태"] = recent_10_df["result"].apply(lambda x: "🟢 OK (정상)" if x == "OK" else "🔴 NG (불량)")

# 출력할 컬럼 순서 정리
display_cols = ["inspection_date", "product_id", "판정 상태", "defect_type", "confidence"]
st.dataframe(
    recent_10_df[display_cols],
    use_container_width=True,
    hide_index=True
)
