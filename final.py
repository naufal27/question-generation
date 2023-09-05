from itertools import dropwhile, takewhile
from datetime import datetime
import instaloader
from flask import Flask, request, jsonify
import time  # Digunakan untuk mensimulasikan waktu yang dibutuhkan model

app = Flask(__name__)

# Simulasikan fungsi untuk menjalankan model NLP


def run_nlp_model(since, until):
    ### scrape ###
    L = instaloader.Instaloader(download_pictures=False, download_videos=False,
                                download_video_thumbnails=False, download_comments=True, compress_json=False, save_metadata=False)
    L.load_session_from_file(username="gralam27", filename="session-gralam27")
    profile = "uinsgd.official"
    posts = instaloader.Profile.from_username(L.context, profile).get_posts()

    UNTIL = datetime(2023, 5, 31)
    SINCE = datetime(2022, 9, 1)

    for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
        L.download_post(post, "coba")

    ### cleansing ###

    return "berhasil"


@app.route('/jalankan-model', methods=['POST'])
def jalankan_model():
    try:
        data = request.json
        input_text = data['teks']  # Ambil teks dari data yang dikirimkan

        hasil = run_nlp_model(input_text)  # Jalankan model NLP

        return jsonify({'hasil': hasil}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
