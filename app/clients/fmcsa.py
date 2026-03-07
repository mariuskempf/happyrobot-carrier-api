"""FMCSA API client for carrier eligibility checks.

This module defines a simple client for interacting with the FMCSA API to check
carrier eligibility based on MC number, USDOT number, or carrier name.
"""

from enum import Enum

import httpx
from loguru import logger
from pydantic import BaseModel

from app.core.config import FMCSASettings


class EligibilityStatus(str, Enum):
    """Carrier eligibility status based on FMCSA data."""

    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    NOT_FOUND = "not_found"
    API_ERROR = "api_error"


class LookupMethod(str, Enum):
    """Method used to look up the carrier."""

    MC_NUMBER = "mc_number"
    DOT_NUMBER = "dot_number"
    NAME = "name"


class CarrierInfo(BaseModel):
    """Structured carrier information with eligibility status."""

    allowed_to_operate: bool
    eligibility: EligibilityStatus
    lookup_method: LookupMethod
    mc_number: int | None = None
    dot_number: int | None = None
    legal_name: str | None = None
    dba_name: str | None = None
    status_code: str | None = None
    common_authority_status: str | None = None
    ineligibility_reason: str | None = None


class FMCSAConfigurationError(Exception):
    """Raised when the FMCSA API key is invalid or not configured correctly."""


