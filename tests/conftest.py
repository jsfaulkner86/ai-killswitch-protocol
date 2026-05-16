"""
pytest fixtures for the AI Kill Switch Protocol test suite.

Provides synthetic IoT readings and drift data — no live devices,
no PHI, no external calls required.
"""

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# IoT / wearable stream fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_reading():
    """A physiologically plausible wearable reading — should pass validation."""
    return {
        "heart_rate_bpm": 72,
        "spo2_percent": 98,
        "systolic_bp_mmhg": 118,
        "diastolic_bp_mmhg": 76,
        "temperature_fahrenheit": 98.6,
        "respiratory_rate_bpm": 16,
    }


@pytest.fixture
def implausible_reading():
    """A reading with implausible values — should trigger AT-005."""
    return {
        "heart_rate_bpm": 350,        # Way above 300 max
        "spo2_percent": 101,          # Above 100 max
        "temperature_fahrenheit": 75, # Below 85 min
    }


@pytest.fixture
def partial_reading():
    """A reading with only known metrics — unknown keys should pass through."""
    return {
        "heart_rate_bpm": 80,
        "unknown_sensor_xyz": 999,   # Unknown — should not trigger violation
    }


@pytest.fixture
def non_numeric_reading():
    """A reading with a non-numeric value — should trigger violation."""
    return {
        "heart_rate_bpm": "fast",
    }


# ---------------------------------------------------------------------------
# Drift detection fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def rng():
    return np.random.default_rng(42)


@pytest.fixture
def stable_distributions(rng):
    """Baseline and production from same distribution — no drift."""
    baseline = rng.normal(loc=0.5, scale=0.1, size=1000)
    production = rng.normal(loc=0.5, scale=0.1, size=1000)
    return baseline, production


@pytest.fixture
def drifted_distributions(rng):
    """Baseline and production from shifted distributions — significant drift."""
    baseline = rng.normal(loc=0.5, scale=0.1, size=1000)
    production = rng.normal(loc=0.9, scale=0.3, size=1000)  # Large shift
    return baseline, production


@pytest.fixture
def warning_distributions(rng):
    """Moderate shift — should produce WARNING status, not HALT."""
    baseline = rng.normal(loc=0.5, scale=0.1, size=1000)
    production = rng.normal(loc=0.58, scale=0.13, size=1000)  # Mild shift
    return baseline, production
