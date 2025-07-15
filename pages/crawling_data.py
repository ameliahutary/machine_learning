import streamlit as st
import pandas as pd
import tweepy
from datetime import datetime

st.set_page_config(page_title="Advanced Twitter Crawler", layout="wide")
st.title("🐦 Twitter Crawler (Custom Jumlah, Rentang Tanggal, Gambar)")

# Input token dan parameter
bearer_token = st.text_input("🔐 Masukkan Bearer Token", type="password")
query = st.text_input("🔍 Kata kunci pencarian", "#enhypen")

start_date = st.date_input("📅 Tanggal mulai")
end_date = st.date_input("📅 Tanggal akhir")
jumlah_total = st.number_input("🔢 Jumlah tweet yang ingin diambil (max 1000 untuk demo)", min_value=10, value=300, step=10)

# Fungsi format tanggal ISO
def to_iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

# Mulai Crawling
if st.button("🚀 Mulai Crawling") and bearer_token and query and start_date and end_date:
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    all_data = []
    next_token = None
    total_collected = 0

    with st.spinner("🔄 Mengambil tweet..."):
        while total_collected < jumlah_total:
            max_batch = min(100, jumlah_total - total_collected)
            response = client.search_all_tweets(  # Ganti ke search_recent_tweets jika hanya butuh data 7 hari ke belakang
                query=query,
                max_results=max_batch,
                start_time=to_iso(datetime.combine(start_date, datetime.min.time())),
                end_time=to_iso(datetime.combine(end_date, datetime.max.time())),
                tweet_fields=["id", "text", "created_at", "lang", "conversation_id", "public_metrics", "in_reply_to_user_id", "attachments"],
                user_fields=["username", "id", "location"],
                media_fields=["url", "type", "preview_image_url"],
                expansions=["author_id", "in_reply_to_user_id", "attachments.media_keys"],
                next_token=next_token
            )

            tweets = response.data or []
            users = {u["id"]: u for u in response.includes.get("users", [])}
            media = {m["media_key"]: m for m in response.includes.get("media", [])}

            for tweet in tweets:
                user = users.get(tweet.author_id, {})
                in_reply_user = users.get(tweet.in_reply_to_user_id, {})
                metrics = tweet.public_metrics
                media_url = None
                if tweet.attachments:
                    media_keys = tweet.attachments.get("media_keys", [])
                    for key in media_keys:
                        m = media.get(key)
                        if m and m.get("type") in ["photo", "animated_gif"]:
                            media_url = m.get("url") or m.get("preview_image_url")
                            break

                row = {
                    "conversation_id_str": str(tweet.conversation_id),
                    "created_at": tweet.created_at,
                    "favorite_count": metrics.get("like_count", 0),
                    "full_text": tweet.text,
                    "id_str": str(tweet.id),
                    "image_url": media_url,
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

                all_data.append(row)
                total_collected += 1

            next_token = response.meta.get("next_token")
            if not next_token:
                break

    if all_data:
        df = pd.DataFrame(all_data)
        st.success(f"✅ Berhasil mengambil {len(df)} tweet!")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="advanced_tweet_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Tidak ada data yang ditemukan.")
