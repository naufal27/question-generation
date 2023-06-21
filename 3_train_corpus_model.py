import io
import time
from datetime import timedelta
from gensim.models import word2vec
import multiprocessing

start_time = time.time()
print('training model')
sentences = word2vec.LineSentence('wiki.txt')
id_w2v = word2vec.Word2Vec(sentences, vector_size=200, workers=multiprocessing.cpu_count()-1)
id_w2v.save('wiki_w2v.model')
finish_time = time.time()
print('Finish dalam waktu : {}'.format(timedelta(seconds=finish_time-start_time)))