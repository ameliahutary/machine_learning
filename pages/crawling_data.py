import streamlit as st
import pandas as pd
import tweepy
from datetime import datetime

st.set_page_config(page_title="Twitter Crawler Resmi", layout="wide")
st.title("🐦 Twitter Crawler Resmi (Tweepy)")

# Input kredensial
bearer_token = st.text_input("🔐 Masukkan Bearer Token Twitter kamu", type="password")

# Input parameter
query = st.text_input("🔍 Kata kunci pencarian (misal: #enhypen)", "#enhypen")
language = st.selectbox("🌐 Pilih bahasa tweet", options=["id", "en", "ko", "ja", "all"], index=1)
start_date = st.date_input("📅 Tanggal mulai", value=datetime(2025, 4, 1))
end_date = st.date_input("📅 Tanggal akhir", value=datetime(2025, 4, 30))
tweet_count = st.number_input("🔢 Jumlah tweet yang ingin diambil", min_value=10, max_value=10000, value=500, step=50)

# Mulai crawling
if st.button("🚀 Mulai Crawling") and bearer_token and query:
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    query_final = query
    if language != "all":
        query_final += f" lang:{language}"

    st.info(f"📡 Mengambil tweet: \"{query_final}\" antara {start_date} dan {end_date} ...")

    data = []
    next_token = None
    collected = 0

    while collected < tweet_count:
        max_results = min(100, tweet_count - collected)
        response = client.search_all_tweets(
            query=query_final,
            tweet_fields=["id", "text", "created_at", "lang", "conversation_id", "public_metrics", "in_reply_to_user_id"],
            user_fields=["username", "id", "location"],
            expansions=["author_id", "in_reply_to_user_id"],
            start_time=datetime.combine(start_date, datetime.min.time()).isoformat() + "Z",
            end_time=datetime.combine(end_date, datetime.max.time()).isoformat() + "Z",
            next_token=next_token,
            max_results=max_results
        )

        tweets = response.data
        users = {u["id"]: u for u in response.includes["users"]} if response.includes else {}

        if not tweets:
            break

        for tweet in tweets:
            user = users.get(tweet.author_id, {})
            in_reply_user = users.get(tweet.in_reply_to_user_id, {})
            metrics = tweet.public_metrics

            row = {
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
            }
            data.append(row)

        collected += len(tweets)
        next_token = response.meta.get("next_token")
        if not next_token:
            break

    if data:
        df = pd.DataFrame(data)
        st.success(f"✅ Berhasil mengambil {len(df)} tweet.")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download sebagai CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="crawled_tweets.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Tidak ada tweet ditemukan pada rentang waktu dan query tersebut.")
