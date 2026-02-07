# Случайный Лес (Random Forest)

# Это ансамблевый метод машинного обучения, который строит
# множество деревьев решений во время обучения и выводит среднее их предсказаний
# (для задач регрессии) или наиболее популярный класс (для задач классификации).

# Как работает:
# 1.  Бэггинг (Bootstrap Aggregating): Создаются случайные подвыборки из
#  обучающего набора данных с возвращением (некоторые образцы могут
#  повторяться, некоторые – отсутствовать). На каждой такой подвыборке
#  обучается отдельное дерево решений.

# 2.  **Случайность признаков (Feature Randomness):** При построении каждого узла
#  в каждом дереве выбирается случайное подмножество признаков, и лучший
#  разделитель ищется только среди них. Это делает деревья более разнообразными.

# Импорт необходимых библиотек
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor  # Модель Случайного Леса для задач регрессии
from sklearn.metrics import mean_squared_error, r2_score  # Метрики для оценки качества модели
import random  # Модуль для генерации случайных чисел

random.seed(42)

print("Шаг 1: Генерация синтетических данных...")
# Задаем диапазоны значений для признаков и целевой переменной
square_range = (80, 400)       # Площадь дома (м2)
rooms_range = (2, 7)           # Количество комнат
year_range = (1980, 2022)      # Год постройки
garage_options = (0, 1)        # Наличие гаража (0 - нет, 1 - да)
price_base = 50000             # Базовая цена
price_per_sq_meter = 3000      # Цена за квадратный метр
price_per_room = 15000         # Надбавка за комнату
price_per_year_factor = 500    # Надбавка за более новый год постройки
garage_bonus = 70000           # Надбавка за гараж
noise_factor = 50000           # Фактор случайного "шума" для цены

num_samples = 2000
# Увеличим количество образцов для более стабильных результатов

# Генерируем данные с некоторой логикой, чтобы модель могла что-то выучить
data_list = []
for _ in range(num_samples):
    sq = random.randint(*square_range)
    rooms = random.randint(*rooms_range)
    year_build = random.randint(*year_range)
    garage = random.choice(garage_options)

    price = (
        price_base + sq * price_per_sq_meter + rooms * price_per_room +
        (year_build - year_range[0]) * price_per_year_factor +
        garage * garage_bonus + random.uniform(-noise_factor, noise_factor)
    )

    price = int(abs(price))
    data_list.append([sq, rooms, year_build, garage, price])


# Создание DataFrame из списка
data = pd.DataFrame(data_list, columns=['Площадь', 'Комнаты', 'Год_постройки', 'Гараж', 'Цена'])
print("Пример сгенерированных данных (первые 5 строк):")
print(data.head())
print("-" * 30)

print("Шаг 2: Подготовка данных (разделение на признаки и целевую переменную)...")
X = data[['Площадь', 'Комнаты', 'Год_постройки', 'Гараж']]  # Признаки
y = data['Цена'] # Целевая переменная

print("Шаг 3: Разделение данных на обучающую и тестовую выборки...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# RandomForestRegressor - это класс из библиотеки scikit-learn для создания модели случайного леса
# для регрессии.
# n_estimators - это один из важнейших гиперпараметров, он задает количество деревьев в "лесу".
# random_state=42 используется для того, чтобы результаты были воспроизводимы.
print("Шаг 4: Обучение модели Случайного Леса...")
model = RandomForestRegressor(n_estimators=15, random_state=42, max_depth=20,
                              min_samples_split=8, min_samples_leaf=3)
# Добавлены гиперпараметры для предотвращения переобучения:
# max_depth: максимальная глубина каждого дерева.
# min_samples_split: минимальное количество образцов, необходимых для разделения внутреннего узла.
# min_samples_leaf: минимальное количество образцов, которые должны быть в листовом узле.
model.fit(X_train, y_train)
print("Модель успешно обучена.")
print("-" * 30)

# --- Оценка качества модели на тестовой выборке ---
print("Шаг 5: Оценка качества модели на тестовой выборке...")
# .predict() - метод для получения предсказаний от обученной модели на новых данных (X_test).
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"Среднеквадратичная ошибка (MSE) на тестовой выборке: {mse:.2f}")
print(f"Среднеквадратичная ошибка (MSE) на тестовой выборке: {mse**0.5:.2f}")

r2 = r2_score(y_test, y_pred)
print(f"Коэффициент детерминации (R²) на тестовой выборке: {r2:.4f}")
# Если R² близок к 1, это означает, что модель хорошо объясняет данные.
# Если R² близок к 0, модель плохо объясняет данные.
# Отрицательный R2 означает, что модель работает хуже, чем простое усреднение.

# --- Важность признаков ---
print("Шаг 6: Оценка важности признаков...")
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'Признак': feature_names, 'Важность': importances})
feature_importance_df = feature_importance_df.sort_values(by='Важность', ascending=False)

print("Важность признаков:")
print(feature_importance_df)

import matplotlib.pyplot as plt
# Визуализация важности признаков
plt.figure(figsize=(10, 6))
plt.bar(feature_importance_df['Признак'], feature_importance_df['Важность'], color='skyblue')
plt.xlabel('Признаки')
plt.ylabel('Важность')
plt.title('Важность признаков в модели Случайного Леса')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
