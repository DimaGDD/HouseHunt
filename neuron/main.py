import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def load_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df


def preprocess_data(df):
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

    label_encoder = LabelEncoder()
    df['Place'] = label_encoder.fit_transform(df['Place'])

    return df, label_encoder

def train_model(df):
    X = df[['Room_number', 'Squares', 'Floor', 'Place']]
    y = df['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = model.score(X_test, y_test) * 100
    print(f"Точность на тестовом наборе: {accuracy:.2f}")

    plot_predictions(y_test, y_pred)

    return model


def predict_price(model, label_encoder, room_number, squares, floor, place):
    place_encoded = label_encoder.transform([place])[0]
    features = pd.DataFrame([[room_number, squares, floor, place_encoded]], columns=['Room_number', 'Squares', 'Floor', 'Place'])
    predicted_price = model.predict(features)[0]
    return predicted_price


def plot_predictions(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print(f"Средняя абсолютная ошибка (MAE): {mae:.2f}")
    
    # График предсказаний vs реальные значения
    plt.figure(figsize=(12, 6))
    
    # Scatter Plot: Реальные значения vs предсказания
    plt.subplot(1, 2, 1)
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Идеальное предсказание')
    plt.xlabel("Реальные значения")
    plt.ylabel("Предсказанные значения")
    plt.title("Реальные значения vs Предсказания")
    plt.legend()
    
    # Residual Plot: Ошибки предсказания
    residuals = y_test - y_pred
    plt.subplot(1, 2, 2)
    plt.scatter(y_pred, residuals, alpha=0.6, color="purple")
    plt.axhline(0, color='r', linestyle='--', label="Нулевая ошибка")
    plt.xlabel("Предсказанные значения")
    plt.ylabel("Остатки (реальные - предсказанные)")
    plt.title("График ошибок (Residual Plot)")
    plt.legend()
    
    plt.tight_layout()
    plt.show()


filepath = 'houses.csv'
df = load_data(filepath)
df, label_encoder = preprocess_data(df)
model = train_model(df)



def start(model, label_encoder):
    room_number = int(input('Количество комнат --> '))
    squares = float(input('Площадь --> '))
    floor = int(input('Этаж --> '))
    place = input('Район --> ')

    predict_price_value = predict_price(model, label_encoder, room_number, squares, floor, place)

    print(f'Средняя цена для квартира: {predict_price_value:.2f}')



if __name__ == '__main__':
    start(model, label_encoder)