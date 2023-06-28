from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Contoh DataFrame dengan kolom 'dokumen'
df = pd.DataFrame({'dokumen': [
    "bayar ukt kapan ya",  # kapan
    "klo ngga sekarang bayar ukt bisa kapan min",  # kapan
    "bayar ukt berapa sih",  # berapa
    "kapan mulai berlaku bayar ukt",  # kapan
    "jika sudah lewat masa pembayaran, kapan lagi bisa bayar ukt",  # kapan
    "dimana aku bisa bayar ukt",  # dimana
    "min berapa biaya untuk bayar ukt semester 2",  # berapa
    "saya harus bayar ukt, mengapa",  # mengapa
    "bagaimana cara saya bayar ukt",  # bagaimana
]})

# List kalimat yang ingin dihitung TF-IDF-nya
kalimat = ["siapa bayar ukt?",
           "apa bayar ukt?",
           "kapan bayar ukt?",
           "dimana bayar ukt?",
           "berapa bayar ukt?",
           "mengapa bayar ukt?",
           "bagaimana bayar ukt?",
           ]

# Menggunakan TfidfVectorizer untuk menghitung TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['dokumen'])

# Menghitung nilai TF-IDF untuk setiap kalimat
tfidf_kalimat = vectorizer.transform(kalimat)

# Menampilkan hasil perhitungan TF-IDF
# for i, kalimat in enumerate(kalimat):
#     feature_names = vectorizer.get_feature_names_out()
#     tfidf_scores = tfidf_kalimat[i].toarray().flatten()
#     df_tfidf = pd.DataFrame({'Kata': feature_names, 'TF-IDF': tfidf_scores})
#     print('Kalimat:', kalimat)
#     print(df_tfidf)
#     print()


# Menghitung cosine similarity
cos_sim = cosine_similarity(tfidf_kalimat, tfidf_matrix)
# print(cos_sim)
# Menampilkan hasil cosine similarity
# pertama
# for i, kalimat in enumerate(kalimat):
#     df_cos_sim = pd.DataFrame(
#         {'Dokumen': df['dokumen'], 'Cosine Similarity': cos_sim[i]})
#     df_cos_sim = df_cos_sim.sort_values(
#         by='Cosine Similarity', ascending=False).reset_index(drop=True)
#     print('Kalimat:', kalimat)
#     print(df_cos_sim)
#     print()
# kedua
# for i in range(len(kalimat)):
#     print('Kalimat:', kalimat[i])
#     for j in range(len(df['dokumen'])):
#         print('Dokumen:', df['dokumen'][j])
#         print('Cosine Similarity:', cos_sim[i][j])
#         print()
# ketiga
# for i in range(len(kalimat)):
#     max_sim = max(cos_sim[i])
#     max_index = cos_sim[i].argmax()
#     max_kalimat = df['dokumen'][max_index]
#     print('Kalimat:', kalimat[i])
#     print('Skor Cosine Similarity Terbesar:', max_sim)
#     print('Kalimat Terbaik:', max_kalimat)
#     print()
# empat
# for i in range(len(kalimat)):
#     max_index = cos_sim[i].argmax()
#     max_kalimat = df['dokumen'][max_index]
#     print('Kalimat:', kalimat[i])
#     print('Kalimat Terbaik:', max_kalimat)
#     print()
# lima
print(cos_sim)
max_sim = -1
max_index = -1
for i in range(len(kalimat)):
    if max(cos_sim[i]) > max_sim:
        max_sim = max(cos_sim[i])
        max_index = i

kalimat_terbaik = kalimat[max_index]
print('Kalimat dengan Cosine Similarity Paling Besar:', kalimat_terbaik)
print('Skor Cosine Similarity:', max_sim)
# dies natalis
# akun official
# jurusan hukum
# wedding venue
# 3
