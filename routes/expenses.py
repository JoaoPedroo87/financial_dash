from flask import Blueprint, render_template, request, redirect
import sqlite3

expenses_bp = Blueprint("expenses", __name__) 

#Conexão com o DB
def connect_db():
    return sqlite3.connect("database.db") 

#Rotas
@expenses_bp.route("/")
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
        )
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(value) FROM expenses")
    total = cursor.fetchone()[0]
    total = total if total else 0

    cursor.execute("SELECT category, SUM(value) FROM expenses GROUP BY category")

    categories = cursor.fetchall()

    conn.close()
    return render_template(
        "index.html", 
        expenses=expenses,
        total=total,
        categories=categories
        )

@expenses_bp.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    value = request.form["value"]
    category = request.form["category"]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (name, value, category) VALUES (?, ?, ?)",
        (name, value, category)
        )
    conn.commit()
    conn.close

    return redirect("/")

@expenses_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


