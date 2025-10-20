cat > README.md << 'EOF'
# Store Inventory API

FastAPI приложение для учета продуктов в магазине.

## Стек технологий
- **FastAPI** - асинхронный веб-фреймворк
- **PostgreSQL** - база данных
- **Docker** - контейнеризация
- **Pytest** - тестирование
- **Asyncpg** - работа с БД

## Запуск проекта

```bash
# Клонировать репозиторий
git clone https://github.com/TimurSharipov02/fastapi-store-inventory.git

# Запустить все сервисы
docker-compose up --build

