from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

router = APIRouter()

TEMPLATES_DIR = Path(__file__).parent.parent / "template"

@router.get("/", response_class=HTMLResponse)
async def serve_portfolio():
    html_file = TEMPLATES_DIR / "portfolio.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return HTMLResponse(content="<h1>404: Page not found</h1>", status_code=404)

@router.post("/submit-data")
async def submit_data(data: dict):
    return {"status": "success", "received_data": data}
