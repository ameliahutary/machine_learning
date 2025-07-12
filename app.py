import streamlit as st
import pandas as pd
from preprocessing import preprocess_text
from model import train_model, evaluate_model
from utils import show_wordcloud, plot_distribution

st.title("Analisis Sentimen Otomatis")

uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview Dataset")
    st.write(df.head())

    if st.button("Hapus Duplikat"):
        df.drop_duplicates(inplace=True)
        st.success("Duplikat dihapus!")

    st.subheader("Preprocessing")
    df['clean_text'] = df['teks'].apply(preprocess_text)
    st.write(df[['teks', 'clean_text']].head())

    st.subheader("Labeling Otomatis")
    from textblob import TextBlob
    df['sentimen'] = df['clean_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['label'] = df['sentimen'].apply(lambda x: 'positif' if x > 0 else ('negatif' if x < 0 else 'netral'))
    st.write(df[['clean_text', 'sentimen', 'label']].head())

    st.subheader("Training Model")
    model, X_test, y_test, y_pred = train_model(df)
    acc, prec, cm = evaluate_model(y_test, y_pred)

    st.write(f"Accuracy: {acc:.2f}, Precision: {prec:.2f}")
    st.write("Confusion Matrix:")
    st.write(cm)

    st.subheader("Visualisasi")
    show_wordcloud(df['clean_text'])
    plot_distribution(df['label'])

    st.download_button("Download Data", df.to_csv(index=False), file_name='hasil_sentimen.csv')
