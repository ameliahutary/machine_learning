import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download resource NLTK (hanya perlu dijalankan sekali)
nltk.download('punkt')
nltk.download('stopwords')

# Baca file CSV
df = pd.read_csv('enhypen_id.csv')

# Ubah nama kolom ke lowercase
df.columns = df.columns.str.lower()

# Set stopwords bahasa Inggris
stop_words = set(stopwords.words('indonesian'))

# Fungsi preprocessing untuk teks Inggris
def preprocess(text):
    if pd.isnull(text):
        return ''
    
    # 1. Remove URLs
    text = re.sub(r'http\S+', '', text)

    # 2. Remove mentions (@username)
    text = re.sub(r'@\w+', '', text)

    # 3. Remove hashtags symbol '#' but keep the word
    text = re.sub(r'#', '', text)

    # 4. Remove numbers and non-letter characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 5. Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # 6. Lowercase
    text = text.lower()

    # 7. Tokenizing
    tokens = word_tokenize(text)

    # 8. Remove stopwords
    filtered = [word for word in tokens if word not in stop_words]

    # 9. Remove duplicate words (optional)
    unique_words = []
    for word in filtered:
        if word not in unique_words:
            unique_words.append(word)

    return ' '.join(unique_words)

# Terapkan preprocessing ke kolom 'full_text'
df['clean_text'] = df['full_text'].apply(preprocess)

# Pilih hanya kolom yang ingin disimpan
output_columns = ['full_text', 'clean_text']
df[output_columns].to_csv('data_bersih.csv', index=False)

print("\n✅ Preprocessing selesai. File disimpan sebagai 'data_cleaned.csv'")
