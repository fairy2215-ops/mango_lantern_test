import pymysql
import sqlparse
from config.config import *


def get_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8",
        autocommit=True
    )
    return connection


def execute_sql_file(filepath, procedure_name):
    connection = get_connection()
    # 读取 SQL 文件
    # with后表达式的值给到as后的变量
    # with上下文管理器，退出缩进代码块时自动释放文件，自动关闭数据库、浏览器等资源，异常也会自动关闭
    with open(filepath, 'r', encoding='utf-8') as f:
        # 使用 sqlparse 拆分 SQL 语句 (智能识别 BEGIN...END)
        statements = sqlparse.split(f.read())
        # 打印调试解析后的SQL语句
        # print(statements)

    with connection.cursor() as cursor:
        # 遍历所有语句
        for statement in statements:
            # 执行语句会报错，存储过程重复创建 'PROCEDURE TEST already exists'
            # 解决方法: 优化sql文件中的存储过程创建
            cursor.execute(statement)
        # 调用存储过程
        cursor.callproc(procedure_name)
        # # 打印调试结果
        # result = cursor.fetchall()
        # for row in result:
        #     print(row)
    # 关闭连接
    connection.close()


# 直接运行这个文件时，先清理测试数据，再初始化数据，方便调试测试用例的执行
# ✅ 直接运行这个文件 → 执行下面的代码（测试用）
# ❌ 被其他文件导入 → 不执行下面的代码（正常使用）
if __name__ == '__main__':
    execute_sql_file("../mysql_data_init/destroy.sql", "DESTROY")
    execute_sql_file('../mysql_data_init/fuction.sql', 'INIT_WAREHOUSE_AREA')

