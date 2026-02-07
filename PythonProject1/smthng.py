import tkinter as tk
from tkinter import ttk, messagebox
import json, os
from datetime import datetime
import matplotlib.pyplot as plt


# ----------------- ФАЙЛЫ -----------------
PURCHASES_FILE = "purchases.json"
MOM_FILE = "mom_orders.json"
NOTES_FILE = "notes.txt"


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# ----------------- ГЛАВНОЕ ОКНО -----------------
app = tk.Tk()
app.title("Bichak.UZ — Учёт и Бизнес")
app.geometry("1200x700")
app.configure(bg="#1e1e1e")

accent = "#ff6b6b"
yellow = "#ffe17a"

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 11))
style.configure("TButton", padding=5, font=("Arial", 10))
style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=28)
style.map("Treeview", background=[("selected", "#444444")])

tab_control = ttk.Notebook(app)
tab_control.pack(fill="both", expand=True, padx=10, pady=10)


frame_exp = tk.Frame(tab_control, bg="#1e1e1e")
tab_control.add(frame_exp, text="Расходы")

purchases = load_json(PURCHASES_FILE)

left_panel = tk.LabelFrame(frame_exp, text="Добавить расход", bg="#1e1e1e", fg=yellow, padx=15, pady=15)
left_panel.grid(row=0, column=0, sticky="n", padx=20, pady=20)

ttk.Label(left_panel, text="Название:").grid(row=0, column=0, sticky="w", pady=5)
entry_name = ttk.Entry(left_panel, width=30)
entry_name.grid(row=1, column=0, pady=5)

ttk.Label(left_panel, text="Цена:").grid(row=2, column=0, sticky="w", pady=5)
entry_price = ttk.Entry(left_panel, width=30)
entry_price.grid(row=3, column=0, pady=5)

ttk.Label(left_panel, text="Категория:").grid(row=4, column=0, sticky="w", pady=5)
combo_cat = ttk.Combobox(left_panel, values=["Еда", "Дом", "Транспорт", "Развлечения", "Другое"], width=28)
combo_cat.current(0)
combo_cat.grid(row=5, column=0, pady=5)


