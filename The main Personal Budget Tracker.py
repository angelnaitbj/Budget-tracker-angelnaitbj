# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 21:56:09 2025

@author: ANGEL NAITBJ
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 21:56:09 2025
@author: ANGEL NAITBJ
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv

# ---------- Helper Function for Placeholder ----------
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------- Database Setup ----------
conn = sqlite3.connect("budget.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
''')
conn.commit()

# ---------- Functions ----------
def add_transaction():
    global selected_transaction_id
    type_ = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()

    try:
        amount = float(amount)
        if not category or category in ["Category"]:
            raise ValueError("Category cannot be empty")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if selected_transaction_id is not None:
            cursor.execute(
                "UPDATE transactions SET type=?, category=?, amount=?, date=? WHERE id=?",
                (type_, category, amount, date, selected_transaction_id)
            )
            selected_transaction_id = None
            add_button.config(text="Add")
        else:
            cursor.execute(
                "INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
                (type_, category, amount, date)
            )

        conn.commit()
        update_transaction_list()
        update_summary()
        clear_inputs()
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def update_transaction_list(filter_category=None, filter_date=None):
    for row in transaction_list.get_children():
        transaction_list.delete(row)

    query = "SELECT * FROM transactions"
    params = []
    if filter_category or filter_date:
        query += " WHERE"
        conditions = []
        if filter_category and filter_category != "Filter by Category":
            conditions.append(" category LIKE ?")
            params.append(f"%{filter_category}%")
        if filter_date and filter_date != "Filter by Date (YYYY-MM-DD)":
            conditions.append(" date LIKE ?")
            params.append(f"%{filter_date}%")
        query += " AND".join(conditions)
    query += " ORDER BY date DESC"

    cursor.execute(query, params)
    for row in cursor.fetchall():
        transaction_list.insert("", "end", values=row)

def update_summary():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expenses = cursor.fetchone()[0] or 0.0

    balance = income - expenses
    income_label.config(text=f"Income: #{income:.2f}")
    expense_label.config(text=f"Expenses: #{expenses:.2f}")
    balance_label.config(text=f"Balance: #{balance:.2f}")

def clear_inputs():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    add_placeholder(category_entry, "Category")
    add_placeholder(amount_entry, "Amount")
    add_button.config(text="Add")
    global selected_transaction_id
    selected_transaction_id = None

def on_transaction_select(event):
    global selected_transaction_id
    selected = transaction_list.selection()
    if not selected:
        return
    values = transaction_list.item(selected[0])['values']
    selected_transaction_id = values[0]
    type_var.set(values[1])
    category_entry.delete(0, tk.END)
    category_entry.insert(0, values[2])
    category_entry.config(fg='black')
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, values[3])
    amount_entry.config(fg='black')
    add_button.config(text="Update")

def delete_transaction():
    selected = transaction_list.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a transaction to delete.")
        return
    transaction_id = transaction_list.item(selected[0])['values'][0]
    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this transaction?")
    if confirm:
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        conn.commit()
        update_transaction_list()
        update_summary()
        clear_inputs()

def show_expense_chart():
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("No Data", "No expense data to visualize.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

def export_to_csv():
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("No Data", "No transactions to export.")
        return

    with open("budget_report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Type", "Category", "Amount", "Date"])
        for row in data:
            writer.writerow(row)

    messagebox.showinfo("Success", "Exported to budget_report.csv")

def apply_filter():
    category = filter_category_entry.get()
    date = filter_date_entry.get()
    update_transaction_list(filter_category=category, filter_date=date)

# ---------- GUI Setup ----------
app = tk.Tk()
app.title("Budget Tracker of Angel Naitbj C777®")
app.geometry("950x650")

selected_transaction_id = None

# --- Input Frame ---
input_frame = tk.Frame(app)
input_frame.pack(pady=10)

type_var = tk.StringVar(value="Expense")
tk.OptionMenu(input_frame, type_var, "Income", "Expense").grid(row=0, column=0, padx=5)

category_entry = tk.Entry(input_frame)
category_entry.grid(row=0, column=1, padx=5)
add_placeholder(category_entry, "Category")

amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=0, column=2, padx=5)
add_placeholder(amount_entry, "Amount")

add_button = tk.Button(input_frame, text="Add", command=add_transaction)
add_button.grid(row=0, column=3, padx=5)

delete_button = tk.Button(input_frame, text="Delete", command=delete_transaction)
delete_button.grid(row=0, column=4, padx=5)

visualize_button = tk.Button(input_frame, text="Visualize", command=show_expense_chart)
visualize_button.grid(row=0, column=5, padx=5)

export_button = tk.Button(input_frame, text="Export CSV", command=export_to_csv)
export_button.grid(row=0, column=6, padx=5)

# --- Filter Frame ---
filter_frame = tk.Frame(app)
filter_frame.pack(pady=5)

filter_category_entry = tk.Entry(filter_frame)
filter_category_entry.grid(row=0, column=0, padx=5)
add_placeholder(filter_category_entry, "Filter by Category")

filter_date_entry = tk.Entry(filter_frame)
filter_date_entry.grid(row=0, column=1, padx=5)
add_placeholder(filter_date_entry, "Filter by Date (YYYY-MM-DD)")

filter_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filter)
filter_button.grid(row=0, column=2, padx=5)

# --- Summary Frame ---
summary_frame = tk.Frame(app)
summary_frame.pack(pady=10)

income_label = tk.Label(summary_frame, text="Income: #0.00", fg="green")
income_label.pack(side=tk.LEFT, padx=10)

expense_label = tk.Label(summary_frame, text="Expenses: #0.00", fg="red")
expense_label.pack(side=tk.LEFT, padx=10)

balance_label = tk.Label(summary_frame, text="Balance: #0.00", fg="blue")
balance_label.pack(side=tk.LEFT, padx=10)

# --- Transaction List with Scrollbars ---
tree_frame = tk.Frame(app)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")

transaction_list = ttk.Treeview(
    tree_frame,
    columns=("ID", "Type", "Category", "Amount", "Date"),
    show="headings",
    yscrollcommand=tree_scroll_y.set,
    xscrollcommand=tree_scroll_x.set
)

tree_scroll_y.config(command=transaction_list.yview)
tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

tree_scroll_x.config(command=transaction_list.xview)
tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

for col in ("ID", "Type", "Category", "Amount", "Date"):
    transaction_list.heading(col, text=col)
    transaction_list.column(col, width=150, anchor="center")

transaction_list.pack(fill=tk.BOTH, expand=True)
transaction_list.bind("<<TreeviewSelect>>", on_transaction_select)

# --- Initialize ---
update_transaction_list()
update_summary()
plt.show()
app.mainloop()
plt.show()
