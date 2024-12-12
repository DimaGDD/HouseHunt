# 🏠 HouseHunt

**HouseHunt** - это проект, который поможет вам узнать стоимость квартир в Ростове-на-Дону, указав подходящие для вас параметры!

---

## 📸 Превью

- **[Главный экран](https://dimagdd.github.io/HouseHunt/index.html)**

  ![Главный экран](img/home.png)

- **[Экран с моделью](https://dimagdd.github.io/HouseHunt/model.html)**

  ![Экран с моделью](img/model.png)

- **Telegram бот**: [@Houses_Hunters_Bot](https://t.me/Houses_Hunters_Bot)

  ![Телеграм бот](img/tg_bot.png)

---

## 📂 Структура проекта

1. [**`main`**](https://github.com/DimaGDD/HouseHunt) - Основная ветка, где хранится рабочая версия проекта.
   
3. В других ветках лежат скрипты и экспериментальные функции для доработки проекта. Эти ветки могут быть не всегда стабильны.
   - [**`neuron`**](https://github.com/DimaGDD/HouseHunt/tree/neuron) - модель
   - [**`parser`**](https://github.com/DimaGDD/HouseHunt/tree/parser) - парсер
   - [**`tg_bot`**](https://github.com/DimaGDD/HouseHunt/tree/tg_bot) - телеграм бот
   - [**`web_site`**](https://github.com/DimaGDD/HouseHunt/tree/web_site) - сайт
     
4. Дополнительная информация о каждой ветке находится в её собственном `README.md`.

---

## 🚀 Установка и запуск

1. **Склонируйте репозиторий**:
   
   ```bash
   git clone https://github.com/ваш_репозиторий.git
   
2. У вас появятся несколько папок:
   - **`neuron`** - папка с моделью, которая обучается если предоставить ей данные, мы используем формат csv
   - **`parser`** - папка с парсером, который заходит на сайт avito и парсит объявления
   - **`tg_bot`** - папка с telegram ботом
   - **`web_site`** - папка с сайтом, здесь находится как frontend, так и backend

3. Для начала работы необходимо создать виртуальное окружение

   ```bash
   python -m venv venv

4. В каждой папке лежит файл **`requirementx.txt`** со всеми зависимостями. Необходимо пройтись по каждой папке и выполнять команду для установки всех необходимых библиотек:

   ```bash
   pip install -r requirements.txt

5. Запуск скриптов:
   - **`neuron`** -
   - **`parser`** - необходимо запустить скрипт **`main.py`** и программа сама начнет парсить объявления с avito
   - **`tg_bot`** - необходимо создать бота в telegram у **`@BotFather`**, затем скопировать **`API`** бота. Далее создайте файл **`.env`** в той же директории, где расположен файл **`main.py`**. В нем мы создаем переменную **`TOKEN`** и указываем токен телеграм бота. Затам запускаем скрипт **`run.py`** и наслаждаемся работой бота
   - **`web_site`** - для запуска backend сайт на фреймфворке Flask необходимо запусиить скрипт **`app.py`**

---

## 🛠️ Технологии проекта

- **Язык программирования:** Python
- **Библиотеки и фреймворки:** Flask, Aiogram, Pandas, NumPy
- **Frontend:** HTML, CSS, JavaScript
- **API:** Telegram API

---

## 📈 Перспективы развития

- Расширение функционала модели для оценки стоимости недвижимости в других регионах.
- Добавление возможности предсказания цен на основе трендов рынка.
- Увеличение набора парсинга, включая другие платформы с объявлениями.
- Улучшение дизайна сайта и Telegram-бота для повышения удобства использования.

---

⭐ **Если вам понравился этот проект, не забудьте поставить звёздочку на GitHub и поделиться им с друзьями!**
