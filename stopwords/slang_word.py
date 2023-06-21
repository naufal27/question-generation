import nltk
import pandas as pd

# slang = [
#     'mantap',
#     'owalah',
#     'lu',
#     'enggak',
#     'gak',
#     'ga',
#     'wow',
#     'banget',
#     'gini',
#     'amat',
#     'kok',
#     'makin',
#     'wkwk',
#     'kangen',
#     'dm',
#     'anjrit',
#     'eh',
#     'yaa',
#     'nih',
#     'tuh',
#     'deh',
#     'udah',
#     'gaada',
#     'wih',
#     'hihi',
#     'wihh',
#     'wihhhh',
#     'ajeh',
#     'gaskeun',
#     'gua',
#     'nyari',
#     'ngapain',
#     'pengen',
#     'dah',
#     'nyimaq',
#     'kek',
#     'bgt',
#     'yeay',
#     'mon',
#     'maap',
#     'anggurin',
#     'aduhh',
#     'nich',
#     'bagiin',
#     'bg',
#     'kate',
#     'yee',
#     'tipsen',
#     'huhuhu',
#     'nunggu',
#     'ahh',
#     'loh',
#     'titip',
#     'netijen',
#     'klo',
#     'waahhh',
#     'kerennn',
#     'lohh',
#     'ngajuin',
#     'wuuuu',
#     'emg',


#     'almet',
#     'katnya',
#     'kumpulin',
#     'dikumpulin',
#     'bagiaan',
#     'fto',
#     'dftr',
#     'gmna',
#     'yng',
#     'karfu',
#     'brlaku',
#     'dapetin',
#     'dmn',
#     'gmn',
#     'pakultas',
#     'gimna',
#     'semangaat',
#     'manaa',
#     'kno',
#     'masi',
#     'msh',
#     'matkul',
#     'nerima',
#     'knapa',
#     'apaa',


# ]


def tokenize(text):
    # tokenized = text.split()
    tokenized = nltk.tokenize.word_tokenize(text)
    return tokenized


df = pd.read_csv('unformal word - gaul.csv', names=['slang'])
list = df.values.tolist()
flatten = nltk.flatten(list)
slang_stopword = flatten
# print(slang_stopword)
