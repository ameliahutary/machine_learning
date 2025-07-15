import streamlit as st
import pandas as pd
import tweepy
from datetime import datetime

st.set_page_config(page_title="Twitter Data Crawler Resmi", layout="wide")
st.title("🐦 Twitter Data Crawler (API Resmi Tanpa Batasan 100)")

# Input token
bearer_token = st.text_input("🔐 Masukkan Bearer Token Twitter", type="password")

# Parameter pencarian
query = st.text_input("🔍 Kata kunci pencarian (misal: #enhypen)", "#enhypen")
lang = st.text_input("🌐 Kode bahasa (id, en, ko, dsb)", "id")
start_date = st.date_input("📅 Tanggal mulai", value=datetime(2025, 4, 1)).strftime("%Y-%m-%dT00:00:00Z")
end_date = st.date_input("📅 Tanggal akhir", value=datetime(2025, 4, 30)).strftime("%Y-%m-%dT23:59:59Z")
tweet_count = st.number_input("🔢 Jumlah tweet yang ingin diambil (boleh >100)", min_value=10, value=200, step=10)

# Tombol mulai
if st.button("🚀 Mulai Crawling") and bearer_token and query:
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    collected_tweets = []
    next_token = None
    total_collected = 0

    with st.spinner("Mengambil tweet..."):
        while total_collected < tweet_count:
            try:
                remaining = tweet_count - total_collected
                max_fetch = 100 if remaining > 100 else remaining

                response = client.search_all_tweets(
                    query=f"{query} lang:{lang}",
                    start_time=start_date,
                    end_time=end_date,
                    tweet_fields=["id", "text", "created_at", "lang", "conversation_id", "public_metrics", "in_reply_to_user_id"],
                    user_fields=["username", "id", "location"],
                    expansions=["author_id", "in_reply_to_user_id"],
                    max_results=max_fetch,
                    next_token=next_token
                )

                if not response.data:
                    break

                users = {u["id"]: u for u in response.includes["users"]} if response.includes else {}

                for tweet in response.data:
                    user = users.get(tweet.author_id, {})
                    in_reply_user = users.get(tweet.in_reply_to_user_id, {})
                    metrics = tweet.public_metrics

                    collected_tweets.append({
                        "conversation_id_str": str(tweet.conversation_id),
                        "created_at": tweet.created_at,
                        "favorite_count": metrics.get("like_count", 0),
                        "full_text": tweet.text,
                        "id_str": str(tweet.id),
                        "image_url": None,
                        "in_reply_to_screen_name": in_reply_user.get("username") if in_reply_user else None,
                        "lang": tweet.lang,
                        "location": user.get("location", None),
                        "quote_count": metrics.get("quote_count", 0),
                        "reply_count": metrics.get("reply_count", 0),
                        "retweet_count": metrics.get("retweet_count", 0),
                        "tweet_url": f"https://twitter.com/{user.get('username')}/status/{tweet.id}",
                        "user_id_str": str(tweet.author_id),
                        "username": user.get("username")
                    })

                total_collected += len(response.data)
                next_token = response.meta.get("next_token")

                if not next_token:
                    break

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
                break

    if collected_tweets:
        df = pd.DataFrame(collected_tweets)
        st.success(f"✅ Berhasil mengambil {len(df)} tweet!")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download sebagai CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="twitter_crawled_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Tidak ada tweet ditemukan dalam rentang waktu dan keyword tersebut.")
