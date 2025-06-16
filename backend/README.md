# Backend

Simple FastAPI backend providing an API and a Bootstrap-styled admin panel.

## Endpoints
- `GET /users` - list registered users.
- `POST /users` - register new user. Fields: `chat_id`, optional `facultative`, `course`, `group`.
- `GET /admin` - dashboard with statistics.
- `GET /admin/users` - list registered users.
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
