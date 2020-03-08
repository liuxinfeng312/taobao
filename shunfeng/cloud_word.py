#encoding=utf-8
import numpy as py
import pandas as pd
import jieba
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
import wordcloud
from PIL import Image
import collections
import re


def wordCloud(txt,tit):
    pattern = re.compile(u'\t|\n|\.|\、|\；|\。|\：|\，|\（|\）|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
    string_data = re.sub(pattern, ' ', txt)
    string_data = string_data.split(' ')
    stop_word = []
    jieba_string = [x for x in string_data if x not in stop_word and len(x) > 1]
    word_counts=collections.Counter(jieba_string)
    word_counts.most_common(80)
    # scale=4，#这个数值越大，产生的图片分辨率越高，字迹越清晰
    wc = wordcloud.WordCloud(scale=4,
                             font_path=r'C:\Windows\Fonts\simhei.ttf',
                             background_color='white',
                             max_words=100,
                             max_font_size=50
                             )
    wc.generate_from_frequencies(word_counts)
    plt.figure(figsize=(30,20))
    plt.imshow(wc)
    plt.axis('off')
    plt.title(tit,fontsize=100,backgroundcolor='r')
    plt.show()

