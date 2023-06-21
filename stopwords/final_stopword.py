import json
import nltk
from an_lang import an_lang_stopword
from singkatan import abbrevation_stopword
from separator import separator_stopword
from slang_word import slang_stopword

list_stopword = []
list_stopword.extend(abbrevation_stopword)
list_stopword.extend(an_lang_stopword)
list_stopword.extend(separator_stopword)
list_stopword.extend(slang_stopword)
flatten = nltk.flatten(list_stopword)
final_stopword = flatten
# print(final_stopword)
