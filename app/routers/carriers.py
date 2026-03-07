"""Carrier-related API endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from app.clients.fmcsa import EligibilityStatus, FMCSAClient
from app.core.config import Settings, get_settings

router = APIRouter()


@router.get("/verify/{mc_number}")
async def verify_carrier(mc_number: str, settings: Settings = Depends(get_settings)):
    """Verify carrier eligibility based on FMCSA data.

    Args:
        mc_number (str): The MC number of the carrier to verify.

    Raises:
        HTTPException: Carrier not found (404)
        HTTPException: Carrier ineligible (403)
        HTTPException: FMCSA API error (503)

    Returns:
        carrier (CarrierInfo): Structured carrier information including eligibility status.
    """
    async with FMCSAClient(settings=settings.fmcsa) as client:
        carrier = await client.lookup_by_mc_number(mc_number)

    if carrier.eligibility == EligibilityStatus.NOT_FOUND:
        raise HTTPException(status_code=404, detail=carrier.ineligibility_reason)

    if carrier.eligibility == EligibilityStatus.API_ERROR:
        raise HTTPException(status_code=503, detail=carrier.ineligibility_reason)

    if carrier.eligibility == EligibilityStatus.INELIGIBLE:
        raise HTTPException(status_code=403, detail=carrier.ineligibility_reason)

    return carrier
