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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.80 Safari/537.36 '}

    def download_page(self):
        html = requests.get(self.target_url).content
        return html

    def parse_html(self, html):
        soup = BeautifulSoup(html)
        #  查找页面中所有remark的内容
        comments_soup = soup.find('div', attrs={'id': 'comments'})
        remark_list_soup = comments_soup.find_all('div', attrs={'class': 'comment-item'})
        remark_data = []
        for remark_soup in remark_list_soup:
            if remark_soup:
                comment_soup = remark_soup.find('span', attrs={'class': 'comment-vote'})
                vote = comment_soup.span.text
                comment_info_soup = remark_soup.find('span', attrs={'class': 'comment-info'})
                avatar = comment_info_soup.a.text
                comment_info = comment_info_soup.find_all('span')
                have_see = comment_info[0].text
                star = comment_info[1].get('class')[0]
                star = star[7]
                date = comment_info[2].get('title')[:9]
                text = remark_soup.p.text
                remark = [avatar, have_see, star, date, vote, text]
                remark_data.append(remark)
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
