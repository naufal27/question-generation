from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import instaloader
from itertools import dropwhile, takewhile
import os
import json
import pandas as pd
import re
import string
import numpy as np
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import time
from datetime import timedelta
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'iep'
# app.config['SESSION_PERMANENT'] = True

### FUNCTION USES ###


def emojify(text):
    regex = re.compile(pattern="["
                       u"\U0001F600-\U0001F64F"  # emoticons
                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       u"\U00002500-\U00002BEF"  # chinese char
                       u"\U00002702-\U000027B0"
                       u"\U00002702-\U000027B0"
                       u"\U000024C2-\U0001F251"
                       u"\U0001f926-\U0001f937"
                       u"\U00010000-\U0010ffff"
                       u"\u2640-\u2642"
                       u"\u2600-\u2B55"
                       u"\u200d"
                       u"\u0101"
                       u"\u00b2"
                       u"\u23cf"
                       u"\u23e9"
                       u"\u231a"
                       u"\ufe0f"  # dingbats
                       u"\u3030"
                       "]+",
                       flags=re.UNICODE)
    return regex.sub(r'', text)


def decode(text):
    processed = text.lower()
    processed = processed.encode('ascii', 'ignore')
    processed = processed.decode()
    return processed


def line_att(text):
    processed = text
    processed = processed.replace('.', '_')    # change dot with underscore
    processed = processed.replace('\n', ' ')    # change newline with space
    processed = processed.replace('\t', ' ')    # change tab with space
    return processed


def mention(text):
    return re.sub(r"@\w+", " ", text)   # remove mention


def hashtag(text):
    return re.sub(r"#\w+", " ", text)   # remove hashtag


def arabic(text):
    return re.sub(r"[ء-ي]\w+", " ", text)  # remove arabic letters


def double_word(text):
    return re.sub(r"\b(\w+)(2)\b(?<!s2)",
                  lambda match: match.group(1)+" "+match.group(1), text)


def punctuation(text):
    return text.translate(str.maketrans(
        "", "", string.punctuation))   # remove punctuation


def remoji(text):
    return emojify(text)  # remove emoji


def space(text):
    processed = text.strip()   # remove whitespace start and end
    processed = " ".join(re.split("\s+", processed, flags=re.UNICODE))
    return processed


def just_number(text):
    kalimat_tanpa_nomor = ''.join(
        karakter for karakter in text if not karakter.isdigit())
    return kalimat_tanpa_nomor


def single_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)  # remove single char


def rename(text):
    hasil = re.sub(r'span ptkin\b', 'spanptkin', text)
    hasil = re.sub(r'span\b', 'spanptkin', hasil)
    hasil = re.sub(r'um ptkin\b', 'umptkin', hasil)
    hasil = re.sub(r'\bum\b', 'umptkin', hasil)
    return hasil


def space(text):
    processed = text.strip()   # remove whitespace start and end
    processed = " ".join(re.split("\s+", processed, flags=re.UNICODE))
    return processed


def de_tokenize(text):
    return TreebankWordDetokenizer().detokenize(text)


def tokenize(text):
    return nltk.tokenize.word_tokenize(text)


def stemming(text):
    hasil = []
    for word in text:
        stem = StemmerFactory().create_stemmer().stem(word)
        hasil.append(stem)
    return hasil


def replace(text):
    hasil = re.sub(r'\bgimana\b', 'bagaimana', text)
    hasil = re.sub(r'\bgmn\b', 'bagaimana', hasil)
    hasil = re.sub(r'\bnunggu\b', 'kapan', hasil)
    hasil = re.sub(r'\bknpa\b', 'kenapa', hasil)
    hasil = re.sub(r'\bmengapa\b', 'kenapa', hasil)
    hasil = re.sub(r'\bto do list\b', 'bagaimana', hasil)
    hasil = re.sub(r'\bemg\b', 'apa', hasil)
    hasil = re.sub(r'\bemang\b', 'apa', hasil)
    hasil = re.sub(r'\bmana\b', 'dimana', hasil)
    hasil = re.sub(r'\bdmna\b', 'dimana', hasil)
    hasil = re.sub(r'\bbiaya\b', 'berapa', hasil)
    return hasil


