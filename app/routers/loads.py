"""Loads API router for searching and retrieving load information."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.database import get_all_loads, get_load_by_id
from app.schemas import Load

router = APIRouter()


@router.get("/search", response_model=list[Load])
def search_loads(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    equipment_type: Optional[str] = Query(None),
):
    """Search available loads. Called by the agent after carrier verification.

    Args:
        origin: Optional filter for load origin (case-insensitive, partial match).
        destination: Optional filter for load destination (case-insensitive, partial match).
        equipment_type: Optional filter for required equipment type (case-insensitive, partial match).

    Returns:
        List of loads matching the search criteria.
    """
    return get_all_loads(origin=origin, destination=destination, equipment_type=equipment_type)


@router.get("/find", response_model=Load)
def find_load(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    equipment_type: Optional[str] = Query(None),
):
    """Find a single load matching the search criteria.

    Args:
        origin: Optional filter for load origin (case-insensitive, partial match).
        destination: Optional filter for load destination (case-insensitive, partial match).
        equipment_type: Optional filter for required equipment type (case-insensitive, partial match).

    Returns:
        The first matching load as an object, or 404 if none found.
    """
    results = get_all_loads(origin=origin, destination=destination, equipment_type=equipment_type)
    if not results:
        raise HTTPException(status_code=404, detail="No matching load found")
    return results[0]


@router.get("/{load_id}", response_model=Load)
def get_load(load_id: str):
    """Get a single load by its ID

    Args:
        load_id: The unique identifier of the load to retrieve.

    Returns:
        The load details if found.
    """
    load = get_load_by_id(load_id)
    if not load:
        raise HTTPException(status_code=404, detail=f"Load {load_id} not found")
    return load
