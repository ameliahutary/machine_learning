import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def preprocess(text):
    if pd.isnull(text): return ''
    text = re.sub(r"http\S+|@\w+|#|[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stop_words]
    return ' '.join(dict.fromkeys(tokens))

st.title("🧹 Preprocessing Teks")

uploaded_file = st.file_uploader("Upload CSV (dengan kolom: full_text)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    if 'full_text' not in df.columns:
        st.error("File harus memiliki kolom 'full_text'")
    else:
        df['clean_text'] = df['full_text'].apply(preprocess)
        st.dataframe(df[['full_text', 'clean_text']])
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Cleaned CSV", csv, "cleaned_text.csv", "text/csv")
