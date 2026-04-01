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
    #Lista de gastos
    cursor.execute("""
        SELECT * FROM expenses ORDER BY id DESC
    """)
    expenses = cursor.fetchall()

    #Receitas
    cursor.execute("""
        SELECT SUM(value) FROM expenses WHERE type = 'income'
    """)
    income = cursor.fetchone()[0] or 0

    #Gastos
    cursor.execute("""
        SELECT SUM(value) FROM expenses WHERE type = 'expense'
    """)
    expenses_total = cursor.fetchone()[0] or 0

    #Gasto por Categoria
    cursor.execute("""
        SELECT category, SUM(value) FROM expenses WHERE type = 'expense' GROUP BY category
    """)
    categories = cursor.fetchall()

    conn.close()
    return render_template(
        "index.html", 
        expenses=expenses,
        income=income,
        expenses_total=expenses_total,
        categories=categories
        )

@expenses_bp.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    value = request.form["value"]
    category = request.form["category"]
    type_of = request.form["type"]
    date = request.form["date"]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (name, value, category, type, date) VALUES (?, ?, ?, ?, ?)",
        (name, value, category, type_of, date)
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


