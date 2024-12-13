import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('/content/drive/MyDrive/Проект АдиМо/houses1.csv')
print(data.head(10))
print(data.info())
print(data.describe())

data.columns = data.columns.str.strip()

print("Столбцы до удаления:", data.columns)
if 'ID' in data.columns:
    data.drop(columns=['ID'], inplace=True)
else:
    print("'ID' не найден в DataFrame.")

data = data.dropna()

data = pd.get_dummies(data, columns=['Place'], drop_first=True)

X = data.drop('Price', axis=1)
y = data['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")
print(f"Средняя абсолютная ошибка (MAE): {mae:.2f}")

pd.options.display.float_format = '{:,.0f}'.format

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7, edgecolors='k', label="Предсказания")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label="Идеальное соответствие")
plt.xlabel("Реальная цена")
plt.ylabel("Предсказанная цена")
plt.title("Реальная vs Предсказанная цена")
plt.legend()
plt.grid(True)
plt.show()

errors = y_test - y_pred
plt.figure(figsize=(8, 6))
sns.histplot(errors, kde=True, bins=30, color="blue", edgecolor="k", label="Ошибки")
plt.axvline(0, color='red', linestyle='--', label="Нулевая ошибка")
plt.xlabel("Ошибка (реальная - предсказанная)")
plt.ylabel("Частота")
plt.title("Распределение ошибок")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label="Реальная цена", linestyle='-', marker='o', alpha=0.7)
plt.plot(y_pred, label="Предсказанная цена", linestyle='--', marker='x', alpha=0.7)
plt.xlabel("Индекс наблюдения")
plt.ylabel("Цена")
plt.title("Реальная vs Предсказанная цена (по индексам)")
plt.legend()
plt.grid(True)
plt.show()

results = pd.DataFrame({
    'Реальная цена': y_test.values,
    'Предсказанная цена': y_pred,
    'Абсолютная ошибка': np.abs(y_test.values - y_pred),
    'Относительная ошибка (%)': np.abs((y_test.values - y_pred) / y_test.values) * 100
})

print("\nПервые 10 строк результатов:")
print(results.head(10))