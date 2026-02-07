import numpy as np
import pandas as pd
import joblib
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
from tkinter import ttk

from scipy.fft import hfftn

model = joblib.load('model.pkl')
le_marital = joblib.load('le_marital.pkl')
le_education = joblib.load('le_education.pkl')

def predict():
    pass


# tk.Tk() создает главное окно приложения. Это "корень" всех остальных виджетов.
root = tk.Tk()

# .title() - устанавливает заголовок окна.
root.title('Прогноз дефолта по кредитам v1.0 beta')

# .geometry() - устанавливает начальный размер окна (ширина x высота + смещениеX + смещениеY).
# Смещение опционально, например '450x350+100+100' откроет окно со смещением.
root.geometry('300x600')  # Немного увеличим окно для новых элементов

# .minsize(width, height) и .maxsize(width, height) - установка минимального/максимального
# размера окна
root.minsize(300, 250)

# Создадим кастомный шрифт
custom_font_label = tkFont.Font(family="Arial", size=10)
custom_font_entry = tkFont.Font(family="Courier New", size=10)

label_age = tk.Label(root, text="Возраст: ", font=custom_font_label, padx=10)
label_age.pack(pady=(10, 0))  # pady=(сверху, снизу) - кортеж для разных отступов
entry_age = tk.Entry(root, width=30)  # width - ширина в символах
entry_age.pack(pady=5)

label_income = tk.Label(root,  font=custom_font_label, text="Доход:")
label_income.pack(pady=(5, 0))
entry_income = tk.Entry(root, width=30)
entry_income.pack(pady=5)

label_rating = tk.Label(root, font=custom_font_label, text="Кредитный рейтинг:")
label_rating.pack(pady=(5, 0))
entry_rating = tk.Entry(root, width=30)
entry_rating.pack(pady=5)

label_experience = tk.Label(root, font=custom_font_label, text="Длительность работы (лет):")
label_experience.pack(pady=(5, 0))
entry_experience = tk.Entry(root, width=30)
entry_experience.pack(pady=5)

label_active_loan = tk.Label(root, font=custom_font_label, text="Активные кредиты:")
label_active_loan.pack(pady=(5, 0))
entry_active_loan = tk.Entry(root, width=30)
entry_active_loan.pack(pady=5)

label_payments = tk.Label(root, font=custom_font_label, text="Просроченные платежи:")
label_payments.pack(pady=(5, 0))
entry_payments = tk.Entry(root, width=30)
entry_payments.pack(pady=5)
label_education = tk.Label(root, font=custom_font_label, text="Образование:")
label_education.pack(pady=(5, 0))
# Создаем Combobox, значения берем из le_education.classes_
combo_education = ttk.Combobox(root, values=list(le_education.classes_), state="readonly")
combo_education.pack(fill='x', pady=(0, 10))
combo_education.current(0)  # Устанавливаем значение по умолчанию (первое в списке)

label_status = tk.Label(root, font=custom_font_label, text="Семейное положение:")
label_status.pack(pady=(5, 0))
# Создаем Combobox, значения берем из le_marital.classes_
combo_status = ttk.Combobox(root, values=list(le_marital.classes_), state="readonly")
combo_status.pack(fill='x', pady=(0, 20)) # Увеличим отступ снизу
combo_status.current(0) # Устанавливаем значение по умолчанию

btn_predict = tk.Button(root, text="Предсказать результат", command=predict,
    font=("Tahoma", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    relief=tk.RAISED,
    bd=2,  # bd - это сокращение для borderwidth
    padx=10,  # Внутренние отступы для текста кнопки
    pady=5
)
btn_predict.pack(pady=20)  # Внешний отступ для кнопки

# --- 4.3. Метка для вывода результата ---
label_result = tk.Label(
    root,
    text="Здесь будет результат...",
    font=("Arial", 12, "italic"),
    pady=10,
    # `wraplength` - ширина, после которой текст будет переноситься на новую строку (в пикселях)
    wraplength=380,
    # `justify` - выравнивание текста (tk.LEFT, tk.CENTER, tk.RIGHT)
    justify=tk.CENTER
)
label_result.pack(fill=tk.X, padx=10)  # fill=tk.X заставит метку растягиваться по горизонтали



# Запуск приложения
root.mainloop()


# Запуск приложения
root.mainloop()
def predict():
  try:
        age = int(entry_age.get())
        income = int(entry_income.get())
        rating = int(entry_rating.get())
        experinence =  int(entry_experience.get())
        active_loan = int(entry_active_loan.get())
        payments = int(entry_payments.get())

        education_str = combo_education.get()
        status_encoded = le_education.transfoem([status_str])[0]

        final_features = pd.DataFrame({
            "age": [age]
            "Lincome": [income]
            "rating": [rating]
            "Work (for years)": [experinence]
            "active_loan": [ active_loan]
            "payments": [payments]
            "educaiton": [ education_encoded]
            "status_encoded": [status_encoded]

        })




label_result.config(text=result_text)
if prediction[0] == 1
    label_result.config(fg="green")
else:
    label_result.config(fg="red")

    except Exception as e:
    print(e)
 messagebox.showerror("Неизвестная ошибка", "Произошла ошибка: {e}")

print(messagebox)
from tkinter import messagebox

if __name__ == '__main__':
    root.mainloop()
    root.mainloop()
getattr("huh")