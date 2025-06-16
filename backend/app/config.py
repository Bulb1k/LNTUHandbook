from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str("DATABASE_URL", "sqlite:///./users.db")
ADMIN_USERNAME = env.str("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = env.str("ADMIN_PASSWORD", "password")
SECRET_KEY = env.str("SECRET_KEY", "secret")
