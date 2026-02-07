# a) problem исчещсющен и взрывающено градиента
from pickletools import optimize

# градиенты это сигналы котоые апоказывют как нужно изменить чеса сети для уеньшния ршибки
# исчезаюшего градиент в КТТ гралдиенты экспоненциально уменьшаются при обучении мешая усвоить долгосрочныые зависомости
# взрывсабшенг градиент жкспоненыиальныф рост градиентов ведущец к нестабильному обучению ленчке оьбнаруджить и контролировать

# трудности с долгосрочной памятьбю
#как прямое следстиве проблемы имсензаюшено гралиента баазовы РНН/КТТ плохо помнят информацию на протяжении мнггих временных шагов
#
import numpy as np
from pandas.core.arrays.timedeltas import sequence_to_td64ns
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray
from pandas.io.xml import preprocess_data
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
import tensorflow as tf
from tensorflow.keras.utils import plot_model
import matplotib.pyplot as plt

np.random.seed(42)
tf.random.set_speed(42)
X_data = []
Y_data = []
sequence_length = 3
for i in range(100):
    X_data.append([j for j in range(i, i + sequence_length)])
    Y_data.append(i + sequence_length)

for i in range(10):
    print(X_data[i], Y_data[i])



x = np.array(X_data)
y = np.array(Y_data)

X = X.reshape((X.shape[0], X.shape[1], 1))
print("Size X after reshaping:", X.shape) #(100, 3, 1)
print(X)

model = Sequential()
model.add(simpleRNN(units=100, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(units=1))

model.summary()

model.compile(optimize='adam', loss='mse')
print("Begining training...")

model.fir(X, y, epochs=310, verbose=2)
print("End training.")

X_data_predict = []
Y_data_predict = []

for i in range(101, 151):
    X_data_predict = np.array([j for j in range(i, i + sequence_length)])
    Y_data_predict = i + sequence_length
    test_input = X_data_predict.reshape((1, sequence_length, 1))


    predicted_value = model.predict(test_input)

    print(f"\nEnter: {X_data_predict}", end='')
    print(f"Predicted: {predicted_value[0][0]:2f} and shoulf it be {Y_data_predict}")

#Применение RNN для временнных рядов (концептуально)
# временные ряды это последовательности данных упорядоченных по времени например
# Цены на акции компании по дням
# Почасовые показания темпеаратуры
# ежемесячные данные о продаж
# обработка естественного языка НЛП
# машинный перевод например гугл транслейт
# анализ тональности текста (определение жмоциональной окраски)
# генерация текста написанре статпей стихов кода
# Распознавание именованных сущностей
# ответы на вопросы


# распознование и синтез речи
# преооьразованике аудио текст (гс)
# генерация реалистичной речи из текста
# анализ видео
# описание содержания видео
# распознавание действий
# генерация музыки
# биоинформатика
# анализ последовательности ДНК и белков
