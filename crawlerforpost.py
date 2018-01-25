import requests
from bs4 import BeautifulSoup


class CrawlerForPosts():
    #  表示单个贴子爬虫的类
    def __init__(self, target_url):
        self.target_url = target_url
        self.img_url_list = []
        self.next_pag = target_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/47.0.2526.80 Safari/537.36 '}

    def download_page(self):
        #  html = requests.get(self.target_url, headers=self.headers).content
        html = requests.get(self.target_url).content
        return html

    def parse_html(self, html):
        soup = BeautifulSoup(html)
        #  查找页面中所有img的URL
        img_list_soup = soup.find_all('img', attrs={'class': 'BDE_Image'})
        for img_soup in img_list_soup:
            img_url = img_soup.get('src')
            self.img_url_list.append(img_url)
        #  查找下一页URL
        next_pag_soup = soup.find('a', text={'下一页'})
        if next_pag_soup:
            self.next_pag = 'https://tieba.baidu.com' + next_pag_soup.get('href')
        else:
            self.next_pag = ""

    def get_info(self):
        self.img_url_list = []
        if self.target_url:
            html = self.download_page()
            self.parse_html(html)
            self.target_url = self.next_pag
