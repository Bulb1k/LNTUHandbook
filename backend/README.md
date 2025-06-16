# Backend

Simple FastAPI backend providing an API and a Bootstrap-styled admin panel.

## Endpoints
- `GET /users` - list registered users.
- `POST /users` - register new user.
- `GET /admin` - admin panel. Requires login.
- `GET /login` and `POST /login` - admin authentication.

The application uses SQLite by default. Configure these environment variables:

```
DATABASE_URL=sqlite:///./users.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
SECRET_KEY=change_me
```