class FMCSAClient:
    """Asynchronous client for FMCSA API interactions."""

    def __init__(self, settings: FMCSASettings):
        self.client = httpx.AsyncClient(
            base_url=settings.base_url,
            params={"webKey": settings.api_key.get_secret_value()},
            timeout=settings.timeout,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.aclose()

    @staticmethod
    def _parse_eligibility(carrier: dict) -> tuple[EligibilityStatus, str | None]:
        """Evaluate carrier eligibility from FMCSA response fields."""
        if carrier.get("allowedToOperate") != "Y":
            return EligibilityStatus.INELIGIBLE, "Carrier is not allowed to operate"

        if carrier.get("statusCode") != "A":
            return EligibilityStatus.INELIGIBLE, "Carrier status is labelled as inactive"

        if carrier.get("commonAuthorityStatus") != "A":
            return EligibilityStatus.INELIGIBLE, "Carrier does not have active common authority"

        return EligibilityStatus.ELIGIBLE, None

    @staticmethod
    def _parse_carrier(carrier: dict, lookup_method: LookupMethod) -> CarrierInfo:
        """Parse raw FMCSA carrier dict into a CarrierInfo model."""
        eligibility, reason = FMCSAClient._parse_eligibility(carrier)

        return CarrierInfo(
            mc_number=int(carrier["mcNumber"]) if carrier.get("mcNumber") else None,
            dot_number=carrier.get("dotNumber"),
            legal_name=carrier.get("legalName"),
            dba_name=carrier.get("dbaName"),
            allowed_to_operate=carrier.get("allowedToOperate") == "Y",
            status_code=carrier.get("statusCode"),
            common_authority_status=carrier.get("commonAuthorityStatus"),
            eligibility=eligibility,
            ineligibility_reason=reason,
            lookup_method=lookup_method,
        )

    async def lookup_by_mc_number(self, mc_number: int) -> CarrierInfo:
        """Look up a carrier by MC number.

        Args:
            mc_number (int): The MC number to look up.

        Returns:
            CarrierInfo: Structured carrier information including eligibility status.
        """
        logger.debug("Looking up carrier by MC number: {}", mc_number)
        try:
            response = await self.client.get(f"/docket-number/{mc_number}")

            if response.status_code == 404:
                logger.info("MC number {} not found in FMCSA database", mc_number)
                return CarrierInfo(
                    mc_number=mc_number,
                    allowed_to_operate=False,
                    eligibility=EligibilityStatus.NOT_FOUND,
                    ineligibility_reason=f"MC number {mc_number} not found in FMCSA database",
                    lookup_method=LookupMethod.MC_NUMBER,
                )

            response.raise_for_status()
            content = response.json()["content"]

            if not content:
                logger.warning("FMCSA API returned empty results for MC number {}", mc_number)
                return CarrierInfo(
                    mc_number=mc_number,
                    allowed_to_operate=False,
                    eligibility=EligibilityStatus.NOT_FOUND,
                    ineligibility_reason=f"MC number {mc_number} not found in FMCSA database",
                    lookup_method=LookupMethod.MC_NUMBER,
                )

            carrier = content[0]["carrier"]
            result = self._parse_carrier(carrier, LookupMethod.MC_NUMBER)
            logger.debug("MC number {} lookup result: eligibility={}", mc_number, result.eligibility)
            return result

        except httpx.TimeoutException:
            logger.warning("FMCSA API timed out for MC number {}", mc_number)
            return CarrierInfo(
                mc_number=mc_number,
                allowed_to_operate=False,
                eligibility=EligibilityStatus.API_ERROR,
                ineligibility_reason="FMCSA API timed out — please try again",
                lookup_method=LookupMethod.MC_NUMBER,
            )
        except httpx.HTTPError as e:
            logger.error("FMCSA API error for MC number {}: {}", mc_number, e)
            return CarrierInfo(
                mc_number=mc_number,
                allowed_to_operate=False,
                eligibility=EligibilityStatus.API_ERROR,
                ineligibility_reason="FMCSA API unavailable — please try again later",
                lookup_method=LookupMethod.MC_NUMBER,
            )

    async def lookup_by_dot_number(self, dot_number: int) -> CarrierInfo:
        """Look up a carrier by USDOT number.

        Carriers registered after October 2025 no longer receive MC numbers
        and must be looked up by their USDOT number instead.

        Args:
            dot_number (int): The USDOT number to look up.

        Returns:
            CarrierInfo: Structured carrier information including eligibility status.
        """
        logger.debug("Looking up carrier by USDOT number: {}", dot_number)
        try:
            response = await self.client.get(f"/{dot_number}")

            if response.status_code == 404:
                logger.info("USDOT number {} not found in FMCSA database", dot_number)
                return CarrierInfo(
                    dot_number=dot_number,
                    allowed_to_operate=False,
                    eligibility=EligibilityStatus.NOT_FOUND,
                    ineligibility_reason=f"USDOT number {dot_number} not found in FMCSA database",
                    lookup_method=LookupMethod.DOT_NUMBER,
                )

            response.raise_for_status()
            content = response.json().get("content", {})
            carrier = content.get("carrier", {})

            if not carrier:
                logger.warning("FMCSA API returned empty results for USDOT number {}", dot_number)
                return CarrierInfo(
                    dot_number=int(dot_number),
                    allowed_to_operate=False,
                    eligibility=EligibilityStatus.NOT_FOUND,
                    ineligibility_reason=f"USDOT number {dot_number} not found in FMCSA database",
                    lookup_method=LookupMethod.DOT_NUMBER,
                )

            result = self._parse_carrier(carrier, LookupMethod.DOT_NUMBER)
            logger.debug("USDOT number {} lookup result: eligibility={}", dot_number, result.eligibility)
            return result

        except httpx.TimeoutException:
            logger.warning("FMCSA API timed out for USDOT number {}", dot_number)
            return CarrierInfo(
                dot_number=int(dot_number),
                allowed_to_operate=False,
                eligibility=EligibilityStatus.API_ERROR,
                ineligibility_reason="FMCSA API timed out — please try again",
                lookup_method=LookupMethod.DOT_NUMBER,
            )
        except httpx.HTTPError as e:
            logger.error("FMCSA API error for USDOT number {}: {}", dot_number, e)
            return CarrierInfo(
                dot_number=int(dot_number),
                allowed_to_operate=False,
                eligibility=EligibilityStatus.API_ERROR,
                ineligibility_reason="FMCSA API unavailable — please try again later",
                lookup_method=LookupMethod.DOT_NUMBER,
            )

    async def lookup_by_name(self, name: str) -> list[CarrierInfo]:
        """Look up carriers by name.

        Note:
            This method may return multiple carriers if the name is not unique.
            The caller should confirm which carrier is correct before proceeding
            with any actions.

        Args:
            name (str): The carrier name to search for.

        Returns:
            list[CarrierInfo]: A list of matching carriers with eligibility status.
        """
        logger.debug("Looking up carriers by name: {}", name)
        try:
            response = await self.client.get(f"/name/{name}")

            if response.status_code == 404:
                logger.info("No carriers found for name '{}'", name)
                return []

            response.raise_for_status()
            carriers = response.json()["content"]["listCarrierBasics"]
            logger.debug("Name lookup '{}' returned {} carrier(s)", name, len(carriers))
            return [FMCSAClient._parse_carrier(c["carrier"], LookupMethod.NAME) for c in carriers]

        except httpx.TimeoutException:
            logger.warning("FMCSA API timed out for name lookup '{}'", name)
            return []
        except httpx.HTTPError as e:
            logger.error("FMCSA API error for name lookup '{}': {}", name, e)
            return []
