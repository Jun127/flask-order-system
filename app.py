from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# 取得商品庫存
def get_stock():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "name": p[1], "stock": p[2]} for p in products]

# 首頁
@app.route("/")
def index():
    return render_template("index.html", products=get_stock())

# 點餐 API
@app.route("/order", methods=["POST"])
def order():
    data = request.json
    product_id = data["id"]

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 獲取當前庫存
    cursor.execute("SELECT name, stock FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product and product[1] > 0:
        new_stock = product[1] - 1
        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
        
        # **記錄訂單**
        cursor.execute("INSERT INTO orders (product_id, product_name) VALUES (?, ?)", (product_id, product[0]))

        conn.commit()
        conn.close()
        return jsonify({"success": True, "new_stock": new_stock})
    
    conn.close()
    return jsonify({"success": False, "message": "庫存不足"})

# **新增 API：查看所有訂單**
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY timestamp DESC")
    orders = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": o[0], "product_id": o[1], "product_name": o[2], "timestamp": o[3]} 
        for o in orders
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
