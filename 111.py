from setting import CrawlerSettings
from crawlerfordoubanmovie import CrawlerForDouBanMovies
import requests
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/subject/6874741/comments?start=220&limit=20&sort=new_score&status=P&percent_type='


global_set = CrawlerSettings()
target_url = url

#  创建爬虫
crawler_douban = CrawlerForDouBanMovies(global_set, target_url)


cookies = crawler_douban.cookies
result = requests.get(target_url, cookies=cookies)
print(result)
