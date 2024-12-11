# import joblib
# import pandas as pd

# # Room_number, Squares, Floor, Place_ZHD, Place_Kirov, Place_Lenin, Place_October, Place_Firstmay, Place_Proletar, Place_Soviet

# model = joblib.load('apartment_cost.pkl')

# room_number = int(input('Количество комнат: '))
# squares = int(input('Площадь: '))
# floor = int(input('Этаж: '))
# # place = int(input('Район: '))

# data = [[room_number, squares, floor, 1, 0, 0, 0, 0, 0, 0]]

# predicted_price = model.predict(data)

# print(f'Предсказанная стоимость квартиры: {predicted_price[0]}')

a = [1, 2, 3]

print(a[0] + 1)
