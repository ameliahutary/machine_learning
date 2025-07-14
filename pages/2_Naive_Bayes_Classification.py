# pages/2_Classification_Naive_Bayes.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.title("📊 Klasifikasi Sentimen - Naive Bayes")

uploaded_file = st.file_uploader("📤 Upload file hasil preprocessing (wajib kolom 'clean_text' dan 'label')", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    if 'clean_text' not in df.columns or 'label' not in df.columns:
        st.error("❌ Kolom 'clean_text' dan 'label' harus ada.")
    else:
        # Split data
        X = df['clean_text']
        y = df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Train model
        model = MultinomialNB()
        model.fit(X_train_vec, y_train)

        # Predict
        y_pred = model.predict(X_test_vec)

        # Evaluation
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='macro')
        recall = recall_score(y_test, y_pred, average='macro')
        cm = confusion_matrix(y_test, y_pred, labels=['positive', 'neutral', 'negative'])

        st.subheader("📈 Hasil Evaluasi:")
        st.write(f"✅ **Accuracy:** {accuracy:.2f}")
        st.write(f"✅ **Precision:** {precision:.2f}")
        st.write(f"✅ **Recall:** {recall:.2f}")

        st.subheader("🧩 Confusion Matrix:")
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['positive', 'neutral', 'negative'], yticklabels=['positive', 'neutral', 'negative'], ax=ax)
        st.pyplot(fig)

        st.subheader("🔍 Contoh Prediksi:")
        hasil_df = pd.DataFrame({'clean_text': X_test, 'label_asli': y_test, 'label_prediksi': y_pred})
        st.dataframe(hasil_df.head())

st.subheader("🌐 WordCloud berdasarkan Sentimen")

# Gabungkan semua teks per label
for label in ['positive', 'neutral', 'negative']:
    st.markdown(f"#### {label.capitalize()}")

    text_kategori = ' '.join(df[df['label'] == label]['clean_text'].dropna())
    if text_kategori.strip():
        wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text_kategori)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning(f"Tidak ada data untuk kategori '{label}'")
