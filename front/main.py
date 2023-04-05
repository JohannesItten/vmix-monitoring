from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
import hashlib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# vmix-id list updating. TODO: remove this shit before deployment
vmixes = {}
with open("../vmixes.json", "r", encoding="utf-8") as file:
    config = json.load(file)

for param in config['vmixes']:
    id = hashlib.md5((param["name"] + param["ip"]).encode("utf-8")).hexdigest()
    vmixes[id] = param["name"]
#

@app.get("/vmix-grid", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("vmix-grid-9.html", {"request": request, "vmixes": vmixes})


@app.get("/nrf/", response_class=HTMLResponse)
async def get_paged_grid(request: Request, page: int = 1):
    page_amount = 6
    page_vmixes_max = min([len(vmixes), page_amount * page])
    
    page_vmixes = {}
    items = list(vmixes.items())
    for i in range(page * page_amount - page_amount, page_vmixes_max):
        item = items[i]
        page_vmixes[item[0]] = item[1]


    return templates.TemplateResponse("vmix-grid.html", {"request": request, "page": page, "vmixes": page_vmixes})


