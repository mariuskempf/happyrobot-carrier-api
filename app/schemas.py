"""Pydantic Schemas to define the structure of data used in API requests and responses."""

from typing import Optional

from pydantic import BaseModel


class Load(BaseModel):
    """Schema representing a freight load listing.

    Attributes:
        load_id: Unique identifier for the load.
        origin: Starting location of the load.
        destination: Ending location of the load.
        pickup_datetime: Scheduled pickup date and time.
        delivery_datetime: Scheduled delivery date and time.
        equipment_type: Type of equipment required for the load.
        loadboard_rate: Broker's opening rate offered to the carrier.
        ceiling_rate: Maximum rate the broker will accept (110% of loadboard_rate).
        notes: Optional additional information about the load.
        weight: Total weight of the load in pounds.
        commodity_type: Type of commodity being transported.
        num_of_pieces: Number of pieces or items in the load.
        miles: Total distance of the load in miles.
        dimensions: Dimensions of the load (e.g., "LxWxH" format).
        status: Current status of the load (e.g., "available", "booked", "in transit", "delivered").
    """

    load_id: str
    origin: str
    destination: str
    pickup_datetime: str
    delivery_datetime: str
    equipment_type: str
    loadboard_rate: float
    ceiling_rate: float
    notes: Optional[str] = None
    weight: float
    commodity_type: str
    num_of_pieces: int
    miles: float
    dimensions: str
    status: str
