import uvicorn

from data.config import (
    SERVER_PORT,
    SERVER_HOST,
)
from server import app as server


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=True,
        log_level="info",
    )
