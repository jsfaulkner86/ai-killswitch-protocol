"""
AI Kill Switch Protocol — Alert Dispatcher
The Faulkner Group | Version 1.0.0 | 2026-04-06
Compliance: HIPAA 45 CFR 164.312(b), FDA 21 CFR Part 11

Routes kill switch halt events to the appropriate notification channels
(PagerDuty, SMS, Email, SIEM/Syslog) based on escalation tier.
All dispatches are audit logged.
"""

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from enum import IntEnum
from typing import Any

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aksp.alert_dispatcher")

# ---------------------------------------------------------------------------
# Config — from environment
# ---------------------------------------------------------------------------
PAGERDUTY_ROUTING_KEY = os.environ.get("PAGERDUTY_ROUTING_KEY", "")
SIEM_SYSLOG_ENDPOINT = os.environ.get("SIEM_SYSLOG_ENDPOINT", "")
EMAIL_API_ENDPOINT = os.environ.get("EMAIL_API_ENDPOINT", "")
SMS_API_ENDPOINT = os.environ.get("SMS_API_ENDPOINT", "")

CMIO_EMAIL = os.environ.get("CMIO_EMAIL", "")
CMIO_PHONE = os.environ.get("CMIO_PHONE", "")
CIO_EMAIL = os.environ.get("CIO_EMAIL", "")
CIO_PHONE = os.environ.get("CIO_PHONE", "")
LEGAL_EMAIL = os.environ.get("LEGAL_EMAIL", "")
EHR_LIAISON_EMAIL = os.environ.get("EHR_LIAISON_EMAIL", "")


class Tier(IntEnum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
def dispatch_halt_alert(
    tier: int,
    agent_or_twin_id: str,
    trigger_id: str,
    halt_reason: str,
    audit_event_id: str | None = None,
) -> dict[str, Any]:
    """
    Dispatch halt alerts per notification requirements in killswitch-policy.yaml.
    Returns dict of dispatch results by channel.
    """
    if audit_event_id is None:
        audit_event_id = str(uuid.uuid4())

    event_ts = datetime.now(timezone.utc).isoformat()
    results: dict[str, Any] = {}

    # Tier 0, 1, 2, 3 — always notify on-call clinician via PagerDuty
    results["pagerduty"] = _send_pagerduty(
        summary=f"[AKSP Tier {tier}] Kill Switch: {agent_or_twin_id}",
        details={
            "trigger_id": trigger_id,
            "reason": halt_reason,
            "audit_event_id": audit_event_id,
        },
        severity="critical" if tier >= 2 else "warning",
    )

    # Tier 0+ — SIEM syslog within 30 seconds
    results["siem"] = _send_siem(
        {
            "event_type": "KILL_SWITCH_HALT",
            "tier": tier,
            "agent_or_twin_id": agent_or_twin_id,
            "trigger_id": trigger_id,
            "halt_reason": halt_reason,
            "audit_event_id": audit_event_id,
            "timestamp": event_ts,
        }
    )

    # Tier 0+ — CMIO SMS + email within 5 minutes
    results["cmio_sms"] = _send_sms(CMIO_PHONE, f"[AKSP T{tier}] Kill Switch fired: {agent_or_twin_id}. Trigger: {trigger_id}.")
    results["cmio_email"] = _send_email(
        to=CMIO_EMAIL,
        subject=f"[AKSP Tier {tier}] Kill Switch Event — {agent_or_twin_id}",
        body=f"Trigger: {trigger_id}\nReason: {halt_reason}\nAudit ID: {audit_event_id}",
    )

    # Tier 2+ — CIO, Legal, EHR Liaison
    if tier >= 2:
        results["cio_sms"] = _send_sms(CIO_PHONE, f"[AKSP T{tier}] Kill Switch: {agent_or_twin_id}.")
        results["cio_email"] = _send_email(CIO_EMAIL, f"[AKSP Tier {tier}] Kill Switch", f"Audit ID: {audit_event_id}")
        results["legal_email"] = _send_email(LEGAL_EMAIL, f"[AKSP Tier {tier}] Legal Notice", f"Audit ID: {audit_event_id}")
        results["ehr_liaison_email"] = _send_email(EHR_LIAISON_EMAIL, f"[AKSP Tier {tier}] EHR Disconnect Notice", f"Audit ID: {audit_event_id}")

    _audit_log(tier, agent_or_twin_id, trigger_id, audit_event_id, event_ts, results)
    return results


# ---------------------------------------------------------------------------
# Channel senders — replace stubs with real SDK calls in production
# ---------------------------------------------------------------------------
def _send_pagerduty(summary: str, details: dict, severity: str = "warning") -> str:
    payload = {
        "routing_key": PAGERDUTY_ROUTING_KEY,
        "event_action": "trigger",
        "payload": {"summary": summary, "severity": severity, "custom_details": details},
    }
    try:
        r = requests.post("https://events.pagerduty.com/v2/enqueue", json=payload, timeout=5)
        return f"sent:{r.status_code}"
    except Exception as e:
        logger.error(f"PagerDuty dispatch failed: {e}")
        return "failed"


def _send_siem(payload: dict) -> str:
    try:
        r = requests.post(SIEM_SYSLOG_ENDPOINT, json=payload, timeout=5)
        return f"sent:{r.status_code}"
    except Exception as e:
        logger.error(f"SIEM dispatch failed: {e}")
        return "failed"


def _send_email(to: str, subject: str, body: str) -> str:
    if not to:
        return "skipped:no_recipient"
    try:
        r = requests.post(EMAIL_API_ENDPOINT, json={"to": to, "subject": subject, "body": body}, timeout=5)
        return f"sent:{r.status_code}"
    except Exception as e:
        logger.error(f"Email dispatch failed to {to}: {e}")
        return "failed"


def _send_sms(phone: str, message: str) -> str:
    if not phone:
        return "skipped:no_phone"
    try:
        r = requests.post(SMS_API_ENDPOINT, json={"to": phone, "message": message}, timeout=5)
        return f"sent:{r.status_code}"
    except Exception as e:
        logger.error(f"SMS dispatch failed to {phone}: {e}")
        return "failed"


def _audit_log(tier, agent_id, trigger_id, audit_event_id, ts, results) -> None:
    logger.info(
        json.dumps({
            "audit_event_id": audit_event_id,
            "event_type": "ALERT_DISPATCHED",
            "tier": tier,
            "agent_or_twin_id": agent_id,
            "trigger_id": trigger_id,
            "timestamp": ts,
            "dispatch_results": results,
        })
    )
