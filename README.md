# Trecker

## Описание
Trecker — это проект для отслеживания задач и проектов. Он включает в себя бэкенд на Django и фронтенд на React.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/JeniaSuperpuper/TSManager.git
   cd Trecker
   ```
2. Установите зависимости для бэкенда:
    ```bash
    cd Task/task
    pip install -r requirements.txt
    ```
3. Установите зависимости для фронтенда:
   ```bash
    cd ../../frontend
    npm install
    ```
4. Запустите Docker Compose:
   ```bash
    docker-compose up --build
    ```