from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .query import fetch_ev_data, format

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class EVDataResponse(BaseModel):
    make: str
    total_vehicles: int
    average_range: float


@app.get("/vehicles/{model_year}", status_code=200)
async def get_vehicles(request: Request, model_year: int):
    ev_data = fetch_ev_data(model_year)

    if len(ev_data) == 0:
        raise HTTPException(
            status_code=404, detail=f"No data found for model year {model_year}"
        )

    stats_by_make: list[EVDataResponse] = format(ev_data)
    return templates.TemplateResponse(
        "vehicles.html",
        {"request": request, "ev_data": stats_by_make, "model_year": model_year, "title": "Vehicles By Year"},
    )
