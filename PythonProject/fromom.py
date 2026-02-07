import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "purchases.json"


def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def update_list():
    listbox.delete(0, tk.END)
    total = 0

    for item in data:
        listbox.insert(tk.END, f"{item['name']} — {item['price']} руб")
        total += item["price"]

    total_label.config(text=f"Сумма: {total} руб")


def add_purchase():
    name = name_entry.get().strip()
    price_text = price_entry.get().strip()

    if not name or not price_text:
        messagebox.showwarning("Ошибка", "Заполни оба поля!")
        return

    try:
        price = float(price_text)
    except ValueError:
        messagebox.showwarning("Ошибка", "Цена должна быть числом")
        return

    data.append({"name": name, "price": price})
    save_data(data)
    update_list()

    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)


# Загружаем данные
data = load_data()

# Окно
window = tk.Tk()
window.title("Учёт покупок")
window.geometry("400x500")

# Поле для названия
tk.Label(window, text="Название продукта").pack()
name_entry = tk.Entry(window, font=("Arial", 14))
name_entry.pack(pady=5)

# Поле для цены
tk.Label(window, text="Цена (руб)").pack()
price_entry = tk.Entry(window, font=("Arial", 14))
price_entry.pack(pady=5)

# Кнопка
add_btn = tk.Button(window, text="Добавить", font=("Arial", 14), command=add_purchase)
add_btn.pack(pady=10)

# Список покупок
listbox = tk.Listbox(window, width=40, height=15, font=("Arial", 12))
listbox.pack(pady=10)

# Сумма
total_label = tk.Label(window, text="Сумма: 0 руб", font=("Arial", 14, "bold"))
total_label.pack(pady=5)

# Обновляем список при запуске
update_list()

window.mainloop()
