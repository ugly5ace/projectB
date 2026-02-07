# Введение во временные ряды

# Временной ряд — это последовательность наблюдений или данных,
# записанных в последовательные моменты времени.

# Применение:
# Финансовые данные: цены акций, валютные курсы, объемы торгов.
# Экономические показатели: ВВП, уровень безработицы, инфляция.
# Погодные данные: температура, осадки, скорость ветра.
# Данные продаж: ежемесячные продажи продукта, посещаемость магазина.
# Трафик веб-сайта: количество посетителей за день, количество просмотров страниц.

# Особенности временных рядов

# Тренд (Trend):
# Определение: Долгосрочное общее направление изменения данных во времени.
# Тренд может быть восходящим (увеличение), нисходящим (уменьшение) или стабильным.

# Сезонность (Seasonality):
# Определение: Регулярные и предсказуемые колебания, которые повторяются с
# определенной периодичностью в рамках года, месяца или дня.

# Цикличность (Cyclical Component):
# Определение: Колебания, связанные с экономическими или другими циклами,
# которые не обязательно имеют фиксированный период.

# Шум (Noise):
# Определение: Случайные и непредсказуемые колебания, которые не могут
# быть объяснены трендом, сезонностью или цикличностью.

import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
data = pd.read_csv('AirPassengers.csv', index_col='Month', parse_dates=True)
data.index.freq = 'MS'  # Устанавливаем частоту: начало месяца

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Passengers'], label='Количество пассажиров')
plt.title('Международные авиаперевозки (1949-1960)')
plt.xlabel('Год')
plt.ylabel('Количество пассажиров')
plt.legend()
plt.show()

# Декомпозиция — процесс разделения временного ряда на его основные компоненты:
# тренд, сезонность и остаток (шум). Это помогает лучше понять структуру данных и
# выбрать подходящую модель для прогнозирования.

# Аддитивная модель: Когда амплитуда сезонных колебаний постоянна.
# Мультипликативная модель: Когда амплитуда сезонных колебаний меняется
# со временем (обычно увеличивается или уменьшается пропорционально тренду).

from statsmodels.tsa.seasonal import seasonal_decompose

# Декомпозиция временного ряда
result = seasonal_decompose(data['Passengers'], model='multiplicative')
result.plot()
plt.show()

# Стационарность временных рядов

# Стационарный временной ряд — это ряд, статистические свойства которого
# (например, среднее, дисперсия) постоянны во времени. Стационарность
# является важным свойством для моделирования временных рядов, особенно при
# использовании моделей ARIMA.

# Постоянное среднее: Среднее значение не меняется со временем.
# Постоянная дисперсия: Разброс данных вокруг среднего остается стабильным.
# Отсутствие сезонности и тренда: Нет долгосрочных изменений или регулярных колебаний.

# Тест Дики-Фуллера (Augmented Dickey-Fuller Test, ADF-тест):
# Гипотезы:
# Нулевая гипотеза (H0): Ряд имеет единичный корень (не стационарен).
# Альтернативная гипотеза (H1): Ряд стационарен.

from statsmodels.tsa.stattools import adfuller

# Применение ADF-теста
result = adfuller(data['Passengers'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])

# model ARIMA
# основные компоненты моделей АРИМА
# Arima (AutoRegressive Integrated Moving Average) - класс моделей для анализа и
#прогнозирования временных рядов который обьединяет три основных компонента

# AR - Авторегрессия - текущее значения зависят от предыдущих значений
# I - Интегрированность - количество дифференцирований необходимых для стационарности
# MA - Скользящее среднее - Текущее значения зависят от прошлых ошибок прогнозирования


# Применение первого дифференцирования
data_diff = data['Passenger'].diff().dropna()
# Дифференцирование значние - приводеит значения к стационарности
# Так как улбирается тренд
# Проверка стационарности дифференцированного ряда
result = adfuller(data_diff)

print('ADF Statistic after differencing :', result[0])
print('p-value:', result[1])

#Обучение модели
model = ARIMA(data['Passenger'], order=(1, 1, 1))
model_fit = model.fit = model.fit()
print(model_fit.summary())

forecast = model_fit.get_forecast(steps=12)
forecast_ci = forecast.conf_int()

plt.figure(figsize=(12, 6))
plt.plot(data.index, data['passenger'], label='Исторические данные')
plt.plot(forecast.predicted_meam.index, forecast.predicted_meam, label='Прогноз')
plt.fill_between(forecast_ci.index, forecast_ci.iloc[: , 0], forecast_ci.iloc[:, 1], alpha=0.3)
plt.legend()
plt.title('Прогноз пассажиропотока на 12 месяцев')
plt.show()

# SARIMA ARIMS(p, d, q)(P, D, Q, S),
# P - порядок сезонной авторегрессии
# D - порядок сезонного дифференцирования
# Q - порядок сезонного скользящего среднего
# s - длинна сезонности (напримерб s=12 для месячных данных с годовой сезооностью)
# Общая формула модели SARIMA
# SARIMA (p,d,q)(P,D,Q,s)

from statsmodels.tsa.statespace.sarimax import SARIMAX

#
model = SARIMAX(data['passenger'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit()
print(model_fit.summary())

plt.figure(figsize=(12, 6))
plt.plot(data.index, data['passenger'], label='Исторические данные')
plt.plot(forecast.predicted_meam.index, forecast.predicted_meam, label='Прогноз')
plt.fill_between(forecast_ci.index,
                 forecast_ci.iloc[: , 0],
                 forecast_ci.iloc[:, 1], alpha=0.3)

plt.figure(figsize=12, 6))
plt.plot(data.index, data['Passenger'], label='')
plt.title('Прогноз количества пассажиров на 24 месяца')
plt.xlabel('Год')
plt.ylabel('Пассажиры')
plt.legend()
plt.show()

from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(data['passsenger'], model='multiplicative')
result.plot()
plt.show()
from statsmodels.tsa.stattools import adfuller
result = adfuller(data['passenger'])
print('ADF Statisic:', result[0])
print ('p-value:', result[1])
from stats