import streamlit as st
import pandas as pd
import tweepy

st.set_page_config(page_title="Twitter Crawler Resmi", layout="wide")
st.title("🐦 Twitter Crawler via Twitter API (Tweepy)")

# Input API
bearer_token = st.text_input("🔐 Masukkan Bearer Token Twitter kamu", type="password")

# Parameter pencarian
query = st.text_input("🔍 Kata kunci pencarian (misal: #enhypen)", "#enhypen")
max_results = st.slider("🔢 Jumlah tweet yang ingin diambil", 10, 100, 50)

# Mulai crawling
if st.button("🚀 Mulai Crawling") and bearer_token and query:
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["id", "text", "created_at", "lang", "conversation_id", "public_metrics", "in_reply_to_user_id"],
        user_fields=["username", "id", "location"],
        expansions=["author_id", "in_reply_to_user_id"]
    )

    tweets = response.data
    users = {u["id"]: u for u in response.includes["users"]} if response.includes else {}

    if tweets:
        data = []
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
                "image_url": None,  # Placeholder, API ini butuh media_fields untuk akses gambar
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

        df = pd.DataFrame(data)
        st.success(f"✅ Berhasil mengambil {len(df)} tweet")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download sebagai CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="twitter_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Tidak ada tweet yang ditemukan.")
