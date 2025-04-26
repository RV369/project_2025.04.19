# project_2025.04.19

Для развертывания необходимо:

- Скопировать файл docker-compose.production.yml
- Создать файл .env с токеном BOT_TOKEN=TOKEN
- Запустить Docker
- команда для запуска скачивания образа и сборки контейнера:
```sh
docker compose -f docker-compose.production.yml up
```
- Либо склонировать репозиторий себе на компьютер и локально собрать и запустить образ командой:
```sh
docker compose up --build
```
- файл можно загрузить при помощи кнопки 'Загрузить файл' или скрепкой выбрать файл ExampleExcel.xlsx
