import streamlit as st
import pandas as pd
st.set_page_config(page_title="Netflix AI Dashboard", layout="wide")
st.set_page_config(page_title="Netflix AI Dashboard", layout="wide")

# ---------------- PAGE TITLE ----------------
st.title("🎬 InsightGenAI - Netflix Analytics Dashboard")
st.caption("Simple Netflix data analysis + insights app")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("netflix_clean_dataset.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("Filters")

if "type" in df.columns:
    type_filter = st.sidebar.multiselect(
        "Select Type",
        df["type"].dropna().unique(),
        default=df["type"].dropna().unique()
    )
    df = df[df["type"].isin(type_filter)]

if "release_year" in df.columns:
    year_range = st.sidebar.slider(
        "Release Year",
        int(df["release_year"].min()),
        int(df["release_year"].max()),
        (int(df["release_year"].min()), int(df["release_year"].max()))
    )
    df = df[df["release_year"].between(year_range[0], year_range[1])]

# ---------------- DATA TABLE ----------------
st.subheader("📊 Dataset")
st.dataframe(df)

# ---------------- KPI METRICS ----------------
st.subheader("📈 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(df))

if "type" in df.columns:
    col2.metric("Movies", len(df[df["type"] == "Movie"]))
    col3.metric("TV Shows", len(df[df["type"] == "TV Show"]))

# ---------------- CHARTS ----------------
st.subheader("📊 Content Distribution")

if "type" in df.columns:
    st.bar_chart(df["type"].value_counts())

st.subheader("📅 Release Year Trends")

if "release_year" in df.columns:
    st.bar_chart(df["release_year"].value_counts().head(10))

# ---------------- SMART RECOMMENDATION ----------------
st.subheader("🎬 Smart Recommendation System")

option = st.selectbox("Filter recommendations by", ["type", "country", "rating"])

if option in df.columns:
    selected = st.selectbox(f"Choose {option}", df[option].dropna().unique())

    recs = df[df[option] == selected]

    st.write("Top Matches:")
    st.dataframe(recs[["title", "type", "country", "release_year", "rating"]].head(10))

# ---------------- AI INSIGHT BUTTON -------------
st.subheader("🤖 AI Data Analyst")

if st.button("Generate Smart Insights"):

    st.info("Analyzing Netflix dataset...")

    total = len(df)
    st.write(f"📊 Total Titles: {total}")

    if "type" in df.columns:
        movies = len(df[df["type"] == "Movie"])
        tv = len(df[df["type"] == "TV Show"])

        st.write(f"🎬 Movies: {movies}")
        st.write(f"📺 TV Shows: {tv}")

        ratio = movies / total * 100

        st.write(f"📊 Movie Ratio: {ratio:.2f}%")

        if movies > tv:
            st.success("Insight: Netflix has more Movies than TV Shows.")
        else:
            st.success("Insight: TV Shows are more dominant.")

    if "country" in df.columns:
        st.write(f"🌍 Top Country: {df['country'].value_counts().idxmax()}")

    if "release_year" in df.columns:
        st.write(f"📅 Latest Content Year: {df['release_year'].max()}")

    st.success("Analysis completed successfully 🚀")
    st.subheader("🤖 Ask Netflix AI")

question = st.text_input("Ask a question about Netflix data")

if question:

    if "country" in df.columns and "country" in question.lower():
        st.write("Top country:", df["country"].value_counts().idxmax())

    elif "movie" in question.lower():
        if "type" in df.columns:
            st.write("Movies count:", len(df[df["type"] == "Movie"]))

    elif "tv" in question.lower():
        if "type" in df.columns:
            st.write("TV Shows count:", len(df[df["type"] == "TV Show"]))

    else:
        st.info("Try asking about movies, TV shows, country, or trends.")