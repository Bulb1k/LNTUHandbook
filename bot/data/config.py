from environs import Env
from pathlib import Path

env = Env()

env.read_env()

SERVER_ADDRESS: str = env.str("SERVER_ADDRESS")
SERVER_PORT: int = env.int("SERVER_PORT")
SERVER_HOST: str = env.str("SERVER_HOST")

BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN")
BOT_URL: str = env.str("TELEGRAM_BOT_LINK")

WEBHOOK_SECRET_TOKEN: str = env.str("TELEGRAM_WEBHOOK_SECRET_TOKEN")
WEBHOOK_PATH: str = env.str("TELEGRAM_WEBHOOK_PATH")

API_BACKEND_URL: str = env.str("API_BACKEND_URL")
API_BACKEND_KEY: str = env.str("API_BACKEND_KEY")

REDIS_HOST: str = env.str("REDIS_HOST")
REDIS_PORT: int = env.int("REDIS_PORT")
REDIS_PASSWORD: str = env.str("REDIS_PASSWORD", default=None)

BASE_DIR = Path(__file__).resolve().parent.parent

USE_NGROK: bool = env.bool("USE_NGROK", default=False)
NGROK_AUTH_TOKEN: str = env.str("NGROK_AUTH_TOKEN", default="")
NGROK_INTERFACE_HOST: str = env.str("NGROK_INTERFACE_HOST", default="ngrok")
NGROK_INTERFACE_PORT: int = env.int("NGROK_INTERFACE_PORT", default=4040)