import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download resource NLTK (hanya perlu sekali)
nltk.download('punkt')
nltk.download('stopwords')

# Baca file CSV
df = pd.read_csv('enhypen.csv')

# Ubah nama kolom ke huruf kecil agar aman
df.columns = df.columns.str.lower()

# Inisialisasi stemmer dan stopwords
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stop_words = set(stopwords.words('indonesian'))

# Fungsi preprocessing lengkap
def preprocess(text):
    if pd.isnull(text):
        return ''
    
    # 1. Hapus URL
    text = re.sub(r'http\S+', '', text)

    # 2. Hapus mention (@username)
    text = re.sub(r'@\w+', '', text)

    # 3. Hapus simbol #, tapi simpan katanya
    text = re.sub(r'#', '', text)

    # 4. Hapus angka dan karakter non-huruf
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # 5. Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()

    # 6. Ubah ke huruf kecil
    text = text.lower()

    # 7. Tokenizing
    tokens = word_tokenize(text)

    # 8. Filtering (hapus stopwords)
    filtered = [word for word in tokens if word not in stop_words]

    # 9. Stemming
    stemmed = [stemmer.stem(word) for word in filtered]

    return ' '.join(stemmed)

# Terapkan preprocessing ke kolom 'full_text'
df['teks_bersih'] = df['full_text'].apply(preprocess)

# Tampilkan 5 hasil pertama
print(df[['full_text', 'teks_bersih']].head())

# Simpan ke file baru
df.to_csv('data_preprocessed.csv', index=False)
print("\n✅ Data berhasil diproses dan disimpan sebagai 'data_preprocessed.csv'")
