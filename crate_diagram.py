from pyecharts import Bar
from setting import ShowSettings
import numpy as np
from pyecharts import Line
from pyecharts import WordCloud
import jieba.analyse
import time
import os


def show_star(global_set):
    db = global_set.db
    cursor = global_set.cursor
    # 使用execute方法执行SQL语句
    sql = """SELECT star, COUNT(ID) FROM remarks GROUP BY star DESC;"""
    try:
        cursor.execute(sql)
    except:
        print('数据读取失败!')
        db.rollback()
    stars_data = cursor.fetchall()
    #  获取各星级评价人数
    star_num_list = []
    for key_name, key_value in stars_data:
        star_num_list.append(key_value)
    print(star_num_list)
    global_set.star_num_list = star_num_list
    #  计算评星有效加权平均值
    star_num = global_set.star_num_list[:-1]
    star_avg = np.average([5, 4, 3, 2, 1], weights=star_num)
    star_avg = round(star_avg, 2)
    global_set.star_avg = star_avg
    #  配置柱状图参数
    attr = ["5星", "4星", "3星", "2星", "1星", "未评级", "平均星级"]
    v1 = star_num_list + [0]
    v2 = [0, 0, 0, 0, 0, 0, star_avg]
    bar = Bar(global_set.show_title, global_set.show_subtitle_1)
    bar.add("各星级评星人数", attr, v1, is_label_show=True)
    bar.add("有效加权平均值", attr, v2, is_label_show=True)
    bar.render(global_set.save_path_1)


def show_date(global_set):
    db = global_set.db
    cursor = global_set.cursor
    # 使用execute方法执行SQL语句
    sql = """SELECT date_of_view, COUNT(ID) FROM remarks GROUP BY date_of_view ASC;"""
    try:
        cursor.execute(sql)
    except:
        print('数据读取失败!')
        db.rollback()
    dates_data = cursor.fetchall()
    #  获取各星级评价人数
    date_list = []
    date_num_list = []
    for key_name, key_value in dates_data:
        date_list.append(key_name)
        date_num_list.append(key_value)
    print(date_list)
    print(date_num_list)
    #  配置折线图参数
    attr = date_list
    v1 = date_num_list
    line = Line(global_set.show_title, global_set.show_subtitle_2)
    line.add("观看时间分布", attr, v1, is_fill=True, area_color='#000', area_opacity=0.3, mark_point=["max"],
             is_smooth=True, mark_line=["max", "average"])
    line.render(global_set.save_path_2)


def show_word(global_set):
    db = global_set.db
    cursor = global_set.cursor
    # 使用execute方法执行SQL语句
    sql = """SELECT ID, remark FROM remarks"""
    try:
        cursor.execute(sql)
    except:
        print('数据读取失败!')
        db.rollback()
    remarks_data = cursor.fetchall()
    #  写各评价内容
    with open(global_set.remark_filename, 'w') as file_object:
        for key_name, key_value in remarks_data:
            try:
                file_object.writelines(key_value)
            except:
                print('影评缓存文件写入出错！')
        print('影评缓存文件写入完毕！')
    #  提取影评
    with open(global_set.remark_filename, 'r') as file_object:
        content = file_object.read()
    #  提取词频
    jieba.suggest_freq(global_set.movie_title, True)   # 标题添加到字典
    jieba.del_word('电影')  # 电影不可见
    tags = jieba.analyse.extract_tags(content, withWeight=True, topK=30)
    word_list = []
    weight_list = []
    #  生成词频数据
    for tag in tags:
        word_list.append(tag[0])
        weight_list.append(tag[1])
    print(word_list)
    print(weight_list)
    #  配置词云图参数
    attr = word_list
    v1 = weight_list
    wordcloud = WordCloud(global_set.show_title, global_set.show_subtitle_3, width=800, height=600)
    wordcloud.add("", attr, v1, word_size_range=[20, 100])
    wordcloud.render(global_set.save_path_3)


def create_diagram(global_set):
    show_star(global_set)
    show_date(global_set)
    show_word(global_set)


def main(movie_title):
    #  设置参数 ========================================================================================================
    print('Step 2: Show Result Function Start.')
    start_time = time.time()
    global_set = ShowSettings(movie_title)
    #  初始创建缓存文件夹
    if not os.path.exists(global_set.save_dir_name):
        os.mkdir(global_set.save_dir_name)
    db = global_set.db
    cursor = global_set.cursor
    #  初始化数据表
    #  根据需要生成不同图表
    create_diagram(global_set)
    # 关闭数据库连接
    cursor.close()
    db.close()
    end_time = time.time()
    print('Step 2: Show Result Function Finished! in ' + str(end_time - start_time) + 's')


if __name__ == '__main__':
    main()
