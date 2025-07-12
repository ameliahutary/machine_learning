import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import streamlit as st

def show_wordcloud(text_series):
    wc = WordCloud(width=800, height=400).generate(" ".join(text_series))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def plot_distribution(labels):
    fig, ax = plt.subplots()
    labels.value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)
