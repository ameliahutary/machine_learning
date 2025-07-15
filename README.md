
# 🧠 Twitter Text Analysis (Crawling, Translate, Preprocessing & Classification)

[![issues](https://img.shields.io/github/issues/ameliahutary/machine_learning)](https://github.com/ameliahutary/machine_learning/issues)
[![language](https://img.shields.io/github/languages/count/ameliahutary/machine_learning)](https://github.com/ameliahutary/machine_learning/search)
[![top-language](https://img.shields.io/github/languages/top/ameliahutary/machine_learning)](https://github.com/ameliahutary/machine_learning/search)
[![commit](https://img.shields.io/github/commit-activity/m/ameliahutary/machine_learning)](https://github.com/ameliahutary/machine_learning/commits/main)
[![last-commit](https://img.shields.io/github/last-commit/ameliahutary/machine_learning)](https://github.com/ameliahutary/machine_learning/commits/main)

---

Proyek ini merupakan aplikasi berbasis **Streamlit** yang dirancang untuk menganalisis teks dari media sosial **Twitter (X)**. Aplikasi ini memiliki fitur mulai dari **pengambilan data (crawling)**, **penerjemahan**, **preprocessing**, hingga **klasifikasi sentimen**.

---

## 📌 Deskripsi Proyek

Dalam proyek ini, data dikumpulkan dari media sosial **Twitter (sekarang X)** menggunakan metode **web scraping** dengan bantuan tool **Tweet Harvest**, yang dijalankan melalui platform **Google Colaboratory (Colab)**.

Tweet Harvest merupakan sebuah **package berbasis Node.js** yang memungkinkan pengguna untuk mengambil tweet berdasarkan:
- Kata kunci (keyword)
- Rentang waktu (date range)
- Bahasa
- Jumlah data yang ditentukan

Setelah data berhasil diambil dalam bentuk `.csv`, aplikasi ini menyediakan serangkaian fitur lanjutan seperti:

- ✅ Penerjemahan otomatis (jika data berbahasa Indonesia atau lainnya)
- ✅ Pembersihan teks (preprocessing) dengan metode NLP
- ✅ Pelabelan sentimen menggunakan TextBlob
- ✅ Klasifikasi sentimen menggunakan algoritma Naive Bayes

---

## 🗂️ Struktur Folder

```
.
├── home.py                                # Halaman utama Streamlit
├── requirements.txt                       # Dependency Python
├── procfile                               # File untuk deployment (Heroku)
├── README.md                              # Dokumentasi proyek ini
├── pages/
│   ├── 1_Translate.py                     # Modul translasi otomatis
│   ├── 2_Preprocessing_and_Labelling.py  # Modul preprocessing + labelling sentimen
│   ├── 3_Naive_Bayes_Classification.py   # Modul klasifikasi Naive Bayes
│   └── Crawl_data_twitter.ipynb          # Notebook untuk scraping tweet via Tweet Harvest
```

---

## ⚙️ Teknologi & Library

- **Streamlit** – Antarmuka web interaktif
- **Pandas** – Pengolahan data
- **TextBlob** – Analisis sentimen
- **NLTK** – Natural Language Toolkit (preprocessing)
- **Scikit-learn** – Naive Bayes Classification
- **Deep Translator** – Translasi otomatis teks
- **Tweet Harvest** – Scraper tweet berbasis Node.js (dijalankan di Colab)

---

## 📥 Cara Menjalankan

### 1. Clone repositori ini:
```bash
git clone https://github.com/ameliahutary/machine_learning.git
cd twitter-text-analysis
```

### 2. Install dependency:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Streamlit:
```bash
streamlit run home.py
```

---

## 🧾 Cara Crawling Data di Colab

1. Buka file `Crawl_data_twitter.ipynb` di Google Colab  
2. Masukkan kata kunci, tanggal mulai, tanggal akhir, bahasa, dan jumlah tweet  
3. Jalankan perintah seperti:
```bash
!npx -y tweet-harvest@2.6.1 -o "enhypen.csv" -s "#enchella2025 since:2025-04-10 until:2025-04-30 lang:en" -l 500
```
4. Download file `.csv` dan upload ke aplikasi Streamlit untuk dianalisis

---

## 📊 Output Data

Hasil crawling dan analisis akan menghasilkan dataset dengan kolom:

| Kolom | Keterangan |
|-------|------------|
| `conversation_id_str` | ID percakapan |
| `created_at` | Tanggal dan waktu tweet |
| `favorite_count` | Jumlah like |
| `full_text` | Isi tweet |
| `id_str` | ID tweet |
| `image_url` | URL gambar (jika ada) |
| `in_reply_to_screen_name` | Username yang dibalas |
| `lang` | Bahasa |
| `location` | Lokasi user |
| `quote_count` | Jumlah quote |
| `reply_count` | Jumlah balasan |
| `retweet_count` | Jumlah retweet |
| `tweet_url` | Link langsung ke tweet |
| `user_id_str` | ID pengguna |
| `username` | Nama pengguna |

---

## 👤 Author

Dibuat oleh Ameliah Utary
📧 Email: ameliyyh12@email.com  
🔗 GitHub: [@ameliahutary](https://github.com/ameliahutary)

---

## 📄 Lisensi

Proyek ini tersedia di bawah lisensi **MIT**. Silakan digunakan untuk pembelajaran, penelitian, atau pengembangan lanjutan.

---
