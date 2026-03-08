"""Pydantic Schemas to define the structure of data used in API requests and responses."""

from typing import Optional

from pydantic import BaseModel


class Load(BaseModel):
    """Schema representing a freight load listing."""

    load_id: str
    origin: str
    destination: str
    pickup_datetime: str
    delivery_datetime: str
    equipment_type: str
    loadboard_rate: float
    notes: Optional[str] = None
    weight: float
    commodity_type: str
    num_of_pieces: int
    miles: float
    dimensions: str
    status: str
