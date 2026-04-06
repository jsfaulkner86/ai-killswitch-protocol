"""
AI Kill Switch Protocol — Unit Tests: Drift Detection
The Faulkner Group | Version 1.0.0 | 2026-04-06
"""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from digital_twins.drift_detection import (
    compute_psi,
    compute_kl_divergence,
    evaluate_drift,
    PSI_HALT_THRESHOLD,
    KL_HALT_THRESHOLD,
)

RNG = np.random.default_rng(42)


def baseline():
    return RNG.normal(loc=0.5, scale=0.1, size=1000)


def no_drift():
    return RNG.normal(loc=0.5, scale=0.1, size=1000)


def moderate_drift():
    return RNG.normal(loc=0.6, scale=0.15, size=1000)


def severe_drift():
    return RNG.normal(loc=0.9, scale=0.3, size=1000)


class TestComputePSI:
    def test_no_drift_below_warning(self):
        psi = compute_psi(baseline(), no_drift())
        assert psi < 0.10, f"Expected PSI < 0.10 for no-drift scenario, got {psi}"

    def test_severe_drift_above_halt_threshold(self):
        psi = compute_psi(baseline(), severe_drift())
        assert psi >= PSI_HALT_THRESHOLD, f"Expected PSI >= {PSI_HALT_THRESHOLD}, got {psi}"

    def test_returns_float(self):
        assert isinstance(compute_psi(baseline(), no_drift()), float)


class TestComputeKLDivergence:
    def test_no_drift_below_warning(self):
        kl = compute_kl_divergence(baseline(), no_drift())
        assert kl < 0.05, f"Expected KL < 0.05 for no-drift scenario, got {kl}"

    def test_severe_drift_above_halt_threshold(self):
        kl = compute_kl_divergence(baseline(), severe_drift())
        assert kl >= KL_HALT_THRESHOLD, f"Expected KL >= {KL_HALT_THRESHOLD}, got {kl}"

    def test_returns_float(self):
        assert isinstance(compute_kl_divergence(baseline(), no_drift()), float)


class TestEvaluateDrift:
    def test_no_drift_returns_ok_no_trigger(self):
        result = evaluate_drift("twn-test", baseline(), no_drift())
        assert result.status == "OK"
        assert result.trigger_fired is False

    def test_severe_drift_returns_halt_and_fires_trigger(self):
        result = evaluate_drift("twn-test", baseline(), severe_drift())
        assert result.status == "HALT"
        assert result.trigger_fired is True
        assert result.trigger_id == "AT-004"

    def test_result_contains_twin_id(self):
        result = evaluate_drift("twn-001", baseline(), no_drift())
        assert result.twin_id == "twn-001"

    def test_result_has_audit_event_id(self):
        result = evaluate_drift("twn-001", baseline(), no_drift())
        assert result.audit_event_id is not None
        assert len(result.audit_event_id) > 0
