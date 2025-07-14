import streamlit as st
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk

nltk.download('punkt')
nltk.download('stopwords')

st.title("🧹 Preprocessing & Sentiment Labelling")

uploaded_file = st.file_uploader("📤 Upload file CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📄 Preview Data Asli:")
    st.dataframe(df.head())

    # Preprocessing function
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

    df['clean_text'] = df['full_text'].astype(str).apply(preprocess)

    # Labeling
    def get_sentiment(text):
        if not text.strip():
            return "neutral"
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return "positive"
        elif polarity < 0:
            return "negative"
        else:
            return "neutral"

    df['label'] = df['clean_text'].apply(get_sentiment)

    st.success("✅ Preprocessing dan pelabelan selesai!")
    st.write("🔍 Preview hasil:")
    st.dataframe(df[['full_text', 'clean_text', 'label']].head())

    # Download link
    st.download_button(
        label="⬇️ Download hasil",
        data=df[['full_text', 'clean_text', 'label']].to_csv(index=False).encode('utf-8'),
        file_name="labelled_data.csv",
        mime="text/csv"
    )
