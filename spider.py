from bs4 import BeautifulSoup
import requests
import os
import time
from datetime import datetime

requests.adapters.DEFAULT_RETRIES = 5

urls = {
    '龙王传说': '/5/5782/',
    '大主宰': '/0/330/',
    '永夜君王': '/2/2790/',
    '雪鹰领主': '/4/4364/',
    '儒道至圣': '/3/3292/',
    '放开那个女巫':'/6/6319/',
    '修真聊天群':'/6/6424/',
    '我真是大明星':'/3/3826/',
    '通天仙路': '/6/6434/',
    '一念永恒': '/6/6145/',
    '天道图书馆': '/6/6435/',
    '全职法师':'/4/4438/'
}

postsPath =r'.'+ os.sep+'source'+os.sep+'_posts'+os.sep

class Post:
    __slots__ = ('book', 'title', 'content')
    def __init__(self, book, title, content):
        self.book = book
        self.title = title
        self.content = content

    def WriteMDFile(self):
        fileName = r'%s%s.md'%(postsPath,self.title)
        with open(fileName, 'a+', encoding='utf-8') as f:
            f.writelines([
                '---\n',
                'title: ' + self.title + '\n',
                'date: ' + time.strftime('%F %T') + '\n',
                'tag: ' + self.book + '\n',
                '---\n',
                self.content
            ])

#解析HTML文件
def GetHTML(url):
    html = requests.get('http://m.37zw.com'+url,timeout=10)
    return html.content

#从小说首页HTML文件中解析出a标签，并返回最新章节地址
def ParseA(html,url):
    soup = BeautifulSoup(html, 'lxml')
    a = soup.select_one('a[href$=.html]')
    title = a.get_text()
    href = a.get('href')
    return title, href

#解析最新章节HTML文件，返回内容
def ParsePostHtml(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select_one('#nr1').get_text()
    return content

def PushGit():
    os.system('git add %s*'%(postsPath))
    os.system('git commit -m "%s"'%('更新小说内容'))
    os.system('git push')
    print('推送完毕')


flag = False
for book, url in urls.items():
    try:
        html = GetHTML(url)
        title, href = ParseA(html,url)
        postHtml = GetHTML(url + href)
        content = ParsePostHtml(postHtml)
        content = content.strip('shipei_x()').replace('\xa0\xa0\xa0\xa0', '\n')
        if len(content)<200:
            continue
        title = book+' '+title
        if title+'.md' in os.listdir(postsPath):
            print(title+' 未更新 '+time.strftime('%F %T'))
            continue
        else:
            print(title+' 更新 '+time.strftime('%F %T'))
        newPost = Post(book, title, content)
        newPost.WriteMDFile()
        flag = True
    except Exception as e:
        print(e)
        continue

if flag :
    PushGit()