stopword_nltk = stopwords.words('indonesian')
stopword_sastrawi = StopWordRemoverFactory().get_stop_words()
tambahan = [
    'uin', 'bandung', 'sgd', 'innalillahi', 'wa', 'inna', 'sunan', 'gunung', 'djati', 'innailaihi', 'kalo',
    'ilaihi', 'min', 'masya', 'allah', 'rojiun', 'ga', 'hatur', 'nuhun', 'nya', 'kasih', 'husnul', 'khotimah',
    'wainna', 'syaa', 'selamat', 'keren', 'banget', 'jalan', 'na', 'waafihi', 'wafuanhu', 'iya', 'nih',
    'dm', 'assalamualaikum', 'kak', 'warhamhu', 'century', 'girl', 'proud', 'of', 'maaf', 'yg', 'ka', 'hallo', 'yaa',
    'nyaa', 'kakak', 'klau', 'klo', 'yah', 'deh', 'sy', 'udh', 'mah', 'wakakakakakakak', 'yahhh', 'bgt', 'sih', 'hehehe',
    'minn'
]
all_stopword = stopword_nltk + stopword_sastrawi + tambahan
all_stopword = set(all_stopword)
kecuali = {'apa', 'siapa', 'kapan', 'mengapa',
           'bagaimana', 'dimana', 'berapa', 'kenapa'}
stopword_ex = all_stopword - kecuali


def stopword_for_ngram(text):
    all_stopword = stopword_nltk + stopword_sastrawi + tambahan
    all_stopword = set(all_stopword)
    return [word for word in text if word not in all_stopword]


def stopword_for_tf(text):
    return [word for word in text if word not in stopword_ex]


### END OF FUNCTION ###

folder_path = "uinsgd.official_comments"
folder_preparation = "preparation"


def scrape(tanggal1t, tanggal1m, tanggal1d, tanggal2t, tanggal2m, tanggal2d):
    ### SCRAPING ###
    L = instaloader.Instaloader(download_pictures=False, download_videos=False,
                                download_video_thumbnails=False, download_comments=True, compress_json=False, save_metadata=False)
    L.load_session_from_file(username="mwafa89k", filename="session-mwafa89k")
    profile = "uinsgd.official"
    posts = instaloader.Profile.from_username(L.context, profile).get_posts()

    UNTIL = datetime(tanggal2t, tanggal2m, tanggal2d)
    SINCE = datetime(tanggal1t, tanggal1m, tanggal1d)

    start_time = time.time()
    for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
        date_post = post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")
        path_txt = os.path.join(folder_path, date_post+"_UTC.txt")
        path_comment = os.path.join(
            folder_path, date_post+"_UTC_comments.json")
        if not (os.path.exists(path_comment)):
            L.download_post(post, "uinsgd.official_comments")
            preparation(path_comment)
    finish_time = time.time()
    print('Proses Scraping and Preparation')
    print('Finish dalam waktu : {}'.format(
        timedelta(seconds=finish_time-start_time)))
    print('Scraping and Preparation Done...')


def merge_file(tanggal1t, tanggal1m, tanggal1d, tanggal2t, tanggal2m, tanggal2d):
    data = []

    since_time = datetime.strptime(
        f'{tanggal1t}-{tanggal1m:02d}-{tanggal1d:02d}', '%Y-%m-%d')
    until_time = datetime.strptime(
        f'{tanggal2t}-{tanggal2m:02d}-{tanggal2d:02d}', '%Y-%m-%d')

    files_json = [comment_json for comment_json in os.listdir(
        folder_preparation + '/uinsgd.official_comments')]

    selected_json_files = []
    for json_file in files_json:
        file_time_str = json_file.split('_')[0]
        file_time = datetime.strptime(file_time_str, '%Y-%m-%d')
        if since_time <= file_time <= until_time:
            with open(folder_preparation+'/uinsgd.official_comments/'+json_file) as file:
                jl = json.load(file)
                data.extend(jl)
            selected_json_files.append(json_file)

    df = pd.DataFrame(data)
    return df


