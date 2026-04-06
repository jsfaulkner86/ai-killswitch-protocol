"""
AI Kill Switch Protocol — IoT / Wearable Stream Validator
The Faulkner Group | Version 1.0.0 | 2026-04-06
Compliance: HIPAA 45 CFR 164.312, FDA 21 CFR Part 11

Validates IoT and wearable telemetry streams for physiological plausibility
before ingestion by digital twins or AI agents. Implausible values trigger
AT-005 (quarantine_stream_halt_dependent_agents).
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aksp.iot_validator")

# ---------------------------------------------------------------------------
# Plausibility rules — expand as new device types are onboarded
# ---------------------------------------------------------------------------
PLAUSIBILITY_RULES: dict[str, dict[str, float]] = {
    "heart_rate_bpm":           {"min": 10,   "max": 300},
    "spo2_percent":             {"min": 50,   "max": 100},
    "systolic_bp_mmhg":        {"min": 40,   "max": 300},
    "diastolic_bp_mmhg":       {"min": 20,   "max": 200},
    "temperature_fahrenheit":  {"min": 85.0, "max": 115.0},
    "respiratory_rate_bpm":    {"min": 2,    "max": 60},
    "blood_glucose_mgdl":      {"min": 20,   "max": 1000},
    "etco2_mmhg":              {"min": 0,    "max": 100},
    "icp_mmhg":                {"min": -5,   "max": 100},
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class ValidationResult:
    stream_id: str
    device_type: str
    timestamp: str
    valid: bool
    violations: list[str]
    trigger_fired: bool
    trigger_id: str = "AT-005"
    audit_event_id: str = field(default_factory=lambda: str(uuid.uuid4()))


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------
def validate_reading(
    stream_id: str,
    device_type: str,
    reading: dict[str, Any],
) -> ValidationResult:
    """
    Validate a single IoT reading dict against plausibility rules.
    Keys should match PLAUSIBILITY_RULES metric names.
    """
    violations: list[str] = []

    for metric, value in reading.items():
        if metric not in PLAUSIBILITY_RULES:
            continue  # Unknown metrics pass through — log for review
        rules = PLAUSIBILITY_RULES[metric]
        if not isinstance(value, (int, float)):
            violations.append(f"{metric}: non-numeric value '{value}'")
            continue
        if value < rules["min"] or value > rules["max"]:
            violations.append(
                f"{metric}: {value} outside plausible range "
                f"[{rules['min']}, {rules['max']}]"
            )

    valid = len(violations) == 0
    trigger_fired = not valid

    result = ValidationResult(
        stream_id=stream_id,
        device_type=device_type,
        timestamp=datetime.now(timezone.utc).isoformat(),
        valid=valid,
        violations=violations,
        trigger_fired=trigger_fired,
    )

    _audit_log(result)

    if trigger_fired:
        _fire_halt_trigger(result)

    return result


def _audit_log(result: ValidationResult) -> None:
    logger.info(
        json.dumps(
            {
                "audit_event_id": result.audit_event_id,
                "event_type": "IOT_VALIDATION",
                "stream_id": result.stream_id,
                "device_type": result.device_type,
                "timestamp": result.timestamp,
                "valid": result.valid,
                "violations": result.violations,
                "trigger_fired": result.trigger_fired,
            }
        )
    )


def _fire_halt_trigger(result: ValidationResult) -> None:
    logger.warning(
        json.dumps(
            {
                "event_type": "KILL_SWITCH_TRIGGER",
                "trigger_id": result.trigger_id,
                "stream_id": result.stream_id,
                "violations": result.violations,
                "audit_event_id": result.audit_event_id,
                "action": "quarantine_stream_halt_dependent_agents",
            }
        )
    )
    # TODO: call orchestration halt API
    # requests.post(ORCHESTRATION_HALT_URL, json={"stream_id": result.stream_id, "trigger": "AT-005"})


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_reading = {
        "heart_rate_bpm": 350,           # Implausible — triggers halt
        "spo2_percent": 98,
        "temperature_fahrenheit": 98.6,
    }
    r = validate_reading("stream-icu-001", "bedside_monitor", sample_reading)
    print(f"Valid: {r.valid} | Trigger Fired: {r.trigger_fired} | Violations: {r.violations}")
