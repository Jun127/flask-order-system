from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# 取得菜單
def get_menu():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "category": p[1], "name": p[2], "price": p[3]} for p in products]

# 首頁（顯示菜單）
@app.route("/")
def index():
    return render_template("index.html", products=get_menu())

# 提交訂單
@app.route("/submit_order", methods=["POST"])
def submit_order():
    data = request.json
    customer_name = data["customer_name"]
    notes = data["notes"]
    delivery_date = data["delivery_date"]
    order_details = data["order_details"]
    total_price = data["total_price"]

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_name, notes, delivery_date, order_details, total_price) VALUES (?, ?, ?, ?, ?)",
                   (customer_name, notes, delivery_date, order_details, total_price))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

# 查看所有訂單
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY timestamp DESC")
    orders = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": o[0], "customer_name": o[1], "notes": o[2], "delivery_date": o[3], "order_details": o[4], "total_price": o[5], "timestamp": o[6]}
        for o in orders
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
