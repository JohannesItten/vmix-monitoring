from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="vue")
app = FastAPI()
app.mount("/assets", StaticFiles(directory="vue/assets"), name="assets")
app.mount("/favicon", StaticFiles(directory="vue/favicon"), name="favicon")

# TODO read from config
_WS_SERVER = 'ws://localhost:9090'


@app.get('/')
async def serve_root(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {'request': request}
    )


@app.get('/defaults')
async def defaults():
    return {
        'server': _WS_SERVER
    }
