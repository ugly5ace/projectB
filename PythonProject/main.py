import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, norm, poisson, ttest_ind

n = 1000
p = 0.25
p_ge_300 = 1 - binom.cdf(299, n, p)
p_eq_200 = binom.pmf(200, n, p)
p_lt_100 = binom.cdf(99, n, p)
print("1. Анализ клиентов:")
print("P(X ≥ 300) =", p_ge_300)
print("P(X = 200) =", p_eq_200)
print("P(X < 100) =", p_lt_100)
sim1 = np.random.binomial(n, p, 10000)
plt.hist(sim1, bins=30, color='skyblue', edgecolor='black')
plt.title("Распределение покупателей")
plt.show()

mu = 3
sigma = 0.5
samples = np.random.normal(mu, sigma, 1000)
plt.hist(samples, bins=30, color='lightgreen', edgecolor='black')
plt.title("Распределение времени загрузки")
plt.show()
p_less_2 = norm.cdf(2, mu, sigma)
p_more_4 = 1 - norm.cdf(4, mu, sigma)
num_more_4 = p_more_4 * 1000
print("\n2. Время загрузки:")
print("P(X < 2) =", p_less_2)
print("Количество загрузок > 4 сек =", num_more_4)

n = 1000
p = 0.15
sim2 = np.random.binomial(n, p, 10000)
plt.hist(sim2, bins=30, color='lightcoral', edgecolor='black')
plt.title("Распределение кликов")
plt.show()
p_less_100 = binom.cdf(99, n, p)
p_more_150 = 1 - binom.cdf(150, n, p)
p_between_120_140 = binom.cdf(140, n, p) - binom.cdf(119, n, p)
print("\n3. Рекламная компания:")
print("P(X < 100) =", p_less_100)
print("P(X > 150) =", p_more_150)
print("P(120 ≤ X ≤ 140) =", p_between_120_140)

lam = 10
sim3 = np.random.poisson(lam, 10000)
plt.hist(sim3, bins=range(0, 26), color='lightblue', edgecolor='black')
plt.title("Распределение звонков")
plt.show()
p_less_5 = poisson.cdf(4, lam)
p_eq_10 = poisson.pmf(10, lam)
p_more_15 = 1 - poisson.cdf(15, lam)
print("\n4. Колл-центр:")
print("P(X < 5) =", p_less_5)
print("P(X = 10) =", p_eq_10)
print("P(X > 15) =", p_more_15)

before = np.random.normal(10000, 2000, 30)
after = np.random.normal(12000, 2500, 30)
t_stat, p_value = ttest_ind(after, before)
plt.hist(before, bins=15, alpha=0.7, label='До компании')
plt.hist(after, bins=15, alpha=0.7, label='После компании')
plt.title("Сравнение выручки")
plt.legend()
plt.show()
print("\n5. Тестирование гипотез:")
print("t =", t_stat)
print("p =", p_value)
if p_value < 0.05:
    print("Результат: компания эффективна")
else:
    print("Результат: различий нет")
