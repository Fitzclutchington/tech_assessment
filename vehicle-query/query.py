import typing as t

import pandas as pd
import requests

BASE_URL = "https://data.wa.gov/resource/f6w7-q2d2.json"


def fetch_ev_data(model_year: int) -> list[dict[str, t.Any]]:
    year_url = f"{BASE_URL}?model_year={model_year}"
    r = requests.get(year_url)
    return r.json()


def format(ev_data: list[dict[str, t.Any]]) -> list[dict[str, int | float | str]]:
    ev_df = pd.DataFrame(ev_data)
    ev_df["electric_range"] = pd.to_numeric(ev_df["electric_range"], errors="coerce")
    aggregated_data = (
        ev_df.groupby("make")
        .agg(total_vehicles=("make", "size"), average_range=("electric_range", "mean"))
        .reset_index()
    )
    return aggregated_data.to_dict(orient="records")
