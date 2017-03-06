import jieba
from wordcloud import WordCloud
import PIL
import matplotlib.pyplot as plt
import numpy as np

f = open('mimeng.txt', 'r', encoding='utf-8').read()
w = open('mimengcount.txt', 'w')
words = list(jieba.cut(f))
for word in words:
    if len(word) > 1:
        word = word + '\n'
        w.writelines(word)
w.close()


def wordcloudplot():
    text = open('mimengcount.txt').read()
    path = '/Library/Fonts/AppleGothic.ttf'
    alice_mask = np.array(PIL.Image.open('text.jpg'))
    wordcloud = WordCloud(font_path=path, background_color="white", margin=5, width=1800, height=800, mask=alice_mask, max_words=2000,
                          max_font_size=60, random_state=42)
    worcloud = wordcloud.generate(text)
    wordcloud.to_file('pic.jpg')
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

wordcloudplot()
