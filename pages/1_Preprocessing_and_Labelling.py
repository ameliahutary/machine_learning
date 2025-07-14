# pages/1_Preprocessing_and_Labeling.py
import streamlit as st
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import nltk

nltk.download('punkt')
nltk.download('stopwords')

st.title("🧹 Preprocessing & Labelling (TextBlob)")

uploaded_file = st.file_uploader("📤 Upload file CSV (wajib punya kolom 'full_text')", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    if 'full_text' not in df.columns:
        st.error("Kolom 'full_text' tidak ditemukan.")
    else:
        stop_words = set(stopwords.words('english'))

        def preprocess(text):
            if pd.isnull(text):
                return ''
            text = re.sub(r"http\S+", "", text)
            text = re.sub(r"@\w+", "", text)
            text = re.sub(r"#", "", text)
            text = re.sub(r"[^a-zA-Z\s]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            text = text.lower()
            tokens = word_tokenize(text)
            filtered = [word for word in tokens if word not in stop_words]
            return ' '.join(filtered)

        def get_sentiment(text):
            if not text.strip():
                return "neutral"
            polarity = TextBlob(text).sentiment.polarity
            if polarity > 0:
                return "positive"
            elif polarity < 0:
                return "negative"
            else:
                return "neutral"

        st.info("🔄 Memproses data...")
        df['clean_text'] = df['full_text'].apply(preprocess)
        df['label'] = df['clean_text'].apply(get_sentiment)

        st.success("✅ Selesai! Berikut hasilnya:")
        st.dataframe(df[['full_text', 'clean_text', 'label']].head())

        st.download_button(
            "⬇️ Download hasil",
            data=df[['full_text', 'clean_text', 'label']].to_csv(index=False).encode('utf-8'),
            file_name="preprocessed_labelled.csv",
            mime="text/csv"
        )
