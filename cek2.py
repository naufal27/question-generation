from sklearn.feature_extraction.text import TfidfVectorizer

# Daftar dokumen dalam koleksi
dokumen = [
    # "bayar ukt kapan ya",  # kapan
    # "klo ngga sekarang bayar ukt bisa kapan min",  # kapan
    # "kapan mulai berlaku bayar ukt",  # kapan
    # "jika sudah lewat masa pembayaran, kapan lagi bisa bayar ukt",  # kapan
    # "bayar ukt berapa sih",  # berapa
    # "min berapa biaya untuk bayar ukt semester 2",  # berapa
    # "berapa nominal yang harus dikeluarkan untuk bayar ukt",  # berapa
    # "dimana aku bisa bayar ukt",  # dimana
    # "untuk bayar ukt dimana saya bisa melakukannya",  # dimana
    # "bagaimana cara saya bayar ukt",  # bagaimana
    "jalur mandiri kapan buka kakdaftar online offline",
    "nunggu jalur mandiri buka",
    "link jalur mandiri",
    "jalur mandiri jurusan apa aja yg dibuka",
    "jalur kip jalur mandiri",
    "yg lulusan daftar jalur mandiri please",
    "daftar jalur mandiri kapan",
    "jalur mandiri kapan",
    "nunggu jalur mandiri buka",
    "tes jalur mandiri calon mahasiswa pascasarjana sdh tutup",
    "umptkin jalur mandiri bukanmaaf tau",
    "jalur mandiri tesnya online apa offline",
    "assalamualaiakum admin lulusan daftar umptkin jalur mandiri",
    "mimin yg hatiuntuk jalur mandiri pake prestasi seni seandainya lolos beasiswa gitu",
    "jalur mandiri kapan buka",
    "berkas jalur mandiri apa aja",
    "jurusan apa ajah yg jalur mandiri",
    "kapan jalur mandiri buka",
    "jalur mandiri",
    "klo pendaftaran jalur mandiri tgl berapa",
    "pendaftaran jalur mandiri",
    "tau info jalur mandiri kapan",
    "emg jalur mandiri tahfiz gk yah",
    "jalur mandiri daftar engga lulusan",
    "jalur mandiri uang pendaftaran ukt apa biaya uang pangkal",
    "jalur mandiri ad uang pendaftaran ukt berapa",
    "jalur mandiri dibuka pendaftarannya tgl juni sd juli",
    "jalur mandiri jurusan",
    "jalur mandiri tersedia"
]

# Kalimat-kalimat yang akan dibandingkan
kalimat = [
    "kapan jalur mandiri?",
    "siapa jalur mandiri?",
    "apa jalur mandiri?",
    "dimana jalur mandiri?",
    "mengapa jalur mandiri?",
    "bagaimana jalur mandiri?",
    "berapa jalur mandiri?"
]

# Menghitung TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(dokumen)

# Mengubah kalimat-kalimat menjadi vektor TF-IDF
kalimat_vectors = vectorizer.transform(kalimat)

# Menghitung Jaccard Similarity


def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    return similarity


# Menghitung Jaccard Similarity antara setiap kalimat dan setiap dokumen dalam koleksi
jaccard_similarities = []
for i in range(kalimat_vectors.shape[0]):
    kalimat_vector = kalimat_vectors[i]
    similarity_scores = []
    for j in range(tfidf_matrix.shape[0]):
        dokumen_vector = tfidf_matrix[j]
        similarity = jaccard_similarity(
            set(kalimat_vector.nonzero()[1]), set(dokumen_vector.nonzero()[1]))
        similarity_scores.append(similarity)
    jaccard_similarities.append(similarity_scores)

# Menampilkan hasil
print("TF-IDF:")
for i in range(tfidf_matrix.shape[0]):
    print(f"Dokumen {i+1}: {tfidf_matrix[i]}")

print("\nJaccard Similarity:")
for i in range(len(jaccard_similarities)):
    sementara = 0
    for j in range(len(jaccard_similarities[i])):
        sementara = sementara+jaccard_similarities[i][j]
    print(f"Kalimat {i+1} hasil : {sementara}")
