from flask import Flask, render_template, jsonify, request
import sqlite3

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
    product_id = request.json["id"]

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 獲取當前庫存
    cursor.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product and product[0] > 0:
        new_stock = product[0] - 1
        cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "new_stock": new_stock})
    
    conn.close()
    return jsonify({"success": False, "message": "庫存不足"})

if __name__ == "__main__":
    app.run(debug=True)
