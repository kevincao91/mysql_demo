import pymysql


class ShowSettings():
    # 配置程序所有的设置数据
    def __init__(self, movie_title):
        #  初始化程序的设置
        self.movie_title = movie_title
        self.show_title = self.movie_title + ' 影评分析'
        self.show_subtitle_1 = '评星人数分布情况'
        self.show_subtitle_2 = '观影日期分布情况'
        self.show_subtitle_3 = '影评词频分布情况'

        #  数据库设置
        #  打开数据库连接
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd="caoke1991928",
                                  db="mypythondatabase", charset="utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        #  缓存文件设置
        self.save_dir_name = movie_title + '/output_file/'
        self.save_path_1 = self.save_dir_name + 'render_show_star_bar.html'
        self.save_path_2 = self.save_dir_name + 'render_show_date_line.html'
        self.save_path_3 = self.save_dir_name + 'render_show_word_cloud.html'
        self.remark_filename = '影评缓存.txt'
        #  评星计算参数设置
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
        self.save_root_path = ''
        self.save_dir_name = ''
        self.save_path = ''
        #  cookies文件设置
        self.cookies_filename = 'cookies.txt'
        #  状态信息设置
        self.start_url = 'https://movie.douban.com/subject/26004132/comments?status=P'  # 移动迷宫短评  热门
        self.max_pag_number = 30
        self.now_pag_number = 0
        self.store_remark_number = 0
        self.total_remark_num = 0
        self.total_d_remark_num = 0
        self.movie_title = ''

    def get_root_path(self):
        #  计算缓存文件夹绝对路径
        self.save_root_path = self.movie_title + '/'

    def get_dir_path(self):
        #  计算缓存文件夹绝对路径
        self.save_dir_name = self.save_root_path + 'html_cache/'

    def get_save_path(self):
        #  计算缓存文件绝对路径
        self.save_path = self.save_dir_name + str(self.now_pag_number) + '.html'
