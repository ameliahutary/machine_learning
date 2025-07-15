import streamlit as st
import pandas as pd
import tweepy
from datetime import datetime

st.set_page_config(page_title="Twitter Crawler Lengkap", layout="wide")
st.title("🐦 Twitter Crawler via API (Unlimited + Tanggal + Media)")

# Input Bearer Token
bearer_token = st.text_input("🔐 Masukkan Bearer Token kamu", type="password")

# Input parameter pencarian
query = st.text_input("🔍 Kata kunci (misal: #enhypen)", "#enhypen")
start_date = st.date_input("📅 Mulai dari tanggal", datetime(2025, 4, 1))
end_date = st.date_input("📅 Sampai tanggal", datetime(2025, 4, 30))
limit = st.number_input("🔢 Jumlah tweet yang ingin diambil", min_value=10, value=200)

# Fungsi bantu ambil gambar
def extract_image_url(tweet, media_map):
    if hasattr(tweet, "attachments") and tweet.attachments:
        for media_key in tweet.attachments.get("media_keys", []):
            media = media_map.get(media_key, {})
            if media.get("type") == "photo":
                return media.get("url")
    return None

# Mulai crawling
if st.button("🚀 Mulai Crawling") and bearer_token and query:
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    tweets_data = []
    next_token = None
    total = 0

    with st.spinner("📡 Mengambil data..."):
        while total < limit:
            remaining = limit - total
            batch_size = min(100, remaining)

            response = client.search_all_tweets(  # untuk full archive
                query=query,
                start_time=f"{start_date}T00:00:00Z",
                end_time=f"{end_date}T23:59:59Z",
                tweet_fields=["id", "text", "created_at", "lang", "conversation_id", "public_metrics", "in_reply_to_user_id", "attachments"],
                user_fields=["username", "id", "location"],
                media_fields=["url", "type"],
                expansions=["author_id", "in_reply_to_user_id", "attachments.media_keys"],
                max_results=batch_size,
                next_token=next_token
            )

            tweets = response.data or []
            includes = response.includes or {}
            users = {u["id"]: u for u in includes.get("users", [])}
            media_map = {m["media_key"]: m for m in includes.get("media", [])}

            for tweet in tweets:
                user = users.get(tweet.author_id, {})
                in_reply_user = users.get(tweet.in_reply_to_user_id, {})
                metrics = tweet.public_metrics

                tweets_data.append({
                    "conversation_id_str": str(tweet.conversation_id),
                    "created_at": tweet.created_at,
                    "favorite_count": metrics.get("like_count", 0),
                    "full_text": tweet.text,
                    "id_str": str(tweet.id),
                    "image_url": extract_image_url(tweet, media_map),
                    "in_reply_to_screen_name": in_reply_user.get("username") if in_reply_user else None,
                    "lang": tweet.lang,
                    "location": user.get("location"),
                    "quote_count": metrics.get("quote_count", 0),
                    "reply_count": metrics.get("reply_count", 0),
                    "retweet_count": metrics.get("retweet_count", 0),
                    "tweet_url": f"https://twitter.com/{user.get('username')}/status/{tweet.id}",
                    "user_id_str": str(tweet.author_id),
                    "username": user.get("username")
                })

            total += len(tweets)
            next_token = response.meta.get("next_token")
            if not next_token:
                break  # tidak ada lagi data

    if tweets_data:
        df = pd.DataFrame(tweets_data)
        st.success(f"✅ Berhasil mengambil {len(df)} tweet!")
        st.dataframe(df)

        st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), "twitter_crawled_data.csv", "text/csv")
    else:
        st.warning("❌ Tidak ada tweet ditemukan.")
