import streamlit as st
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import nltk
import io

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Stopwords list
stop_words = set(stopwords.words('english'))

# Preprocessing function
def preprocess(text):
    if pd.isnull(text):
        return ''
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)     # Remove mentions
    text = re.sub(r'#', '', text)         # Remove hashtag symbols
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-letter characters
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra whitespace
    text = text.lower()                  # Lowercase
    tokens = word_tokenize(text)         # Tokenize
    filtered = [word for word in tokens if word not in stop_words]  # Remove stopwords
    unique_words = list(dict.fromkeys(filtered))  # Remove duplicates
    return ' '.join(unique_words)

# Sentiment analysis function
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Streamlit app
st.title("ENHYPEN Tweet Preprocessing & Sentiment Analysis")

uploaded_file = st.file_uploader("Upload CSV file (must include 'full_text' column)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    if 'full_text' not in df.columns:
        st.error("Kolom 'full_text' tidak ditemukan dalam file CSV.")
    else:
        st.info("Memproses teks...")
        df['clean_text'] = df['full_text'].apply(preprocess)
        st.success("Preprocessing selesai!")

        st.info("Menganalisis sentimen...")
        df['sentiment'] = df['clean_text'].apply(get_sentiment)
        st.success("Analisis sentimen selesai!")

        st.subheader("Contoh hasil:")
        st.dataframe(df[['full_text', 'clean_text', 'sentiment']].head())

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Hasil sebagai CSV",
            data=csv,
            file_name='enhypen_cleaned_sentiment.csv',
            mime='text/csv'
        )
