import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
from datetime import date

st.set_page_config(page_title="Twitter Data Crawler", layout="wide")
st.title("🐦 Twitter Data Crawler")

# Form input
with st.form("crawl_form"):
    keyword = st.text_input("🔍 Masukkan kata kunci atau hashtag (misalnya: #enchella2025)", "#enhypen")
    start_date = st.date_input("📅 Tanggal mulai", value=date(2025, 4, 1))
    end_date = st.date_input("📅 Tanggal akhir", value=date(2025, 4, 30))
    limit = st.number_input("🔢 Jumlah tweet yang ingin diambil", min_value=10, max_value=1000, value=100, step=10)
    submitted = st.form_submit_button("🚀 Mulai Crawling")

if submitted:
    query = f'{keyword} since:{start_date} until:{end_date} lang:en'
    st.info(f"📡 Mengambil tweet dengan query: `{query}`")

    tweets = []
    with st.spinner("⏳ Mengambil data dari Twitter..."):
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            tweets.append({
                'date': tweet.date,
                'user': tweet.user.username,
                'full_text': tweet.content,
                'like_count': tweet.likeCount,
                'retweet_count': tweet.retweetCount,
                'url': tweet.url
            })

    if tweets:
        df = pd.DataFrame(tweets)
        st.success(f"✅ Berhasil mengambil {len(df)} tweet!")
        st.dataframe(df[['date', 'user', 'full_text']])

        # Tombol download
        st.download_button(
            label="⬇️ Download sebagai CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="tweet_crawled.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Tidak ada tweet yang ditemukan.")
