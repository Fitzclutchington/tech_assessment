from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates

from .schemas import EVDataResponse
from .query import fetch_ev_data, format

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/vehicles/{model_year}", status_code=200)
async def get_vehicles(request: Request, model_year: int):
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
