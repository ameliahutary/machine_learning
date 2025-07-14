import streamlit as st
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

nltk.download('punkt')
nltk.download('stopwords')

st.title("📊 Naive Bayes Classification")

uploaded_file = st.file_uploader("📤 Upload file CSV berlabel (full_text & label)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📄 Preview data:")
    st.dataframe(df.head())

    stop_words = set(stopwords.words('english'))

    def clean(text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"@\w+", "", text)
        text = re.sub(r"#", "", text)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        text = text.lower()
        tokens = word_tokenize(text)
        filtered = [word for word in tokens if word not in stop_words]
        return ' '.join(filtered)

    df['clean_text'] = df['full_text'].astype(str).apply(clean)

    X = df['clean_text']
    y = df['label']

    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    st.subheader("📈 Evaluasi Model")
    report = classification_report(y_test, y_pred, output_dict=True)
    st.dataframe(pd.DataFrame(report).transpose())

    st.subheader("🔁 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=model.classes_, yticklabels=model.classes_)
    st.pyplot(fig)

    st.subheader("☁️ WordCloud dari Data")
    text_all = ' '.join(df['clean_text'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_all)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)
