import os
import json
import re
import string
import pandas as pd
import numpy as np

# Merge All Comments File
path_json = '../uinsgd.official_comments2/'
json_files = [comment_json for comment_json in os.listdir(
    path_json) if comment_json.endswith('.json')]
data = []
for json_file in json_files:
    with open(path_json + json_file) as file:
        jl = json.load(file)
        for d in jl:
            d['path'] = json_file
        data.extend(jl)

# Preprocessing Data


def emojify(text):  # remove emoji
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
                       #    u"\u2018"
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


def just_number(text):
    return re.sub(r"\b\d+\b", " ", text)  # remove just numbers


def punctuation(text):
    return text.translate(str.maketrans(
        "", "", string.punctuation))   # remove punctuation


def single_char(text):
    return re.sub(r"\b[a-zA-Z]\b", " ", text)  # remove single char


def remoji(text):
    return emojify(text)  # remove emoji


def space(text):
    processed = text.strip()   # remove whitespace start and end
    processed = " ".join(re.split("\s+", processed, flags=re.UNICODE))
    return processed


# Create Dataframe
for i, d in enumerate(data):
    if not d['answers']:
        data[i]['answers'] = [{'answers': [{}]}]

normalized_1 = pd.json_normalize(data)  # 2838
normalized_2 = pd.json_normalize(normalized_1.to_dict(  # 3437  #1239
    orient='records'), meta=['text', 'path'], record_path='answers', record_prefix='answer_')
text_drop = normalized_2['text'].drop_duplicates()
text_path = pd.DataFrame({'text': text_drop, 'path': normalized_2['path']})
atext_path = pd.DataFrame(
    {'text': normalized_2['answer_text'], 'path': normalized_2['path']})
df = pd.concat([text_path, atext_path], ignore_index=True)
df.dropna(inplace=True)

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
df['text'] = df['text'].apply(space)

df.replace('', np.nan, inplace=True)  # 418
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
y = df.to_json(r'cleansing.json', orient='records', indent=4)
print(df)
