Бек-енд топоніміки. 
Тримає в SQLite-базі даних інформацію про українські населені пункти, надає ендпойнт `/api/settlements` для пошуку по назві НП за регулярним виразом. 

#### Головна гілка:
`master`

#### Локальний запуск:
1. (опціонально) встановити virtualenv/virtualenvwrapper і створити venv; активувати venv
2. `pip install -r requirements/dev.txt`
3. `export FLASK_ENV=development && python ./dev_starter.py`
4. Додаток доступний на http://localhost:5000

#### Поточний деплоймент:
- Додаток на http://134.122.66.78/ запущений на digitalocean-дроплеті через nginx + gunicorn. Зроблено по цьому [туторіалу](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04). 
- Прод версія: https://ridni.in.ua/toponimika

#### Головний клас який створює аплікейшн:
`app/__init__.py`

#### Дані:
- Дані взяті з https://github.com/Medniy2000/ua_locations. 
- Міграції зроблені на Flask-Migrate/alembic, запускаються автоматично при створенні аплікейшену в `app/__init__.py`, можна також запустити вручну через `flask db upgrade`.
- Після завершення міграцій, в папці `app` буде лежати база `settlements.db`, до якої й будуть робитись запити.
- В першій міграції створюємо схему бази, в другій - беремо незмінений json-файл з ua_locations (`ua_locations_10_11_2021.json`), завантажуємо в базу (при імпорті чистячи дані) в наступних двох - додаємо деякі дані.
- Станом на сьогодні не всі НП в базі мають проставлені координати. Це поправимо дещо пізніше, заповнивши координати в файлах що лежать в `resources/ua_locations_db/manual_coordinates`.

#### Веб-контролери:
- лежать в `app/blueprints`
- `api_bp.py` - містить API для пошуку
- `rendering_bp.py` - url який рендерить html-сторінку
- `static_files_bp.py` - шляхи для js/css-файлів.

#### Огляд бібліотек для роботи з файлами (щоб не загубити):
https://flatlogic.com/blog/top-mapping-and-maps-api/
