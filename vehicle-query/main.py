from fastapi import FastAPI

from query import fetch_ev_data, format

app = FastAPI()

@app.get("vehicles/{model_year}")
async def get_vehicles(model_year: int):
    ev_data = fetch_ev_data(model_year)
    stats_by_make: dict[str, dict[str, int | float]] = format(ev_data)
    return stats_by_make