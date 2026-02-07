from flask import Flask, render_template, request
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MENU = [
    {
        "id": "meat",
        "name": "Сомса с мясом",
        "price": 25000,
        "image": "meat.jpg",
        "popular": True
    },
    {
        "id": "greens",
        "name": "Сомса с зеленью",
        "price": 15000,
        "image": "greens.jpg",
        "popular": False
    },
    {
        "id": "cheese_greens",
        "name": "Сомса с сыром и зеленью",
        "price": 20000,
        "image": "cheese_greens.jpg",
        "popular": True
    },
    {
        "id": "pumpkin",
        "name": "Сомса с тыквой",
        "price": 15000,
        "image": "pumpkin.jpg",
        "popular": False
    }
]

app = Flask(__name__)

ADMIN_EMAIL = "netvoedelo"
ADMIN_PHONE = "tvoedelo"


def load(filename):
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(filename, data):
    path = os.path.join(BASE_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    phone = request.form["phone"]

    users = load("users.json")

    role = "admin" if email == ADMIN_EMAIL and phone == ADMIN_PHONE else "client"


    users.append({
        "email": email,
        "phone": phone,
        "role": role
    })

    save("users.json", users)

    if role == "admin":
        orders = load("orders.json")
        return render_template("admin.html", users=users, orders=orders)

    return render_template("menu.html", email=email)


@app.route("/order", methods=["POST"])
def order():
    cart = []
    total = 0

    for item in MENU:
        qty = int(request.form.get(item["id"], 0))
        if qty > 0:
            cost = qty * item["price"]
            cart.append(f'{item["name"]} ×{qty} — {cost} сум')
            total += cost

    if total < 50000:
        return "Минимальный заказ — 50 000 сум"

    message = "🥟 Новый заказ — Shakar Somsa\n\n"
    message += "\n".join(cart)
    message += f"\n\nИтого: {total} сум"

    send_telegram(message)

    orders = load("orders.json")
    orders.append({"cart": cart, "total": total})
    save("orders.json", orders)

    return "Заказ принят ✅"


if __name__ == "__main__":
  app.run(debug=True)


