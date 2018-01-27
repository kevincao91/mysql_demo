import pymysql


class ShowSettings():
    # 配置程序所有的设置数据
    def __init__(self):
        #  初始化程序的设置

        self.show_title = '无问东西影评分析'
        self.show_subtitle = '评星分布情况'
        self.save_path = ''

        #  数据库设置
        #  打开数据库连接
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd="caoke1991928",
                                  db="mypythondatabase", charset="utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        #  缓存文件设置
        self.cache_filename = '影评.txt'
        self.root_dir_name = 'html_cache/'
        self.save_path = ''

        #
        self.star_num_list = []
        self.star_weight_list = []
        self.star_avg = 0


class CrawlerSettings():
    # 配置爬虫程序所有的设置数据
    def __init__(self):
        #  初始化程序的设置
        #  数据库设置
        #  打开数据库连接
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd="caoke1991928",
                                  db="mypythondatabase", charset="utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        #  缓存文件设置
        self.cache_filename = '影评.txt'
        self.root_dir_name = 'html_cache/'
        self.save_path = ''
        #  cookies文件设置
        self.cookies_filename = 'cookies.txt'
        #  状态信息设置
        self.start_url = 'https://movie.douban.com/subject/6874741/comments?status=P'  # 无问东西短评
        self.max_pag_number = 20
        self.now_pag_number = 0
        self.store_remark_number = 0
        self.total_remark_num = 0
        self.total_d_remark_num = 0

    def get_save_path(self):
        #  计算缓存文件绝对路径
        self.save_path = self.root_dir_name + str(self.now_pag_number) + '.html'

