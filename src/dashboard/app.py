import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.config import config
from src.utils.logger import logger

app = FastAPI()

# Setup templates directory relative to this file
templates = Jinja2Templates(directory="src/dashboard/templates")

@app.get("/", response_class=HTMLResponse)
async def read_config(request: Request):
    # Filter sensitive keys for the UI if desired, but here we show all for editing
    return templates.TemplateResponse("index.html", {
        "request": request,
        "config_items": config._config
    })

@app.post("/", response_class=HTMLResponse)
async def update_config(request: Request):
    form_data = await request.form()
    for key, value in form_data.items():
        config.set_val(key, value)
    
    config.save_config()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "config_items": config._config,
        "message": "Configuration updated and persisted successfully!"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
