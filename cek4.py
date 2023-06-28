from sklearn.feature_extraction.text import TfidfVectorizer

# Dokumen yang diberikan
dokumen = [
    # "dokumen1 ini contoh",
    # "ini dokumen2 contoh",
    # "ini contoh dokumen3"
    "bayar ukt kapan ya",  # kapan
    "klo ngga sekarang bayar ukt bisa kapan min",  # kapan
    "kapan mulai berlaku bayar ukt",  # kapan
    "jika sudah lewat masa pembayaran, kapan lagi bisa bayar ukt",  # kapan
]

# Inisialisasi objek TfidfVectorizer
vectorizer = TfidfVectorizer()

# Melakukan fitting dan transformasi pada dokumen
tfidf_matrix = vectorizer.fit_transform(dokumen)

# Mendapatkan daftar kata yang dijadikan fitur
fitur = vectorizer.get_feature_names_out()

# Mencetak skor TF-IDF untuk setiap kata dalam setiap dokumen
for i in range(len(dokumen)):
    print("Dokumen ", i+1)
    for j in range(len(fitur)):
        kata = fitur[j]
        skor_tfidf = tfidf_matrix[i, j]
        print("Kata:", kata, " - Skor TF-IDF:", skor_tfidf)
    print()
print(fitur)
print(tfidf_matrix)
