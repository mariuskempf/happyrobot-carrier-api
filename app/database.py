"""Database access utilities for loads."""

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent / "data" / "loads.db"


def _get_connection() -> sqlite3.Connection:
    """Get a connection to the loads database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_loads(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    equipment_type: Optional[str] = None,
    status: str = "available",
) -> list[dict]:
    """Fetch loads with optional filters.

    Args:
        origin: Optional filter for load origin (case-insensitive, partial match).
        destination: Optional filter for load destination (case-insensitive, partial match).
        equipment_type: Optional filter for required equipment type (case-insensitive, partial match).
        status: Filter loads by status (default: "available").

    Returns:
        A list of dictionaries representing the loads that match the filters.
    """
    conn = _get_connection()
    query = "SELECT * FROM loads WHERE status = ?"
    params: list = [status]

    if origin:
        query += " AND LOWER(origin) LIKE ?"
        params.append(f"%{origin.lower()}%")
    if destination:
        query += " AND LOWER(destination) LIKE ?"
        params.append(f"%{destination.lower()}%")
    if equipment_type:
        query += " AND LOWER(equipment_type) LIKE ?"
        params.append(f"%{equipment_type.lower()}%")

    rows = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return rows


def get_load_by_id(load_id: str) -> Optional[dict]:
    """Fetch a single load by ID.

    Args:
        load_id: The unique identifier of the load to retrieve.

    Returns:
        A dictionary representing the load if found, or None if not found.
    """
    conn = _get_connection()
    row = conn.execute("SELECT * FROM loads WHERE load_id = ?", (load_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# Note: not really used for this demo, but could be called by the agent when booking a load
# to update its status to "booked".
# Not sure here, as the agent is supposed to forward the call to a sales representative after
# agreement on the load. We could do this in the future though.


def update_load_status(load_id: str, status: str) -> bool:
    """Update the status of a load (e.g. available → booked).

    Args:
        load_id: The unique identifier of the load to update.
        status: The new status to set for the load.

    Returns:
        True if the load was found and updated, False otherwise.
    """
    conn = _get_connection()
    cursor = conn.execute("UPDATE loads SET status = ? WHERE load_id = ?", (status, load_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated
