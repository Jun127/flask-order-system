import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 建立商品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    # 建立訂單表（含訂購人資訊）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            notes TEXT,
            delivery_date TEXT NOT NULL,
            order_details TEXT NOT NULL,
            total_price INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 初始化菜單
    cursor.execute("DELETE FROM products")  # 清除舊菜單，防止重複新增
    menu_items = [
        ("健康餐", "鮮蝦", 100), ("健康餐", "打拋豬", 100), ("健康餐", "雞胸肉", 100),
        ("活力餐", "瓜仔肉", 100), ("活力餐", "日式咖哩", 100), ("活力餐", "蔬食", 100),
        ("活力餐", "氣炸雞塊", 100), ("活力餐", "三杯雞", 100),
        ("沙拉", "鮮蝦", 100), ("沙拉", "蔬果", 100), ("沙拉", "雞胸肉", 100)
    ]
    cursor.executemany("INSERT INTO products (category, name, price) VALUES (?, ?, ?)", menu_items)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("資料庫初始化完成！")
