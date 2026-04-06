"""
AI Kill Switch Protocol — Digital Twin Drift Detection
The Faulkner Group | Version 1.0.0 | 2026-04-06
Compliance: FDA 21 CFR Part 11, ISO 13485:2016

Monitors production digital twin outputs for statistical drift relative to
baseline. Triggers AT-004 (suspend_twin_inference) when PSI or KL divergence
exceeds defined thresholds.
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Logging — structured JSON for SIEM ingestion
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}',
)
logger = logging.getLogger("aksp.drift_detection")


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
PSI_WARNING_THRESHOLD = 0.10   # Yellow — increased monitoring
PSI_HALT_THRESHOLD = 0.20      # Red — trigger AT-004

KL_WARNING_THRESHOLD = 0.05
KL_HALT_THRESHOLD = 0.10


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class DriftResult:
    twin_id: str
    check_timestamp: str
    psi: float
    kl_divergence: float
    status: str           # OK | WARNING | HALT
    trigger_fired: bool
    trigger_id: str = "AT-004"
    audit_event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    details: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------
def compute_psi(baseline: np.ndarray, production: np.ndarray, buckets: int = 10) -> float:
    """
    Population Stability Index.
    PSI < 0.10: no drift  |  0.10–0.20: moderate  |  > 0.20: significant drift
    """
    baseline_counts, bin_edges = np.histogram(baseline, bins=buckets)
    production_counts, _ = np.histogram(production, bins=bin_edges)

    baseline_pct = (baseline_counts + 1e-8) / len(baseline)
    production_pct = (production_counts + 1e-8) / len(production)

    psi = float(np.sum((production_pct - baseline_pct) * np.log(production_pct / baseline_pct)))
    return round(psi, 6)


def compute_kl_divergence(baseline: np.ndarray, production: np.ndarray, buckets: int = 10) -> float:
    """
    KL Divergence (relative entropy). Measures how much production
    distribution diverges from baseline.
    """
    baseline_counts, bin_edges = np.histogram(baseline, bins=buckets, density=True)
    production_counts, _ = np.histogram(production, bins=bin_edges, density=True)

    p = baseline_counts + 1e-8
    q = production_counts + 1e-8
    p /= p.sum()
    q /= q.sum()

    kl = float(np.sum(p * np.log(p / q)))
    return round(kl, 6)


def evaluate_drift(twin_id: str, baseline: np.ndarray, production: np.ndarray) -> DriftResult:
    """
    Evaluate drift for a digital twin. Returns DriftResult with status and
    whether AT-004 halt trigger should fire.
    """
    psi = compute_psi(baseline, production)
    kl = compute_kl_divergence(baseline, production)

    if psi >= PSI_HALT_THRESHOLD or kl >= KL_HALT_THRESHOLD:
        status = "HALT"
        trigger_fired = True
    elif psi >= PSI_WARNING_THRESHOLD or kl >= KL_WARNING_THRESHOLD:
        status = "WARNING"
        trigger_fired = False
    else:
        status = "OK"
        trigger_fired = False

    result = DriftResult(
        twin_id=twin_id,
        check_timestamp=datetime.now(timezone.utc).isoformat(),
        psi=psi,
        kl_divergence=kl,
        status=status,
        trigger_fired=trigger_fired,
        details={
            "psi_halt_threshold": PSI_HALT_THRESHOLD,
            "kl_halt_threshold": KL_HALT_THRESHOLD,
        },
    )

    _log_drift_event(result)

    if trigger_fired:
        _fire_halt_trigger(result)

    return result


def _log_drift_event(result: DriftResult) -> None:
    """Write drift result to immutable audit log (SIEM-ready JSON)."""
    payload = {
        "audit_event_id": result.audit_event_id,
        "event_type": "DRIFT_CHECK",
        "twin_id": result.twin_id,
        "timestamp": result.check_timestamp,
        "psi": result.psi,
        "kl_divergence": result.kl_divergence,
        "status": result.status,
        "trigger_fired": result.trigger_fired,
    }
    logger.info(json.dumps(payload))


def _fire_halt_trigger(result: DriftResult) -> None:
    """
    Fire AT-004: suspend twin inference.
    In production: call the orchestration layer halt API.
    """
    logger.warning(
        json.dumps(
            {
                "event_type": "KILL_SWITCH_TRIGGER",
                "trigger_id": result.trigger_id,
                "twin_id": result.twin_id,
                "reason": "Model drift exceeded halt threshold",
                "psi": result.psi,
                "kl_divergence": result.kl_divergence,
                "audit_event_id": result.audit_event_id,
                "timestamp": result.check_timestamp,
                "action": "suspend_twin_inference",
            }
        )
    )
    # TODO: replace with actual orchestration API call
    # requests.post(ORCHESTRATION_HALT_URL, json={"twin_id": result.twin_id, "trigger": "AT-004"})


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    baseline_data = rng.normal(loc=0.5, scale=0.1, size=1000)
    production_data = rng.normal(loc=0.7, scale=0.2, size=1000)  # Simulated drift

    result = evaluate_drift("twn-001", baseline_data, production_data)
    print(f"Twin: {result.twin_id} | PSI: {result.psi} | KL: {result.kl_divergence} | Status: {result.status}")
