from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .query import fetch_ev_data, format
from .schemas import EVDataResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, status_code=200)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit-year")
async def submit_year(model_year: int = Form(...)):

    return RedirectResponse(url=f"/vehicles?model_year={model_year}", status_code=303)


@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles(request: Request, model_year: int | None = None):
    # TODO: handle case where year is None, need some refactoring
    # consider future query args like model or make
    ev_data = fetch_ev_data(model_year)

    stats_by_make: list[EVDataResponse] = format(ev_data)
    return templates.TemplateResponse(
        "vehicles.html",
        {
            "request": request,
            "ev_data": stats_by_make,
            "model_year": model_year,
            "title": "Vehicles By Year",
        },
    )
