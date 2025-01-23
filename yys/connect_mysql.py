import pymysql

# 连接到 MySQL 数据库
connection = pymysql.connect(
    host='193.169.203.10',
    user='sylink',
    password='sylink',
    database='guava'
)

# 创建游标对象
cursor = connection.cursor()

# 执行查询
cursor.execute("select * from guava.recycle_code_history rch where code = 'BGCPCP00000071-0351/00002';", (20,))

# 获取查询结果
results = cursor.fetchall()
for row in results:
    print(row)

# 关闭连接
cursor.close()
connection.close()