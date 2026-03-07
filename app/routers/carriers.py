"""Carrier-related API endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from app.clients.fmcsa import CarrierInfo, EligibilityStatus, FMCSAClient
from app.core.config import Settings, get_settings

router = APIRouter()


def _raise_for_eligibility(carrier: CarrierInfo) -> None:
    """Raise appropriate HTTP exception based on carrier eligibility status.

    Args:
        carrier: The carrier info to check.

    Raises:
        HTTPException: 404 if carrier not found.
        HTTPException: 503 if FMCSA API error.
        HTTPException: 403 if carrier is ineligible.
        HTTPException: 500 if FMCSA is misconfigured.
    """
    if carrier.eligibility == EligibilityStatus.NOT_FOUND:
        raise HTTPException(status_code=404, detail=carrier.ineligibility_reason)

    if carrier.eligibility == EligibilityStatus.API_ERROR:
        raise HTTPException(status_code=503, detail=carrier.ineligibility_reason)

    if carrier.eligibility == EligibilityStatus.INELIGIBLE:
        raise HTTPException(status_code=403, detail=carrier.ineligibility_reason)


@router.get("/verify/mc/{mc_number}", response_model=CarrierInfo)
async def verify_carrier_by_mc(
    mc_number: int,
    settings: Settings = Depends(get_settings),
) -> CarrierInfo:
    """Verify carrier eligibility by MC number.

    Args:
        mc_number: The MC number of the carrier to verify.

    Raises:
        HTTPException: 404 if carrier not found.
        HTTPException: 403 if carrier is ineligible.
        HTTPException: 503 if FMCSA API is unavailable.

    Returns:
        CarrierInfo: Structured carrier information including eligibility status.
    """
    async with FMCSAClient(settings=settings.fmcsa) as client:
        carrier = await client.lookup_by_mc_number(mc_number)

    _raise_for_eligibility(carrier)
    return carrier


@router.get("/verify/dot/{dot_number}", response_model=CarrierInfo)
async def verify_carrier_by_dot(
    dot_number: int,
    settings: Settings = Depends(get_settings),
) -> CarrierInfo:
    """Verify carrier eligibility by USDOT number.

    Carriers registered after October 2025 no longer receive MC numbers
    and must be verified by USDOT number instead.

    Args:
        dot_number: The USDOT number of the carrier to verify.

    Raises:
        HTTPException: 404 if carrier not found.
        HTTPException: 403 if carrier is ineligible.
        HTTPException: 503 if FMCSA API is unavailable.

    Returns:
        CarrierInfo: Structured carrier information including eligibility status.
    """
    async with FMCSAClient(settings=settings.fmcsa) as client:
        carrier = await client.lookup_by_dot_number(dot_number)

    _raise_for_eligibility(carrier)
    return carrier


# Note: Lookup via name is disabled for now

# @router.get("/search/{name}", response_model=list[CarrierInfo])
# async def search_carriers_by_name(
#     name: str,
#     settings: Settings = Depends(get_settings),
# ) -> list[CarrierInfo]:
#     """Search for carriers by name.

#     Note:
#         May return multiple results — the caller should confirm which carrier
#         is correct before proceeding with any booking actions.

#     Args:
#         name (str): The carrier name to search for.

#     Raises:
#         HTTPException: 404 if no carriers found matching the name.
#         HTTPException: 503 if FMCSA API is unavailable.

#     Returns:
#         list[CarrierInfo]: List of matching carriers with eligibility status.
#     """
#     async with FMCSAClient(settings=settings.fmcsa) as client:
#         carriers = await client.lookup_by_name(name)

#     if not carriers:
#         raise HTTPException(
#             status_code=404,
#             detail=f"No carriers found matching '{name}'",
#         )

#     return carriers
