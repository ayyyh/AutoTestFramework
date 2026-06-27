import sqlite3

# 1. 连接（如果不存在会自动创建）本地数据库文件 test_db.db
conn = sqlite3.connect("test_db.db")
cursor = conn.cursor()

# 2. 创建 users 表（模拟你公司数据库里的用户表）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        first_name TEXT,
        last_name TEXT
    )
''')

# 3. 插入一条测试数据（模拟数据库里已经存在的合法用户）
# 注意：必须和 dummyjson.com 里 emilys 的信息完全一致！
cursor.execute('''
    INSERT OR REPLACE INTO users (id, username, email, first_name, last_name)
    VALUES (1, 'emilys', 'emily.johnson@x.dummyjson.com', 'Emily', 'Johnson')
''')

conn.commit()
conn.close()
print("✅ 本地测试数据库 test_db.db 创建成功，并插入了 emilys 的用户数据！")