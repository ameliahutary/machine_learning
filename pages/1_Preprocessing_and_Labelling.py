import streamlit as st
import pandas as pd
import re
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk

# Download NLTK stopwords (sekali saja)
nltk.download('stopwords')

# Konfigurasi halaman
st.set_page_config(page_title="Preprocessing & Sentiment Labelling", layout="wide")
st.title("🧹 Preprocessing & Sentiment Labelling")

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

        # Inisialisasi stopwords
        stop_words = set(stopwords.words('english'))

        # Fungsi preprocessing
        def preprocess(text):
            if pd.isnull(text):
                return ''
            text = re.sub(r"http\S+", "", text)           # Hapus URL
            text = re.sub(r"@\w+", "", text)              # Hapus mention
            text = re.sub(r'#.*', '', text)               # Hapus hashtag symbol
            text = re.sub(r"[^a-zA-Z\s]", "", text)       # Hapus karakter non-huruf
            text = re.sub(r"\s+", " ", text).strip()      # Hapus spasi berlebih
            text = text.lower()                           # Lowercase
            tokens = text.split()                         # Tokenisasi
            filtered = [word for word in tokens if word not in stop_words]
            unique_words = list(dict.fromkeys(filtered))  # Hapus duplikat
            return ' '.join(unique_words)

        # Proses teks
        df['clean_text'] = df['full_text'].apply(preprocess)

        # Fungsi untuk pelabelan sentimen
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

        # Terapkan pelabelan
        df['label'] = df['clean_text'].apply(get_sentiment)

        # Tampilkan hasil
        st.success("✅ Preprocessing dan pelabelan selesai!")
        st.dataframe(df[['full_text', 'clean_text', 'label']].head())

        # Tombol download
        st.download_button(
            label="⬇️ Download hasil sebagai CSV",
            data=df[['full_text', 'clean_text', 'label']].to_csv(index=False).encode('utf-8'),
            file_name="preprocessed_labeled_data.csv",
            mime="text/csv"
        )
