@st.cache_data
def load_data():

    # cp949 실패 시 utf-8 사용
    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv")

    df.columns = df.columns.str.strip()

    # 날짜 처리
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        errors="coerce"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df
