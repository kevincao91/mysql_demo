from pyecharts import Bar
from setting import ShowSettings
import numpy as np
from pyecharts import Line


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
    bar = Bar(global_set.show_title, global_set.show_subtitle)
    bar.add("各星级评星人数", attr, v1, is_label_show=True)
    bar.add("有效加权平均值", attr, v2, is_label_show=True)
    bar.render('render_show_star_bar.html')


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
    line = Line(global_set.show_title)
    line.add("观看时间分布", attr, v1, mark_point=["max"], is_smooth=True, mark_line=["max", "average"])
    line.render('render_show_date_line.html')


def create_diagram(global_set):
    show_star(global_set)
    show_date(global_set)


def main():
    #  设置参数 ========================================================================================================
    print('Function Start.')
    global_set = ShowSettings()
    db = global_set.db
    cursor = global_set.cursor
    #  初始化数据表

    #  根据需要生成不同图表
    create_diagram(global_set)

    # 关闭数据库连接
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
