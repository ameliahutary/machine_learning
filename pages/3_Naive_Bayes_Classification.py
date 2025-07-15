import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Naive Bayes Classification", layout="wide")
st.title("📊 Naive Bayes Classification & Sentiment Evaluation")

uploaded_file = st.file_uploader("📤 Upload file hasil preprocessing dan labelling (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {'clean_text', 'label'}

    if not required_cols.issubset(df.columns):
        st.error("⚠️ File harus memiliki kolom 'clean_text' dan 'label'.")
    else:
        st.write("📄 Preview Data:")
        st.dataframe(df[['clean_text', 'label']].head())

        # Split data
        X = df['clean_text']
        y = df['label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # TF-IDF
        vectorizer = TfidfVectorizer()
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        # Naive Bayes model
        model = MultinomialNB()
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)

        # Evaluasi
        st.subheader("📈 Classification Report:")
        report = classification_report(y_test, y_pred, output_dict=True)
        st.dataframe(pd.DataFrame(report).transpose())

        st.subheader("🧾 Confusion Matrix:")
        cm = confusion_matrix(y_test, y_pred, labels=["positive", "neutral", "negative"])
        cm_df = pd.DataFrame(cm, columns=["Predicted Pos", "Predicted Neu", "Predicted Neg"],
                                index=["Actual Pos", "Actual Neu", "Actual Neg"])
        st.dataframe(cm_df)

        # Simpan hasil prediksi
        df_test = pd.DataFrame(X_test)
        df_test['actual_label'] = y_test.values
        df_test['predicted_label'] = y_pred
        st.subheader("🔍 Contoh Hasil Prediksi:")
        st.dataframe(df_test.head())

        # Download hasil prediksi
        st.download_button(
            label="⬇️ Download hasil prediksi",
            data=df_test.to_csv(index=False).encode('utf-8'),
            file_name="naive_bayes_predictions.csv",
            mime="text/csv"
        )

        # WordCloud positif dan negatif
        st.subheader("☁️ WordCloud per Sentimen")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Positive Words**")
            pos_text = ' '.join(df[df['label'] == 'positive']['clean_text'])
            if pos_text:
                wordcloud_pos = WordCloud(width=400, height=300, background_color='white').generate(pos_text)
                fig1, ax1 = plt.subplots()
                ax1.imshow(wordcloud_pos, interpolation='bilinear')
                ax1.axis('off')
                st.pyplot(fig1)
            else:
                st.write("Tidak ada data sentimen positif.")

        with col2:
            st.markdown("**Negative Words**")
            neg_text = ' '.join(df[df['label'] == 'negative']['clean_text'])
            if neg_text:
                wordcloud_neg = WordCloud(width=400, height=300, background_color='white').generate(neg_text)
                fig2, ax2 = plt.subplots()
                ax2.imshow(wordcloud_neg, interpolation='bilinear')
                ax2.axis('off')
                st.pyplot(fig2)
            else:
                st.write("Tidak ada data sentimen negatif.")
