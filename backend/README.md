# Backend

Simple FastAPI backend providing an API and a basic admin panel.

## Endpoints
- `GET /users` - list registered users.
- `POST /users` - register new user.
- `GET /admin?secret=ADMIN_SECRET` - view admin panel with user list.

The application uses SQLite by default. Configure `DATABASE_URL` and `ADMIN_SECRET` using environment variables.
