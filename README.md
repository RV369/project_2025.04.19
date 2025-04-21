# project_2025.04.19

Для развертывания необходимо:

- Скопировать файл docker-compose.production.yml
- Создать файл .env с токеном BOT_TOKEN=TOKEN
- Запустить Docker
- команда для запуска скачивания образа и сборки контейнера:
```sh
docker compose -f docker-compose.production.yml up
```
- файл можно загрузить при помощи кнопки /start или перетащить в окно чата
