from bs4 import BeautifulSoup
import requests
import os
import time
from datetime import datetime

requests.adapters.DEFAULT_RETRIES = 5

categories = {
    '龙王传说': {
        'url': '/5/5782/',
        'tags': '[Duke, Hannb]'
    },
    '大主宰': {
        'url': '/0/330/',
        'tags': '[Duke, Hannb]'
    },
    '雪鹰领主': {
        'url': '/4/4364/',
        'tags': '[Duke, Hannb]'
    },
    '通天仙路': {
        'url': '/6/6434/',
        'tags': '[Duke, Hannb]'
    },
    '一念永恒': {
        'url': '/6/6145/',
        'tags': '[Duke, Hannb]'
    },
    '儒道至圣': {
        'url': '/3/3292/',
        'tags': '[Duke]'
    },
    '放开那个女巫': {
        'url': '/6/6319/',
        'tags': '[Duke]'
    },
    '修真聊天群': {
        'url': '/6/6424/',
        'tags': '[Duke]'
    },
    '我真是大明星': {
        'url': '/3/3826/',
        'tags': '[Duke]'
    },
    '天道图书馆': {
        'url': '/6/6435/',
        'tags': '[Duke]'
    },
    '全职法师': {
        'url': '/4/4438/',
        'tags': '[Duke]'
    },
    '剑王朝': {
        'url': '/3/3461/',
        'tags': '[Hannb]'
    },
    '剑王朝': {
        'url': '/3/3461/',
        'tags': '[Hannb]'
    },
    '永恒国度': {
        'url': '/6/6377/',
        'tags': '[Hannb]'
    }
}

postsPath =r'.'+ os.sep+'source'+os.sep+'_posts'+os.sep

class Post:
    __slots__ = ('tags', 'book', 'title', 'content')
    def __init__(self, tags, book, title, content):
        self.tags = tags
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
                'categories: ' + self.book + '\n',
                'tags: ' + self.tags + '\n',
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
for book, item in categories.items():
    try:
        url = item['url']
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
        newPost = Post(item['tags'], book, title, content)
        newPost.WriteMDFile()
        flag = True
    except Exception as e:
        print(e)
        continue
if flag :
    PushGit()
