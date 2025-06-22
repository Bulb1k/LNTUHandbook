# Backend

Simple FastAPI backend providing an API and a Bootstrap-styled admin panel.
The code is organized into routers under `app/routers` with shared dependencies in `app/dependencies.py`.


## Endpoints
- `GET /users` - list registered users.
- `GET /users/{chat_id}` - retrieve a single user by chat ID.
- `POST /users` - register new user. Fields: `chat_id`, optional `facultative`, `course`, `group`.
- `PUT /users/{chat_id}` - update an existing user's facultative, course or group.
- `GET /admin` - dashboard with statistics.
- `GET /admin/users` - list registered users with edit/delete actions.
- `GET /admin/users/{id}/edit` and `POST /admin/users/{id}/edit` - edit a user's details.
- `POST /admin/users/{id}/delete` - remove a user from the database.
- `GET /admin/push` and `POST /admin/push` - send push notifications to the Telegram bot. Messages can be targeted to specific chat IDs or filtered by facultative, course, or group. If no filters are provided the message goes to all users.
- `GET /login` and `POST /login` - admin authentication.
- `GET /logout` - clear the session.

The application uses SQLite by default. Configure these environment variables:

```
DATABASE_URL=sqlite:///./users.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
SECRET_KEY=change_me
BOT_API_URL=http://tgbot:8080/api
```