def add_purchase():
    name = entry_name.get().strip()
    price_text = entry_price.get().strip()
    cat = combo_cat.get()

    if not name or not price_text:
        return messagebox.showwarning("Ошибка", "Заполни все поля")

    try:
        price = float(price_text)
    except:
        return messagebox.showwarning("Ошибка", "Цена должна быть числом")

    purchases.append({
        "name": name,
        "price": price,
        "category": cat,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_json(PURCHASES_FILE, purchases)
    update_purchases()
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)


def update_purchases():
    tree.delete(*tree.get_children())
    total = 0

    for item in purchases:
        tree.insert("", tk.END,
                    values=(item["name"], item["price"], item["category"], item["date"]))
        total += item["price"]

    lbl_total.config(text=f"Итого: {total} UZS")


btn_add = ttk.Button(left_panel, text="Добавить", command=add_purchase)
btn_add.grid(row=6, column=0, pady=10)

right_panel = tk.Frame(frame_exp, bg="#1e1e1e")
right_panel.grid(row=0, column=1, padx=20, pady=20, sticky="n")

tree = ttk.Treeview(
    right_panel,
    columns=("name", "price", "category", "date"),
    show="headings",
    height=18
)
tree.grid(row=0, column=0, padx=10, pady=10)

for col, txt in zip(("name", "price", "category", "date"), ("Название", "Цена", "Категория", "Дата")):
    tree.heading(col, text=txt)
    tree.column(col, width=150)

lbl_total = tk.Label(right_panel, text="Итого: 0 UZS", font=("Arial", 15, "bold"), fg=accent, bg="#1e1e1e")
lbl_total.grid(row=1, column=0, pady=10)

update_purchases()


frame_mom = tk.Frame(tab_control, bg="#1e1e1e")
tab_control.add(frame_mom, text="Мамин бизнес")

orders = load_json(MOM_FILE)

mom_left = tk.LabelFrame(frame_mom, text="Новый заказ", fg=yellow, bg="#1e1e1e", padx=15, pady=15)
mom_left.grid(row=0, column=0, sticky="n", padx=20, pady=20)

ttk.Label(mom_left, text="Клиент:").grid(row=0, column=0, sticky="w", pady=5)
entry_client = ttk.Entry(mom_left, width=30)
entry_client.grid(row=1, column=0, pady=5)

ttk.Label(mom_left, text="Товар:").grid(row=2, column=0, sticky="w", pady=5)
entry_product = ttk.Entry(mom_left, width=30)
entry_product.grid(row=3, column=0, pady=5)

ttk.Label(mom_left, text="Цена:").grid(row=4, column=0, sticky="w", pady=5)
entry_price2 = ttk.Entry(mom_left, width=30)
entry_price2.grid(row=5, column=0, pady=5)

ttk.Label(mom_left, text="Статус:").grid(row=6, column=0, sticky="w", pady=5)
combo_status = ttk.Combobox(mom_left, values=["Ожидает", "Готово", "Доставлено"], width=28)
combo_status.current(0)
combo_status.grid(row=7, column=0, pady=5)


def add_order():
    c = entry_client.get().strip()
    p = entry_product.get().strip()
    t = entry_price2.get().strip()
    s = combo_status.get()

    if not c or not p or not t:
        return messagebox.showwarning("Ошибка", "Заполни все поля")

    try:
        price = float(t)
    except:
        return messagebox.showwarning("Ошибка", "Цена должна быть числом")

    orders.append({"client": c, "product": p, "price": price, "status": s})
    save_json(MOM_FILE, orders)
    update_orders()


ttk.Button(mom_left, text="Добавить заказ", command=add_order).grid(row=8, column=0, pady=10)

mom_right = tk.Frame(frame_mom, bg="#1e1e1e")
mom_right.grid(row=0, column=1, padx=20, pady=20, sticky="n")

mom_tree = ttk.Treeview(
    mom_right,
    columns=("client", "product", "price", "status"),
    show="headings",
    height=18
)
mom_tree.grid(row=0, column=0, padx=10, pady=10)

for col, txt in zip(("client", "product", "price", "status"), ("Клиент", "Товар", "Цена", "Статус")):
    mom_tree.heading(col, text=txt)
    mom_tree.column(col, width=180)


def update_orders():
    mom_tree.delete(*mom_tree.get_children())
    total = 0

    for o in orders:
        mom_tree.insert("", tk.END, values=(o["client"], o["product"], o["price"], o["status"]))
        total += o["price"]

    lbl_total_orders.config(text=f"Сумма заказов: {total} UZS")


lbl_total_orders = tk.Label(mom_right, text="Сумма заказов: 0 UZS",
                            font=("Arial", 15, "bold"),
                            fg=accent, bg="#1e1e1e")
lbl_total_orders.grid(row=1, column=0, pady=10)

update_orders()


frame_notes = tk.Frame(tab_control, bg="#1e1e1e")
tab_control.add(frame_notes, text="Заметки")

txt = tk.Text(frame_notes, width=100, height=30, bg="#2c2c2c", fg="white", font=("Arial", 12))
txt.grid(row=0, column=0, padx=20, pady=20)
txt.insert("1.0", load_notes())


def save_notes_btn():
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write(txt.get("1.0", tk.END))
    messagebox.showinfo("OK", "Заметки сохранены")


ttk.Button(frame_notes, text="Сохранить", command=save_notes_btn).grid(row=1, column=0, pady=10)


frame_an = tk.Frame(tab_control, bg="#1e1e1e")
tab_control.add(frame_an, text="Аналитика")


def chart_expenses():
    if not purchases:
        return messagebox.showinfo("Нет данных", "Нет расходов")

    cats = {}
    for p in purchases:
        cats[p["category"]] = cats.get(p["category"], 0) + p["price"]

    plt.figure(figsize=(6, 6))
    plt.title("Расходы по категориям")
    plt.pie(cats.values(), labels=cats.keys(), autopct="%1.1f%%")
    plt.show()


ttk.Button(frame_an, text="График расходов", command=chart_expenses).pack(pady=30)


app.mainloop()
