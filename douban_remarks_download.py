import time
import os
from setting import CrawlerSettings
from crawlerfordoubanmovie import CrawlerForDouBanMovies
import crate_diagram as cd
from tkinter import *


def initial_table(db, cursor):
    #  使用execute方法执行SQL语句
    #  删除 表
    sql1 = """DROP TABLE IF EXISTS remarks;"""
    try:
        cursor.execute(sql1)
    except:
        print('数据表初始化失败!')
        db.rollback()
    #  创建 表
    sql = """CREATE TABLE remarks (
             ID  INT PRIMARY KEY AUTO_INCREMENT,
             NICK_NAME  CHAR(20),
             HAVE_SEE CHAR(10),
             STAR CHAR(10),
             DATE_OF_VIEW CHAR(20),
             VOTE CHAR(10),
             REMARK CHAR(225))"""
    try:
        cursor.execute(sql)
    except:
        print('表已存在!')
        db.rollback()


def write_database(db, cursor, data):
    #  data = [avatar, have_see, star, date, vote, text]
    success_flag = False
    sql = "INSERT INTO `remarks` (`NICK_NAME`, `HAVE_SEE`, `STAR`, `DATE_OF_VIEW`, `VOTE`, `REMARK`) " \
          "VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4], data[5]))
        # 提交
        db.commit()
        success_flag = True
    except Exception:
        # 错误回滚
        print('插入失败!')
        db.rollback()
    return success_flag


def write_html(global_set, html):
    with open(global_set.save_path, 'wb') as file_object:
        try:
            file_object.write(html)
        except:
            print('html文件写入出错！')


def get_info_from_web_or_file(global_set, crawler_douban):
    remark_data = []
    #  判断缓存文件是否存在
    if os.path.exists(global_set.save_path):
        with open(global_set.save_path, 'rb') as file_object:
            try:
                html = file_object.read()
            except:
                print('html文件读取出错！')
            if html:
                #  抓取信息
                remark_data = crawler_douban.parse_html(html)
                crawler_douban.finish_time = time.time()
    else:
        #  抓取信息
        html, remark_data = crawler_douban.get_info()
        #  储存html信息
        write_html(global_set, html)
    return remark_data


def main(target_url):
    #  设置参数 ========================================================================================================
    print(target_url)
    print('Step 1: Scan Function Start.')
    global_set = CrawlerSettings()
    global_set.start_url = target_url
    db = global_set.db
    cursor = global_set.cursor
    #  初始化数据表
    initial_table(db, cursor)
    #  创建爬虫
    crawler_douban = CrawlerForDouBanMovies(global_set, target_url)
    start_time = time.time()
    #  获取标题
    global_set.movie_title = crawler_douban.get_movie_title()
    #  初始创建缓存文件夹
    global_set.get_root_path()
    if not os.path.exists(global_set.save_root_path):
        os.mkdir(global_set.save_root_path)
    global_set.get_dir_path()
    if not os.path.exists(global_set.save_dir_name):
        os.mkdir(global_set.save_dir_name)
    #  显示开始信息
    print('Movie: ' + global_set.movie_title + ' Remark Scan Start.')
    #  抓取页面Post链接 ================================================================================================
    while (crawler_douban.target_url != "") & (global_set.now_pag_number < global_set.max_pag_number):
        #  显示开始抓取信息
        global_set.now_pag_number += 1
        print('Douban Remark Page ' + str(global_set.now_pag_number))
        #  计算缓存文件绝对路径
        global_set.get_save_path()
        #  抓取信息
        remark_data = get_info_from_web_or_file(global_set, crawler_douban)
        #  显示抓取结果
        print(str(len(remark_data)) + ' Remarks Has Been Find.')
        #  储存remark信息 ==============================================================================================
        index_remark = 0
        d_index_remark = 0
        for remark in remark_data:
            index_remark += 1
            print('>>> Remark ' + str(index_remark), end="")
            success_flag = write_database(global_set.db, global_set.cursor, remark)
            if success_flag:
                d_index_remark += 1
                print(' Save Done!')
        #  统计总评论数 总储存评论数
        global_set.total_remark_num += index_remark
        global_set.total_d_remark_num += d_index_remark
        #  计算下一页URL
        crawler_douban.target_url = crawler_douban.next_pag
        #  显示跳出原因
        if global_set.now_pag_number >= global_set.max_pag_number:
            print('达到用户设置最大页数！')
        if not crawler_douban.target_url:
            print('没有下一页了！')
    #  显示结束信息  ===================================================================================================
    end_time = time.time()
    print('Step 1: Scan Function Finished! in ' + str(end_time - start_time) + 's')
    print(str(global_set.total_remark_num) + ' remarks has been find, and ', end="")
    print(str(global_set.total_d_remark_num) + ' remarks has been save.')
    #  显示结果
    sql = 'SELECT count(`ID`) AS `num_remark` FROM `remarks`'
    cursor.execute(sql)
    print(cursor.fetchone())
    # 关闭数据库连接
    cursor.close()
    db.close()
    # 画图
    cd.main(global_set.movie_title)


if __name__ == '__main__':
    main()
