# Курсовая работа

Создать виртуальное окружение
```
python -m venv venv
```
Активировать виртуальное окружение
```
venv\Scripts\activate.bat
```
Установить зависимости
```
pip install -r requirements.txt
```
Активировать постгис
```
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```
Запустить приложение
1. Сначала необходимо перейти в папку app
```
cd app
```
2. А затем ввести следующую команду
```
uvicorn main:app --reload
```

Для удобства проверять можно на странице <code> http://127.0.0.1:8000/docs/ </code>