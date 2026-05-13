from tkinter import *
import sqlite3
import matplotlib.pyplot as plt

# ---------------- DATABASE SETUP ----------------

conn = sqlite3.connect("expenses.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")

conn.commit()

conn.close()

# ---------------- SAVE EXPENSE FUNCTION ----------------

def save_expense():

    if amount.get() == "" or description.get() == "":
        status_label.config(text="Please fill all fields")
        return

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses(category, amount, description) VALUES (?, ?, ?)",
        (
            selected_category.get(),
            amount.get(),
            description.get()
        )
    )

    conn.commit()

    conn.close()

    status_label.config(text="Expense Saved Successfully")

    amount.delete(0, END)

    description.delete(0, END)

# ---------------- SHOW EXPENSES FUNCTION ----------------

def show_expenses():

    expense_list.delete(0, END)

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")

    rows = cursor.fetchall()

    for row in rows:

        expense_list.insert(END, row)

    conn.close()

# ---------------- SHOW CHART FUNCTION ----------------

def show_chart():

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    data = cursor.fetchall()

    categories = []

    amounts = []

    for row in data:

        categories.append(row[0])

        amounts.append(row[1])

    plt.figure(figsize=(6, 6))

    plt.pie(
        amounts,
        labels=categories,
        autopct='%1.1f%%'
    )

    plt.title("Expense Distribution")

    plt.show()

    conn.close()

# ---------------- DELETE EXPENSE FUNCTION ----------------

def delete_expense():

    selected = expense_list.curselection()

    if not selected:
        status_label.config(text="Please select an expense")
        return

    item = expense_list.get(selected)

    expense_id = item[0]

    conn = sqlite3.connect("expenses.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (expense_id,)
    )

    conn.commit()

    conn.close()

    status_label.config(text="Expense Deleted Successfully")

    show_expenses()

# ---------------- GUI ----------------

root = Tk()

root.title("Expense Tracker")

root.geometry("650x650")

root.configure(bg="#dbeafe")

# ---------------- HEADING ----------------

Label(
    root,
    text="Expense Tracker",
    font=("Arial", 22, "bold"),
    bg="#dbeafe",
    fg="#1e3a8a"
).pack(pady=15)

# ---------------- CATEGORY ----------------

Label(
    root,
    text="Category",
    font=("Arial", 12),
    bg="#dbeafe"
).pack()

categories = ["Food", "Travel", "Shopping", "Bills"]

selected_category = StringVar()

selected_category.set(categories[0])

dropdown = OptionMenu(
    root,
    selected_category,
    *categories
)

dropdown.config(
    font=("Arial", 11),
    width=20
)

dropdown.pack(pady=5)

# ---------------- AMOUNT ----------------

Label(
    root,
    text="Amount",
    font=("Arial", 12),
    bg="#dbeafe"
).pack()

amount = Entry(
    root,
    font=("Arial", 12),
    width=30
)

amount.pack(pady=5)

# ---------------- DESCRIPTION ----------------

Label(
    root,
    text="Description",
    font=("Arial", 12),
    bg="#dbeafe"
).pack()

description = Entry(
    root,
    font=("Arial", 12),
    width=30
)

description.pack(pady=5)

# ---------------- BUTTONS ----------------

Button(
    root,
    text="Save Expense",
    command=save_expense,
    bg="#22c55e",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=8)

Button(
    root,
    text="Show Expenses",
    command=show_expenses,
    bg="#3b82f6",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=8)

Button(
    root,
    text="Show Chart",
    command=show_chart,
    bg="#f59e0b",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=8)

Button(
    root,
    text="Delete Expense",
    command=delete_expense,
    bg="#ef4444",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=8)

# ---------------- STATUS LABEL ----------------

status_label = Label(
    root,
    text="",
    font=("Arial", 11),
    bg="#dbeafe",
    fg="green"
)

status_label.pack(pady=10)

# ---------------- EXPENSE LIST ----------------

expense_list = Listbox(
    root,
    width=80,
    height=15,
    font=("Courier New", 10)
)

expense_list.pack(pady=20)

# ---------------- RUN APP ----------------

root.mainloop()