import streamlit as st
import pandas as pd
import re
from nltk.corpus import stopwords
from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk

# Unduh stopwords jika belum ada
nltk.download('stopwords')

# Konfigurasi halaman
st.set_page_config(page_title="Translasi, Preprocessing & Sentiment Labelling", layout="wide")
st.title("🌐 Translasi ➜ Preprocessing ➜ Sentiment Labelling")

# Upload file
uploaded_file = st.file_uploader("📤 Upload file CSV (wajib ada kolom 'full_text')", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    if 'full_text' not in df.columns:
        st.error("⚠️ Kolom 'full_text' tidak ditemukan dalam file.")
    else:
        st.write("📄 Preview Data Asli:")
        st.dataframe(df[['full_text']].head())

        with st.spinner("🔄 Menerjemahkan teks ke Bahasa Inggris..."):
            def translate_text(text):
                try:
                    return GoogleTranslator(source='auto', target='en').translate(text)
                except:
                    return text  # jika gagal, pakai teks aslinya

            df['translated'] = df['full_text'].apply(translate_text)

        st.write("🌍 Hasil Translasi:")
        st.dataframe(df[['full_text', 'translated']].head())

        # Inisialisasi stopwords Bahasa Inggris
        stop_words = set(stopwords.words('english'))

        # Fungsi preprocessing
        def preprocess(text):
            if pd.isnull(text):
                return ''
            text = re.sub(r"http\S+", "", text)
            text = re.sub(r"@\w+", "", text)
            text = re.sub(r"#", "", text)
            text = re.sub(r"[^a-zA-Z\s]", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            text = text.lower()
            tokens = text.split()
            filtered = [word for word in tokens if word not in stop_words]
            unique_words = list(dict.fromkeys(filtered))
            return ' '.join(unique_words)

        df['clean_text'] = df['translated'].apply(preprocess)

        # Fungsi pelabelan sentimen
        def get_sentiment(text):
            if not text.strip():
                return 'neutral'
            polarity = TextBlob(text).sentiment.polarity
            if polarity > 0:
                return 'positive'
            elif polarity < 0:
                return 'negative'
            else:
                return 'neutral'

        df['label'] = df['clean_text'].apply(get_sentiment)

        st.success("✅ Translasi, preprocessing, dan pelabelan selesai!")
        st.dataframe(df[['full_text', 'translated', 'clean_text', 'label']].head())

        # Tombol download
        st.download_button(
            label="⬇️ Download hasil sebagai CSV",
            data=df[['full_text', 'translated', 'clean_text', 'label']].to_csv(index=False).encode('utf-8'),
            file_name="translated_preprocessed_labeled.csv",
            mime="text/csv"
        )


