from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import pandas as pd

ft = open('comments_stopworded.json')
ft2 = json.load(ft)
df = pd.DataFrame(ft2)
# print(df)

# Wordcloud
text = df[0].values
text = ' '.join(text)
wcld = WordCloud().generate(text)

plt.imshow(wcld, interpolation='bilinear')
plt.axis('off')
plt.show()