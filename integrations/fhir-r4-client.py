"""
AI Kill Switch Protocol — FHIR R4 Client
The Faulkner Group | Version 1.0.0 | 2026-04-06
Compliance: HL7 FHIR R4, ONC HTI-1 Final Rule, HIPAA 45 CFR 164.312

Provides authenticated FHIR R4 read access for agents and digital twins.
All requests are logged. PHI fields are masked in logs.
"""

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aksp.fhir_client")

PHI_MASK = "[MASKED-PHI]"
PHI_LOG_FIELDS = {"name", "birthDate", "ssn", "address", "telecom", "identifier"}

FHIR_BASE_URL = os.environ.get("EPIC_FHIR_BASE_URL", "")
TOKEN_ENDPOINT = os.environ.get("EPIC_TOKEN_ENDPOINT", "")
CLIENT_ID = os.environ.get("EPIC_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("EPIC_CLIENT_SECRET", "")
REQUEST_TIMEOUT_SEC = 5


def _get_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def _get_access_token() -> str:
    """Obtain OAuth 2.0 SMART on FHIR access token."""
    session = _get_session()
    response = session.post(
        TOKEN_ENDPOINT,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "patient/*.read",
        },
        timeout=REQUEST_TIMEOUT_SEC,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def _mask_phi(resource: dict) -> dict:
    """Remove PHI fields from a FHIR resource dict for safe logging."""
    return {k: (PHI_MASK if k in PHI_LOG_FIELDS else v) for k, v in resource.items()}


def _audit_log(event_type: str, details: dict) -> None:
    logger.info(
        json.dumps(
            {
                "audit_event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **details,
            }
        )
    )


def read_resource(resource_type: str, resource_id: str, requester_agent_id: str) -> dict[str, Any]:
    """
    Read a single FHIR R4 resource by type and ID.
    Logs request (PHI masked). Raises on non-200 responses.
    """
    token = _get_access_token()
    url = f"{FHIR_BASE_URL}/{resource_type}/{resource_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/fhir+json",
    }

    session = _get_session()
    response = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SEC)

    _audit_log(
        "FHIR_READ",
        {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "requester_agent_id": requester_agent_id,
            "http_status": response.status_code,
        },
    )

    response.raise_for_status()
    return response.json()


def search_resources(resource_type: str, params: dict, requester_agent_id: str) -> list[dict]:
    """
    Search FHIR R4 resources. Returns list of matching resource dicts.
    """
    token = _get_access_token()
    url = f"{FHIR_BASE_URL}/{resource_type}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/fhir+json",
    }

    session = _get_session()
    response = session.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT_SEC)

    _audit_log(
        "FHIR_SEARCH",
        {
            "resource_type": resource_type,
            "params": params,
            "requester_agent_id": requester_agent_id,
            "http_status": response.status_code,
        },
    )

    response.raise_for_status()
    bundle = response.json()
    entries = bundle.get("entry", [])
    return [e["resource"] for e in entries if "resource" in e]


def validate_sync(resource_type: str, resources: list[dict]) -> dict[str, Any]:
    """
    Validate a list of FHIR resources against sync rules.
    Returns dict with valid (bool), violations (list), and trigger_at003 (bool).
    """
    violations = []
    for resource in resources:
        if resource.get("resourceType") != resource_type:
            violations.append(f"Resource type mismatch: expected {resource_type}")
        if "id" not in resource:
            violations.append("Missing required field: id")
        if resource_type == "Observation" and "valueQuantity" not in resource and "valueString" not in resource:
            violations.append(f"Observation {resource.get('id')} missing value field")

    valid = len(violations) == 0
    _audit_log(
        "FHIR_SYNC_VALIDATION",
        {
            "resource_type": resource_type,
            "resource_count": len(resources),
            "valid": valid,
            "violations": violations,
            "trigger_at003": not valid,
        },
    )
    return {"valid": valid, "violations": violations, "trigger_at003": not valid}
