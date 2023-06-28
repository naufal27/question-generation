from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pandas as pd

# Daftar dokumen yang digunakan untuk perhitungan TF-IDF
ft = open('ngram.json')
ft2 = json.load(ft)
df = pd.DataFrame.from_dict(ft2, orient='index').transpose()
print(df.info())

# # Kalimat yang ingin dihitung TF-IDF-nya
# kalimat = "Ini adalah kalimat yang ingin dihitung TF-IDF-nya."

# # Inisialisasi objek TfidfVectorizer
# tfidf_vectorizer = TfidfVectorizer()

# # Menghitung bobot TF-IDF dari dokumen
# tfidf_matrix = tfidf_vectorizer.fit_transform(dokumen)

# # Mengubah kalimat menjadi vektor TF-IDF
# kalimat_vector = tfidf_vectorizer.transform([kalimat])

# # Mendapatkan daftar fitur kata dari vektor TF-IDF
# fitur_kata = tfidf_vectorizer.get_feature_names()

# # Menampilkan bobot TF-IDF untuk setiap kata dalam kalimat
# for i, feature in enumerate(fitur_kata):
#     tfidf_score = kalimat_vector[0, i]
#     if tfidf_score > 0:
#         print("Kata: {}, Bobot TF-IDF: {:.4f}".format(feature, tfidf_score))
