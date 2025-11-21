# MyFirstWeb - Django REST API

Проект представляет собой REST API для управления пользователями, группами, постами, комментариями и лайками.

## 🚀 Возможности

- **Пользователи**: CRUD операции для управления пользователями
- **Группы**: Создание групп, добавление/удаление пользователей
- **Посты**: Публикация постов с привязкой к группам
- **Комментарии**: Система комментариев к постам
- **Лайки**: Возможность лайкать посты
- **Документация**: Автоматическая генерация Swagger/ReDoc документации

## 🛠 Технологии

- **Backend**: Django 5.2, Django REST Framework
- **Документация**: drf-spectacular
- **База данных**: SQLite3
- **Аутентификация**: Пока не реализована

## 📦 Установка и запуск

1. **Клонируй репозиторий**:
```bash
git clone https://github.com/horinim/UhabMessenger/tree/Dev
cd myfirstweb
```

2. **Создай виртуальное окружение**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. **Установи зависимости**:
```bash
pip install -r requirements.txt
```

4. **Примени миграции**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Запусти сервер**:
```bash
python manage.py runserver
```

## 📚 API Endpoints

### Пользователи (`/api/users/`)
- `GET /api/users/` - список всех пользователей
- `POST /api/users/` - создать пользователя
- `GET /api/users/{id}/` - получить пользователя по ID
- `PUT /api/users/{id}/` - обновить пользователя
- `DELETE /api/users/{id}/` - удалить пользователя

### Группы (`/api/groups/`)
- `GET /api/groups/` - список всех групп
- `POST /api/groups/` - создать группу
- `GET /api/groups/{id}/` - получить группу по ID
- `PUT /api/groups/{id}/` - обновить группу
- `DELETE /api/groups/{id}/` - удалить группу
- `POST /api/groups/{id}/members/` - добавить пользователя в группу
- `DELETE /api/groups/{id}/members/{user_id}/` - удалить пользователя из группы

### Посты (`/api/posts/`)
- `GET /api/posts/` - список всех постов
- `POST /api/posts/` - создать пост
- `GET /api/posts/{id}/` - получить пост по ID (с лайками и комментариями)
- `PUT /api/posts/{id}/` - обновить пост
- `DELETE /api/posts/{id}/` - удалить пост

### Комментарии (`/api/comments/`)
- `GET /api/comments/posts/{post_id}/` - комментарии к посту
- `POST /api/comments/posts/{post_id}/` - создать комментарий к посту
- `PUT /api/comments/{id}/` - обновить комментарий
- `DELETE /api/comments/{id}/` - удалить комментарий

### Лайки (`/api/likes/`)
- `POST /api/likes/posts/{post_id}/like/` - поставить лайк посту
- `DELETE /api/likes/posts/{post_id}/like/` - убрать лайк с поста
- `GET /api/likes/posts/{post_id}/likes/count/` - количество лайков поста
- `DELETE /api/likes/{id}/` - удалить лайк по ID

## 📖 Документация API

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Схема OpenAPI**: http://localhost:8000/api/schema/

## 🗃 Модели данных

### UsersList
- `id` - AutoField (primary key)
- `username` - CharField (имя пользователя)
- `email` - EmailField
- `created_at` - DateTimeField (автоматически)

### GroupUser
- `id` - AutoField (primary key) 
- `name` - CharField (название группы)
- `description` - TextField
- `users_list` - ManyToManyField к UsersList
- `created_at` - DateTimeField

### Post
- `id` - AutoField (primary key)
- `author_id` - ForeignKey к UsersList
- `group_id` - ForeignKey к GroupUser (опционально)
- `content` - TextField
- `created_at` - DateTimeField
- `likes_count` - вычисляемое свойство

### CommentPost
- `id` - AutoField (primary key)
- `post_id` - ForeignKey к Post
- `author_id` - ForeignKey к UsersList
- `text` - TextField
- `created_at` - DateTimeField

### LikePost
- `id` - AutoField (primary key)
- `post_id` - ForeignKey к Post
- `author_id` - ForeignKey к UsersList


## 👨‍💻 Разработчик

Horinim - [\[ссылка на GitHub\]](https://github.com/horinim)

---