def preparation(path_comment):
    if not (os.path.exists(path_comment)):
        return
    data = []
    with open(path_comment) as file:
        jl = json.load(file)
        data.extend(jl)
    for i, d in enumerate(data):
        if not d['answers']:
            data[i]['answers'] = [{'answers': [{}]}]

    normalized_1 = pd.json_normalize(data)
    normalized_2 = pd.json_normalize(normalized_1.to_dict(
        orient='records'), meta=['text'], record_path='answers', record_prefix='answer_')
    normalized_2['text'] = normalized_2['text'].drop_duplicates()
    comments = pd.DataFrame({'text': normalized_2['text']})

    if 'answer_text' in normalized_2.columns:
        answers_comment = pd.DataFrame({'text': normalized_2['answer_text']})
        df = pd.concat([comments, answers_comment], ignore_index=True)
    else:
        df = comments

    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    ### CLEANSING ###
    df['text'] = df['text'].apply(decode)
    df['text'] = df['text'].apply(line_att)
    df['text'] = df['text'].apply(mention)
    df['text'] = df['text'].apply(hashtag)
    df['text'] = df['text'].apply(arabic)
    df['text'] = df['text'].apply(double_word)
    df['text'] = df['text'].apply(just_number)
    df['text'] = df['text'].apply(punctuation)
    df['text'] = df['text'].apply(single_char)
    df['text'] = df['text'].apply(remoji)
    df['text'] = df['text'].apply(rename)
    df['text'] = df['text'].apply(space)
    df.replace('', np.nan, inplace=True)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    # print('Cleansing Done...')

    ### STOPWORD ###
    df['text'] = df['text'].apply(tokenize)
    df['text'] = df['text'].apply(stopword_for_tf)
    df['text'] = df['text'].apply(de_tokenize)
    df['text'] = df['text'].apply(space)
    df.replace('', np.nan, inplace=True)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    # print('Stopwords Done...')

    ### STEMMING ###
    df['text'] = df['text'].apply(tokenize)
    df['text'] = df['text'].apply(stemming)
    # print('Stemming Done...')

    df.to_json(folder_preparation + '/' + path_comment,
               orient='records', indent=4)


def modeling(df):
    ### NGRAM ###
    df_ngram = df.copy()
    df_tf = df.copy()
    df_ngram['text'] = df_ngram['text'].apply(stopword_for_ngram)
    df_ngram['text'] = df_ngram['text'].apply(de_tokenize)

    c_vec1 = CountVectorizer(ngram_range=(2, 2))
    ngrams1 = c_vec1.fit_transform(df_ngram['text'])
    count_values1 = ngrams1.toarray().sum(axis=0)
    vocab1 = c_vec1.vocabulary_
    df_bigram = pd.DataFrame(sorted([(count_values1[i], k) for k, i in vocab1.items(
    )], reverse=True)).rename(columns={0: 'frekuensi', 1: 'bigram'})

    bigram_ignored = ['dies natalis', 'akun official',
                      'jurus hukum', 'kampus cinta', 'info daftar', 'daftar jalur', 'buka daftar']
    bigram_result = df_bigram[~df_bigram['bigram'].isin(bigram_ignored)]
    bigram_result = bigram_result.head(7)
    print(bigram_result)

    df_tf['text'] = df_tf['text'].apply(de_tokenize)
    comments_filtered_bigram = {}
    bigram_result = bigram_result['bigram'].values.tolist()
    for item in bigram_result:
        comments_filtered = df_tf[df_tf['text'].str.contains(item)]
        comments = comments_filtered['text'].values.tolist()
        if item == "uji mandiri":
            comments_filtered_bigram["ujian mandiri"] = comments
            continue
        comments_filtered_bigram[item] = comments
    for k, n in enumerate(bigram_result):
        if n == "uji mandiri":
            bigram_result[k] = "ujian mandiri"
    # print('Ngram Done...')

    ### REPLACE ###
    replace_bigram = pd.DataFrame(columns=['bigram', 'comments'])
    for key, values in comments_filtered_bigram.items():
        temp_df = pd.DataFrame({'bigram': key, 'comments': values})
        replace_bigram = pd.concat(
            [replace_bigram, temp_df], ignore_index=True)
    replace_bigram['comments'] = replace_bigram['comments'].apply(replace)
    # print('Replace Done...')

    ### GENERATE QUESTION ###
    question_words = ["siapa", "apa", "kapan",
                      "dimana", "kenapa", "bagaimana", "berapa"]
    bigram_quesgen = {}
    for n in bigram_result:
        addons = ""
        word = {}
        for q in question_words:
            if q == 'bagaimana':
                addons = " cara"
            elif q == "berapa":
                addons = " biaya"
            elif q == "kenapa":
                addons = ""
                if n == "bayar ukt":
                    addons = " di indomaret tidak bisa"
            elif q == "dimana":
                addons = ""
                if n == "jalur umptkin" or n == "ujian mandiri" or n == "jalus spanptkin":
                    addons = " informasi tentang"
            elif q == "kapan":
                addons = " dibuka"
            elif q == "apa":
                addons = ""
                if n == "jalur snbp":
                    addons = " jurusan yang terdaftar pada"
                elif n == "ujian mandiri":
                    addons = " materi"
                elif n == "jalur mandiri":
                    addons = " saja informasi tentang"
                elif n == "bayar ukt" or n == "daftar wisuda":
                    addons = " kendala"
            elif q == "siapa":
                addons = ""
            sementara = q + addons + " " + n + "?"
            word[q] = sementara
        bigram_quesgen[n] = word
    # print('Generate Question Done...')

    ### TERM FREQUENCY ###
    frekuensi_kata = {}
    for n in bigram_result:
        frekuensi_kata[n] = {}
        for word in question_words:
            test = []
            sementara = 0
            for index, row in replace_bigram.iterrows():
                if row['bigram'] == n:
                    dt = row['comments'].split()
                    if word in dt:
                        sementara += 1
                        test.append(row['comments'])
            frekuensi_kata[n][word] = {
                'frekuensi': sementara, 'comment': test}
    for objek, subobjek in frekuensi_kata.items():
        subobjek_baru = dict(
            sorted(subobjek.items(), key=lambda x: x[1]['frekuensi'],
                   reverse=True)[:3])
        subobjek_baru = {k: v for k, v in subobjek_baru.items()
                         if v['frekuensi'] != 0}
        frekuensi_kata[objek] = subobjek_baru
    # print('Term Frequency Done...')

    ### COSINE SIMILARITY ###
    end_result = {}
    for ngram, qw in frekuensi_kata.items():
        # print(ngram)
        list_qg = []
        for sub_qw, fre_com in qw.items():
            for d_ngram, d_qw in bigram_quesgen.items():
                for key, value in d_qw.items():
                    if d_ngram == ngram:
                        if sub_qw == key:
                            list_qg.append(value)
                            comment = fre_com['comment']
                            qg = [value]
                            vectorizer = CountVectorizer()
                            tfidf_matrix = vectorizer.fit_transform(comment)
                            tfidf_kalimat = vectorizer.transform(qg)
                            cos_sim = cosine_similarity(
                                tfidf_kalimat, tfidf_matrix)

                            # for j in range(len(qg)):
                            # print(sub_qw)
                            # print('Generate:', qg[j])
                            # for i in range(len(comment)):
                            #                                 if max(cos_sim[j]) == cos_sim[j][i]:
                            # print('TF:', comment[i])
                            # print('Cosine Similarity:', cos_sim[j][i])
                            # print()
        end_result[ngram] = list_qg
    print('Modeling Done...')
    return end_result

