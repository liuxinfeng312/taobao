#encoding=utf-8
import numpy as np
import pandas as pd
from  pandas import DataFrame,Series
import matplotlib.pyplot as plt
import jieba
from shunfeng.cloud_word import wordCloud
plt.rcParams['font.sans-serif'] = 'SimHei'  ##设置字体为SimHei显示中文
plt.rcParams['axes.unicode_minus'] = False  ##设置正常显示符号

def lei_pie():
    df = pd.read_excel('顺丰优选差评数据.xlsx')
    kind = df['商品类名']
    good_name = df['商品名']
    fail_num = 0
    kind_label = []
    kind_num = []
    for it in list(kind.unique()):
        kind_label.append(it)
        try:
            lei_good = set(good_name[df['商品类名'] == it])
            kind_num.append(int(len(lei_good)))
        except:
            fail_num += 1

    explode = (0, 0, 0, 0.1)
    plt.pie(kind_num, explode=explode, labels=kind_label, autopct='%1.1f%%', shadow=True, startangle=1500)
    plt.title("电商评论优选差评-种类")
    plt.show()

def goods_chaping():
    df = pd.read_excel('顺丰优选差评数据.xlsx')
    kind = df['商品类名']
    good_name = df['商品名']
    pinglun = df['评论']
    fail_num = 0
    fig = plt.figure(figsize=(8, 6))
    index = 0
    for it in list(kind.unique()):
        index += 1
        goods = []
        goods_num = []

        try:
            lei_good = set(good_name[df['商品类名'] == it])
            for jt in lei_good:
                good_pinglun = set(pinglun[df['商品名'] == jt])
                goods.append(jt)
                goods_num.append(int(len(good_pinglun)))

        except:
            fail_num += 1
            # print('\n')
            # print(it+jt+'\t'+pinglun[df['商品名']==jt])
            # exit()
        ax = fig.add_subplot(1, 4, index)
        ax.bar(range(len(goods_num)), goods_num)
        ax.set_xlabel('商品名')
        ax.set_ylabel('差评数量\n差评最多的商品（{}）'.format(goods[goods_num.index(max(goods_num))]), c='r')
        ax.set_title(it)
    fig.show()


def pinglun_word():
    df = pd.read_excel('顺丰优选差评数据.xlsx')

    kind = df['商品类名']
    good_name = df['商品名']
    pinglun = df['评论']
    fail_num = 0
    index = 0
    for it in list(kind.unique()):
        index += 1
        lei_pinglun = set()
        try:
            lei_good = set(good_name[df['商品类名'] == it])
            for jt in lei_good:

                good_pinglun = set(pinglun[df['商品名'] == jt])
                print(good_pinglun)
                lei_pinglun.add(','.join(good_pinglun))

        except:
            fail_num += 1
        txt=','.join(lei_pinglun)
        wordCloud(txt,tit=it)

def clean_data():
    df=pd.read_excel('顺丰优选差评数据.xlsx')
    # print(df.info())
    kind=df['商品类名']
    good_name=df['商品名']
    pinglun=df['评论']
    # print(kind.unique())
    # print(len(list(good_name.unique())))
    fail_num=0
    kind_label=[]
    kind_num=[]

    fig=plt.figure(figsize=(8,6))
    index=0
    for it in list(kind.unique()):
        index+=1
        print('\n')
        print(it)
        kind_label.append(it)
        goods = []
        goods_num = []
        lei_pinglun=set()
        try:
            lei_good=set(good_name[df['商品类名']==it])
            print(len(lei_good),lei_good)
            kind_num.append(int(len(lei_good)))
            for jt in lei_good:
                good_pinglun=set(pinglun[df['商品名']==jt])
                lei_pinglun.add(','.join(good_pinglun))
                # wordCloud(','.join(good_pinglun))
                # print(it,repr(jt),len(good_pinglun),repr(good_pinglun))

                goods.append(jt)
                goods_num.append(int(len(good_pinglun)))
            print('*'*100)
            print(goods_num)
        except:
            fail_num+=1
            # print('\n')
            # print(it+jt+'\t'+pinglun[df['商品名']==jt])
            # exit()
        wordCloud(','.join(lei_pinglun))

        ax = fig.add_subplot(2, 4, index)
        ax.bar(range(len(goods_num)), goods_num)
        ax.set_xlabel('商品名')
        ax.set_ylabel('差评数量\n差评最多的商品（{}）'.format(goods[goods_num.index(max(goods_num))]),c='r')
        ax.set_title(it)
        print(goods[goods_num.index(max(goods_num))],'max')
    print(fail_num)
    # print(kind_label,kind_num)
    explode = (0,0,0,0.1)
    ax2 = fig.add_subplot(2, 4, 5)
    ax2.pie(kind_num, explode=explode, labels=kind_label, autopct='%1.1f%%', shadow=True, startangle=1500)
    ax2.set_title("顺丰优选差评-种类")

    fig.show()




if __name__ == '__main__':
    # clean_data()

    lei_pie()
    goods_chaping()
    pinglun_word()

