# MVP

### Core Backend:
1. Установить Python + фреймворки:
   - uv
   - FastAPI
   - uvicorn
   - Jinja2
   - SQLAlchemy

3. Создать модели:
   - Product (name, price, stock)
   - User (login, password)
   - Order (user_id, product_id, date)

4. Интеграция с БД:
   - Подготовить PostgreSQL внутри docker-контейнера
   - Использовать SQLAlchemy для создания таблиц

### Basic Frontend:
1. Использовать Jinja2 для создания основных страниц:
   - Главная
   - Авторизация
   - Заказ
