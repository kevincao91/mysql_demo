import requests
from bs4 import BeautifulSoup
import time


class CrawlerForDouBanMovies():
    #  表示单个贴吧爬虫的类
    def __init__(self, global_set, target_url):
        self.global_set = global_set
        self.target_url = target_url
        self.post_url_list = []
        self.next_pag = target_url
        self.start_time = time.time()
        self.finish_time = time.time()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'}
        #  cookies文件设置
        self.cookies = {}
        self.get_cookies()

    def get_cookies(self):
        cookies_filename = self.global_set.cookies_filename
        #  获得cookies文件内容
        with open(cookies_filename, 'r') as file_object:
            try:
                raw_cookies = file_object.read()
            except:
                print('cookies文件读取出错！')
        for line in raw_cookies.split(';'):
            line = line.strip()
            key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
            self.cookies[key] = value

    def download_page(self):
        cookies = self.cookies
        html = requests.get(self.target_url, cookies=cookies).content
        return html

    def parse_html(self, html):
        soup = BeautifulSoup(html)
        #  查找页面中所有remark的内容
        comments_soup = soup.find('div', attrs={'id': 'comments'})
        remark_list_soup = comments_soup.find_all('div', attrs={'class': 'comment-item'})
        remark_data = []
        # index = 0
        for remark_soup in remark_list_soup:
            # index += 1
            # print(index)
            if remark_soup:
                comment_soup = remark_soup.find('span', attrs={'class': 'comment-vote'})
                vote = comment_soup.span.text
                comment_info_soup = remark_soup.find('span', attrs={'class': 'comment-info'})
                avatar = comment_info_soup.a.text
                comment_info = comment_info_soup.find_all('span')
                have_see = comment_info[0].text
                if len(comment_info) == 3:
                    star = comment_info[1].get('class')[0]
                    star = star[7]
                    date = comment_info[2].get('title')
                    date = date.split(' ')[0]
                else:
                    star = '0'
                    date = comment_info[1].get('title')
                    date = date.split(' ')[0]
                text = remark_soup.p.text.strip()
                remark = [avatar, have_see, star, date, vote, text]
                remark_data.append(remark)
                # print('Done!')
        #  查找下一页URL
        next_pag_soup = soup.find('a', attrs={'class': 'next'})
        if next_pag_soup:
            self.next_pag = self.global_set.start_url[:-9] + next_pag_soup.get('href')
        else:
            self.next_pag = ""
        return remark_data

    def get_info(self):
        if self.target_url:
            html = self.download_page()
            remark_data = self.parse_html(html)
            self.finish_time = time.time()
            return html, remark_data
        else:
            return None

    def get_movie_title(self):
        if self.target_url:
            html = self.download_page()
            soup = BeautifulSoup(html)
            #  查找页面中所有h1的内容
            comments_soup = soup.find('h1')
            title = comments_soup.text[:-3]
            return title
        else:
            return None
