import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    # 初始化商品
    cursor.execute("INSERT INTO products (name, stock) VALUES ('A', 10), ('B', 5)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("資料庫初始化完成！")
