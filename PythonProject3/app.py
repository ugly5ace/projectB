import os
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # важно для macOS + Flask (чтобы график сохранялся без окон)
import matplotlib.pyplot as plt

from flask import Flask, render_template
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

app = Flask(__name__)

MENU_CSV = os.path.join("csv", "menu.csv")
FORECAST_PNG = os.path.join("static", "forecast.png")


def load_menu() -> list[dict]:
    """
    Ожидаемые колонки в csv/menu.csv:
    name, price, description, image
    """
    df = pd.read_csv(MENU_CSV)
    # гарантируем нужные колонки (если вдруг порядок другой)
    df = df[["name", "price", "description", "image"]]
    return df.to_dict(orient="records")


def make_forecast_and_plot() -> dict:
    """
    Простая DS-часть: прогноз количества клиентов по месяцам.
    - обучаем LinearRegression
    - прогнозируем следующие 3 месяца
    - сохраняем график static/forecast.png
    - считаем MAE и R2 на обучающих данных (демонстрационно)
    """

    # Примерные данные (можно любые) — клиенты за 12 месяцев
    months = np.arange(1, 13).reshape(-1, 1)
    clients = np.array([920, 980, 1010, 1080, 1120, 1180, 1210, 1270, 1320, 1380, 1450, 1520])

    model = LinearRegression()
    model.fit(months, clients)

    # Метрики на обучающих данных (для демонстрации)
    train_pred = model.predict(months)
    mae = float(mean_absolute_error(clients, train_pred))
    r2 = float(r2_score(clients, train_pred))

    # Прогноз на 3 следующих месяца
    future_months = np.array([13, 14, 15]).reshape(-1, 1)
    forecast = model.predict(future_months)

    # График
    os.makedirs("static", exist_ok=True)
    plt.figure(figsize=(9, 5))
    plt.plot(months.flatten(), clients, marker="o", linewidth=2, label="Фактические клиенты")
    plt.plot(future_months.flatten(), forecast, marker="o", linestyle="--", linewidth=2, label="Прогноз (Linear Regression)")
    plt.title("Прогноз количества клиентов (Data Science)")
    plt.xlabel("Месяц")
    plt.ylabel("Клиенты")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FORECAST_PNG)
    plt.close()

    avg_clients = int(round(float(np.mean(clients))))
    # рост последнего факта -> первый прогноз (пример “роста в месяц”)
    monthly_growth_pct = float((forecast[0] - clients[-1]) / clients[-1] * 100.0)
    yearly_growth_pct = monthly_growth_pct * 12.0

    return {
        "avg_clients": avg_clients,
        "monthly_growth_pct": monthly_growth_pct,
        "yearly_growth_pct": yearly_growth_pct,
        "mae": mae,
        "r2": r2,
        "forecast_next_3": [int(round(float(x))) for x in forecast],
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    items = load_menu()
    return render_template("menu.html", menu=items)


@app.route("/forecast")
def forecast():
    stats = make_forecast_and_plot()
    return render_template("forecast.html", stats=stats)


if __name__ == "__main__":
    app.run(debug=True, port=5001)



