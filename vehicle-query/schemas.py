from pydantic import BaseModel


class EVDataResponse(BaseModel):
    make: str
    total_vehicles: int
    average_range: float