# Running


def run_nlp_model(tanggal1t, tanggal1m, tanggal1d, tanggal2t, tanggal2m, tanggal2d):
    model_start = time.time()

    scrape(tanggal1t, tanggal1m, tanggal1d,
           tanggal2t, tanggal2m, tanggal2d)
    merged_files = merge_file(tanggal1t, tanggal1m,
                              tanggal1d, tanggal2t, tanggal2m, tanggal2d)
    modelled = modeling(merged_files)
    model_end = time.time()
    print('Waktu yang Dibutuhkan Sistem : {}'.format(
        timedelta(seconds=model_end-model_start)))
    return modelled


def cron_job():
    scheduler = BackgroundScheduler(daemon=True)

    def tanggal_now():
        return datetime.now().date()

    scheduler.add_job(scrape, 'cron', args=[tanggal_now(
    ).year, tanggal_now().month, (tanggal_now().day - 1), tanggal_now(
    ).year, tanggal_now().month, tanggal_now().day], hour=23, minute=59)
    scheduler.start()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

### ROUTES ###


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.username.data == 'iep' and form.password.data == 'sakti':
            session['logged_in'] = True
            return redirect(url_for('admin'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/')
def public():
    return render_template('public.html')


@app.route('/get-hasil', methods=['GET'])
def get_hasil():
    hasil_data = session.get('hasil')
    if hasil_data:
        return jsonify(hasil_data)
    else:
        return jsonify({"Not Found": "Data tidak ditemukan"})


@app.route('/kirim-tanggal', methods=['POST'])
def kirim_tanggal():
    data = request.json
    tanggal1 = data.get('tanggal1')
    tanggal2 = data.get('tanggal2')

    tanggal1 = datetime.strptime(tanggal1, "%Y-%m-%d")
    tanggal1t = tanggal1.year
    tanggal1m = tanggal1.month
    tanggal1d = tanggal1.day
    tanggal2 = datetime.strptime(tanggal2, "%Y-%m-%d")
    tanggal2t = tanggal2.year
    tanggal2m = tanggal2.month
    tanggal2d = tanggal2.day

    hasil = run_nlp_model(tanggal1t, tanggal1m, tanggal1d,
                          tanggal2t, tanggal2m, tanggal2d)
    session['hasil'] = hasil
    return jsonify(hasil)


if __name__ == '__main__':
    cron_job()
    app.run()
