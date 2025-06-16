# Backend

Simple FastAPI backend providing an API and a Bootstrap-styled admin panel.

## Endpoints
- `GET /users` - list registered users.
- `POST /users` - register new user. Fields: `telegram_id`, optional `username`, `full_name`, `facultative`, `course`, `group`.
- `GET /admin` - dashboard with statistics.
- `GET /admin/users` - list registered users.
- `GET /admin/push` and `POST /admin/push` - send push notifications to the Telegram bot.
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
