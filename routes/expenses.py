from flask import Blueprint, render_template, request, redirect
import sqlite3
from datetime import date
from calendar import monthrange


expenses_bp = Blueprint("expenses", __name__) 

#Conexão com o DB
def connect_db():
    return sqlite3.connect("database.db") 

#Rotas
@expenses_bp.route("/")
def index():
    conn = connect_db()
    cursor = conn.cursor()

    today = date.today()
    first_day = today.replace(day=1)

    lastday_num = monthrange(today.year, today.month)[1]
    last_day = today.replace(day=lastday_num)


    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not start_date or not end_date:
        start_date = first_day
        end_date = last_day
    
    query_filter = ""
    params = []

    if start_date and end_date:
        query_filter = "AND date BETWEEN ? AND ?"
        params = [start_date, end_date]

    #Transações
    cursor.execute(f"""
        SELECT * FROM expenses {'WHERE date BETWEEN ? AND ?' if start_date and end_date else ''} ORDER BY date DESC LIMIT 50
    """, params)
    expenses = cursor.fetchall()

    #Receitas
    cursor.execute(f"""
        SELECT SUM(value) FROM expenses WHERE type = 'income' {query_filter}
    """, params)
    income = cursor.fetchone()[0] or 0

    #Gastos
    cursor.execute(f"""
        SELECT SUM(value) FROM expenses WHERE type = 'expense' {query_filter}
    """, params)
    expenses_total = cursor.fetchone()[0] or 0

    #Gasto por Categoria
    cursor.execute(f"""
        SELECT category, SUM(value) FROM expenses WHERE type = 'expense' {query_filter} GROUP BY category
    """, params)
    categories = cursor.fetchall()

    #Saldo
    balance = income - expenses_total

    #Evolucão Mensal
    cursor.execute("""
        SELECT strftime('%Y-%m', date) as month,
                SUM(CASE WHEN type='income' THEN value ELSE 0 END),
                SUM(CASE WHEN type='expense' THEN value ELSE 0 END)
        FROM expenses
        GROUP BY month
        ORDER BY month
    """)
    monthly = cursor.fetchall()

    conn.close()
    return render_template(
        "index.html", 
        expenses=expenses,
        income=income,
        expenses_total=expenses_total,
        categories=categories,
        balance=balance,
        monthly = monthly,
        start_date = start_date,
        end_date = end_date
        )

@expenses_bp.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    value = request.form["value"]
    category = request.form["category"]
    type_of = request.form["type"]
    date = request.form["date"]

    if not name or not value:
        return "Dados inválidos", 400
    
    try:
        value = float(value)
    except:
        return "Valor Inválido", 400
    
    if value <= 0:
        return "Valor deve ser positivo", 400

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


