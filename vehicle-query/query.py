import typing as t

import pandas as pd
import requests
from fastapi import HTTPException

from .schemas import EVDataResponse

# TODO: consider a class per data source
# Pros - DRY functions for fetching and formatting data
# considerations - What if number of data sources balloons?

BASE_URL = "https://data.wa.gov/resource/f6w7-q2d2.json"


def fetch_ev_data(model_year: int) -> list[dict[str, t.Any]]:
    year_url = f"{BASE_URL}?model_year={model_year}"
    try:
        r = requests.get(year_url)
    except:
        raise HTTPException(
            status_code=500, detail="Failed to fetch data from data.wa.gov"
        )
    return r.json()


def format(ev_data: list[dict[str, t.Any]]) -> EVDataResponse:

    if len(ev_data) == 0:
        return []

    ev_df = pd.DataFrame(ev_data)
    ev_df["electric_range"] = pd.to_numeric(ev_df["electric_range"], errors="coerce")
    aggregated_data = (
        ev_df.groupby("make")
        .agg(total_vehicles=("make", "size"), average_range=("electric_range", "mean"))
        .reset_index()
    )
    # convert to list of EVDataResponse to ensure data integrity
    # NOTE: not sure if this is the most efficient way to do this.
    formatted_data = aggregated_data.apply(
        lambda row: EVDataResponse(
            make=row["make"],
            total_vehicles=row["total_vehicles"],
            average_range=row["average_range"],
        ),
        axis=1,
    ).tolist()

    return formatted_data
