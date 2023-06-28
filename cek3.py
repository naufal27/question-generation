# Dokumen yang diberikan
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
    "apakah sidang munaqosah februari bayar ukt",
    "bayar ukt gabisa indomaret sy udh indo tpi gabisa kenapa",
    "apakah bisa cicil bayar ukt",
    "nau bayar ukt cicil bagaimana",
    "bagaimana cara bayar ukt",
    "syukur lulus biar bayar ukt",
    "bayar ukt gabisa indomaret sy udh bulak indo tpi gabisa",
    "apakah yg udh bayar ukt tp akun salam terang bayar",
    "batas bayar ukt kapan",
    "bayar ukt bsi mobile gagal trs pdhl udh aktifin yg salam",
    "punten bayar ukt indomaret sial sy udh indo gabisa trs kenapa",
    "smg lancar rezekinyabisa bayar ukt waktuaamiin",
    "gak panjang bayar ukt uang gak bayar ukt",
    "panjang bayar ukt",
    "coba deh mindmap alur kurang ukt selesai kendala ukt kadang ormawa advokasi mentok wadek mahasiswa aljamiah akademik uang coba list apa aja perlu aju kurang ukt bagaimana telat bayar ukt uang kirakira apa bijak",
    "bayar ukt pake permen yupi hasil kembali warung ceu nonoh",
    "panjang bayar ukt hehe",
    "teh email mahasiswa butuh kontak ptipd langsung respon apaapa tindak lanjut maha ieu teh palayanna bayar ukt loh",
    "nanya masalah bayar ukt telat bayar bayar ukt yg lewat batas jadwal bayar krs",
    "yg gk bayar ukt ky yah",
    "apakah bayar ukt telat yah",
    "apakah assalamualaikummaaf lulus terima angkat bayar dri tgl telat bayar ukt tgl",
    "terima bayar ukt jalur spanptkin ngapain yaa",
    "ah gara telat bayar ukt hari aja maba gagal masuk segitu tega",
    "bener daftar sidang kuliah semester genap feb mahasiswa ikut sidang bayar ukt semester genap kalo sidang gak bayar uktnya nyusul luar periode bayar ukt",
    "afwanjika kendala bayar ukt telat bagaimana",
    "lu telat bayar ukt bang",
    "bayar ukt dlu bang"
]

# Menghitung frekuensi kemunculan kata dalam setiap dokumen
frekuensi_kata = {}
for doc in dokumen:
    kata = doc.split()
    for word in kata:
        if word in frekuensi_kata:
            frekuensi_kata[word] += 1
        else:
            frekuensi_kata[word] = 1

# Mengurutkan kata berdasarkan frekuensinya dari yang terbesar
kata_terurut = sorted(frekuensi_kata.items(), key=lambda x: x[1], reverse=True)

# Menampilkan kata-kata yang diurutkan
for word, freq in kata_terurut:
    print("Kata:", word, " - Skor frekuensi:", freq)
