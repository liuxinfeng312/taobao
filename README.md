```
step1:查看数据结构，对数据进行清洗、去除空值异常值，通过DateFrame 列名 切割数据。step2：通过matplotlib 根据商品类名，统计类名下的数量 ，画饼图。
step3:通过DateFrame根据类名找到 类名下的商品名，再根据商品名找到对应商品名下的评论，根据类名下的商品名的评论画柱状图，并显示差评最多的商品名。
step4:调用第三方库wordcloud 绘制词云，将每个类名下的评论搜集起来后，按照中文符号等进行切割，再将清洗过的数据放到自定义好的函数(cloud_word.py)中进行绘制。
```

