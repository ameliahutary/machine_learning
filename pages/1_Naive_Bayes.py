import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

st.title("🤖 Naive Bayes Sentiment Classification")

uploaded_file = st.file_uploader("Upload CSV (dengan kolom: full_text dan label)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower()

    if 'full_text' not in df.columns or 'label' not in df.columns:
        st.error("CSV harus mengandung kolom 'full_text' dan 'label'")
    else:
        df['clean_text'] = df['full_text'].apply(preprocess)

        # WordCloud
        st.subheader("☁️ WordCloud")
        all_words = ' '.join(df['clean_text'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Vectorization & Split
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df['clean_text'])
        y = df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model
        model = MultinomialNB()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Metrics
        st.subheader("📊 Evaluation")
        st.write(f"**Accuracy:** {accuracy_score(y_test, y_pred):.2f}")
        st.write(f"**Precision:** {precision_score(y_test, y_pred, average='weighted', zero_division=0):.2f}")
        st.write("**Confusion Matrix:**")
        st.write(confusion_matrix(y_test, y_pred))

        # Preview
        st.subheader("🔍 Sample Prediction")
        sample = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}).reset_index(drop=True)
        st.dataframe(sample.head())

        # Download
        df_result = df[['full_text', 'clean_text']].copy()
        df_result['label'] = y
        df_result['predicted'] = model.predict(X)
        csv = df_result.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Prediction CSV", csv, "nb_predictions.csv", "text/csv")
