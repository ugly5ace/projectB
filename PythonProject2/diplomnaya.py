import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score



sns.set_theme(
    style="whitegrid",
    palette="Set2",
    font_scale=1.1
)

plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12


data = pd.DataFrame({
    "month": np.arange(1, 13),
    "active_users_thousands": [120, 135, 150, 170, 190, 215, 240, 265, 290, 320, 350, 380],
    "transaction_volume_billion": [1.2, 1.4, 1.6, 1.9, 2.2, 2.6, 3.0, 3.4, 3.9, 4.5, 5.0, 5.6],
    "avg_transaction_value": [150, 152, 155, 158, 160, 162, 165, 168, 170, 172, 175, 178]
})


plt.figure()
sns.lineplot(
    x="month",
    y="active_users_thousands",
    data=data,
    marker="o",
    linewidth=2.5
)
plt.title("Рост активных пользователей жопы Тимы в неделю")
plt.xlabel("Месяц")
plt.ylabel("Активные пользователи (тыс.)")
plt.tight_layout()
plt.show()

plt.figure()
sns.regplot(
    x="month",
    y="transaction_volume_billion",
    data=data,
    scatter_kws={"s": 70},
    line_kws={"linewidth": 3}
)
plt.title("Динамика объёма транзакций Uzum Bank")
plt.xlabel("Месяц")
plt.ylabel("Объём транзакций (млрд)")
plt.tight_layout()
plt.show()


plt.figure(figsize=(7, 5))
sns.heatmap(
    data.corr(),
    annot=True,
    fmt=".2f",
    cmap="RdYlGn",
    linewidths=0.5,
    cbar_kws={"shrink": 0.8}
)
plt.title("Корреляция финансовых показателей Uzum Bank")
plt.tight_layout()
plt.show()


X = data[['month', 'active_users_thousands', 'avg_transaction_value']]
y = data['transaction_volume_billion']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))

plt.figure()
sns.scatterplot(x=y_test, y=y_pred, s=80)
sns.lineplot(
    x=y_test,
    y=y_test,
    linewidth=2,
    linestyle="--"
)
plt.title("Качество прогноза модели (Uzum Bank)")
plt.xlabel("Реальный объём транзакций")
plt.ylabel("Прогноз модели")
plt.tight_layout()
plt.show()


plt.figure()
sns.scatterplot(x=y_test, y=t_pred, s=80)
sns.lineplot(
    x=y_test,
    y=y_test,
    linewidth=2,
    linestyle="--"

)
plt.title("Сколько мужиков ебали в жопу тимы за эту неделю")
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()
plt.show()
