import requests
import typing as t

BASE_URL = "https://data.wa.gov/resource/f6w7-q2d2.json"


def fetch_ev_data(model_year: int) -> dict[str, t.Any]:
    year_url = f"{BASE_URL}?model_year={model_year}"
    r = requests.get(year_url)
    return r.json()

def format(ev_data: dict[str, t.Any]) -> dict[str, dict[str, int | float]]:
    pass