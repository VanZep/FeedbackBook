# Проект YaMDb

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Технологии
Python 3.9.13, Django 3.2, djangorestframework 3.12.4

### Запуск проекта в dev-режиме
- **Склонируйте проект к себе на компьютер:**
+ *Для этого из нужной директории в командной строке выполните команду*
```
git clone git@github.com:VanZep/YaMDb.git
```
- **Перейдите в каталог проекта:**
```
cd Yatube
```
- **Создайте виртуальное окружение:**
+ *для Windows*
```
python -m venv venv
```
+ *для macOS*
```
python3 -m venv venv
```
- **Активируйте виртуальное окружение:**
+ *для Windows*
```
source venv/Scripts/activate
```
+ *для macOS*
```
source venv/bin/activate
```
- **Установите зависимости из файла requirements.txt:**
```
pip install -r requirements.txt
```
- **Выполните миграции:**
+ *для этого перейдите в каталог с файлом manage.py*
```
cd api_yamdb
```
+ *затем выполните команду*
```
python manage.py migrate
```
- **Загрузите данные в БД с помощью команды:**
```
python manage.py load_csv
```
- **Далее запустите dev-сервер, выполнив команду:**
```
python manage.py runserver
```
- **Проект будет доступен по адресу - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### Примеры. Некоторые примеры запросов к API.
- **Спецификация API с примерами о том, как должен работать проект доступна по адресу - [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)**
- **Вы также можете восользоваться готовой коллекцией запросов. В файле README.md, который лежит в каталоге postman_collection есть описание того, как это сделать.**

### Авторы:
***MaryPak, AlekseySazonov, VanZep***