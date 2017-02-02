### 使用Beautiful Soup抓取结构化数据
> 简书 http://www.jianshu.com/p/74c1acd7ca8b

写了Scrapy XPath抓取结构化数据的方法和技巧：
* [《再谈Scrapy抓取结构化数据》](http://www.jianshu.com/p/3d52e6046782)
* [《[小技巧]Chrome中拷贝XPath的方法》](http://www.jianshu.com/p/7408d3d3dcac)

再来一篇如何使用Beautiful Soup抓取结构化数据。把一些不同的写法汇总、对比列出来。
Beautiful Soup 官方文档较详细，每个方法下也有示例，[**Beautiful Soup**4.2.0 文档 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)
但没有抓取结构化数据的例子。

![结构化数据](http://upload-images.jianshu.io/upload_images/938707-86ea88593eb762b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


Beautiful Soup提供的方法都是按标签查找（select方法可以按标签逐层查找，相当于路径），对比一下XPath是按路径查找。着重讲BS的三个方法。

###1. find_all()
> find_all( name , attrs , recursive , text , **kwargs )

find_all() 方法搜索当前tag的所有子节点，并判断是否符合过滤器的条件。

```
soup.find_all("a")  ##查找文档中所有的<a>标签

```

```
soup.find_all('tr',  "item")  ##查找tr标签，class="item"

soup.find_all('tr', class_='item') 

soup.find_all('tr', attrs={"class": "item"}) # attrs 参数定义一个字典参数来搜索包含特殊属性的tag
```

带属性的标签，推荐用上面的第2种或第3种写法。


###2. find()
>find( name , attrs , recursive , text , **kwargs )

find_all()方法返回的是文档中符合条件的所有tag，是一个集合(class 'bs4.element.ResultSet')，find()方法返回的一个Tag(class 'bs4.element.Tag')


###3. select()
select可以筛选元素，按标签逐层查找。

```
soup.select("html head title")  ##标签层级查找

soup.select('td  div  a')  ## 标签路径 td --> div --> a

soup.select('td > div > a') 

```

注意，以上按路径 标签之间的空格 `td  div  a`，可以用`>`，但也要注意`>`与标签之间都有空格。

注意：select()方法指定标签属性可以这样用：
```
uls = soup.select('a.nbg')   # <a class="nbg">
```

###举栗子来说明
还是以 `https://book.douban.com/top250`为例，抓取图书名，出版社、价格，评分，评价推荐语。

1） 选择数据块（结构化数据）的循环点

在这里：
![](http://upload-images.jianshu.io/upload_images/938707-7f2f4cd6d1dc86b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


一个图书所有信息包含在表格的一行中`tr`

```
for link in soup.find_all('tr', class_='item'):
    ## 循环取出单个图书的信息
```

2）在循环中取每条数据
完整代码：

```
#-*-coding:utf8-*-
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

url = 'https://book.douban.com/top250'

def get_info2(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    for link in soup.find_all('tr', attrs={"class": "item"}):

        name = link.find("a")
        print name['href']
        info = link.find('p')
        print info.text

        title = link.find('div')
        print (str(title.a.text)).strip()

        quote = link.find('span',class_="inq")

        if quote:
            print quote.text
```


更多的代码，不同的写法放在Github：https://github.com/ppy2790/BeautifulSoup


**使用Beautiful Soup最大不方便的地方，在于需要定位标签时，它没有属性，或者属性不足于支持筛选出要所要的数据**。这时就结合select选取路径，或者使用`find_next_siblings() `等其他方法。如碰到取不到数据或取出来的是空的时候，调试的办法就是往上一级标签找数据。

其他内容可以多看看文档。
