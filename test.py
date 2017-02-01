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

def get_info(url):
    wb_data = requests.get(url, headers=headers).content
    soup = BeautifulSoup(wb_data, 'lxml')
    uls = soup.select('a.nbg')  # <a class="nbg">

    for a in uls:
        print a['href']



def get_info3(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    #for link in soup.find_all('tr', attrs={"class": "item"}):
    #for link in soup.find_all('tr',  "item"):
    for link in soup.find_all('tr', class_='item'):

        name = link.find("a")
        print name['href']
        info = link.find('p')
        print info.text

        title = link.find('div')
        print (str(title.a.text)).strip()

        quote = link.find('span',class_="inq")

        if quote:
            print quote.text



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



        titles2 = link.select('td > div > a')
        #titles2 = link.select('td  div  a')

        print titles2[0].text



get_info2(url)



