# Refacer — Face Swap Tool

Face swapping приложение на основе InsightFace и INSwapper, запущенное в Docker с Gradio интерфейсом.

## Возможности

- 🖼️ Face swap для фотографий
- 🎬 Face swap для видео
- 🐳 Docker контейнеризация
- 🎯 Web UI через Gradio

## Требования

- Docker & Docker Compose
- ~1GB дискового пространства для моделей

## Установка

```bash
git clone <repo-url>
cd refacer
docker compose build
docker compose up
```

Откройте браузер: `http://localhost:7860`

## Использование

### Для фото

1. Загрузите исходное лицо (источник)
2. Загрузите целевое изображение (куда вставить)
3. Нажмите "Swap Photo"

### Для видео

1. Загрузите фото источника
2. Загрузите видеофайл
3. Нажмите "Swap Video"

## Архитектура

- **refacer.py** — основной класс для работы с лицами и свопом
- **webui.py** — Gradio интерфейс
- **Dockerfile** — контейнеризация
- **docker-compose.yml** — конфигурация сервиса

## Модели

Используются модели из InsightFace:
- `buffalo_l` — детекция лиц
- `inswapper_128.onnx` — face swapping

## Ограничения

- Работает на CPU (медленнее, чем GPU)
- GTX 560 Ti не совместима с CUDA (CC 2.1 < 3.5)
- Требует хороших фото с четкими лицами

## Лицензия

MIT
