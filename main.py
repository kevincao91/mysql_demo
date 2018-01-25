import pymysql
from setting import Settings


def initial_table(db, cursor):
    # 使用execute方法执行SQL语句
    sql = """CREATE TABLE remarks (
             ID  INT PRIMARY KEY AUTO_INCREMENT,
             NICK_NAME  CHAR(20),
             HAVE_SEE CHAR(10),  
             DATE_OF_VIEW CHAR(20),
             VOTE CHAR(10),
             REMARK CHAR(225))"""
    try:
        cursor.execute(sql)
    except :
        print('表已存在!')
        db.rollback()


def get_info(global_set):
    db = global_set.db
    cursor = global_set.cursor
    with open(global_set.cache_filename, 'r') as file_object:
        liens = file_object.readlines()
        count = 0
        for line in liens:
            count += 1
            print(count)
            data = []
            data = line.strip().split('^')
            #  写数据到数据库
            write_database(db, cursor, data)


def write_database(db, cursor, data):
    # sql = """INSERT INTO EMPLOYEE(FIRST_NAME,LAST_NAME, AGE, SEX, INCOME) VALUES ('Mac', 'Mohan', 20, 'M', 1800)"""
    sql = "INSERT INTO `remarks` (`NICK_NAME`, `HAVE_SEE`, `DATE_OF_VIEW`, `VOTE`, `REMARK`) " \
          "VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (data[1], data[2], data[3], data[0], data[4]))
        # 提交
        db.commit()
    except Exception:
        # 错误回滚
        print('插入失败!')
        db.rollback()


def main():
    #  初始化数据
    global_set = Settings()
    db = global_set.db
    cursor = global_set.cursor
    #  初始化数据表
    initial_table(db, cursor)
    #  抓取数据
    html, remark_data = get_info(global_set)
    #  显示结果
    sql = 'SELECT count(`ID`) AS `num_remark` FROM `remarks`'
    cursor.execute(sql)
    print(cursor.fetchone())
    # 关闭数据库连接
    global_set.cursor.close()
    global_set.db.close()


if __name__ == '__main__':
    main()

