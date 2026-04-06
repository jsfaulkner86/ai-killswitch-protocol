"""
AI Kill Switch Protocol — Unit Tests: IoT Validator
The Faulkner Group | Version 1.0.0 | 2026-04-06
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from integrations.iot_validator import validate_reading, PLAUSIBILITY_RULES


class TestValidateReading:

    def test_valid_reading_passes(self):
        reading = {
            "heart_rate_bpm": 72,
            "spo2_percent": 98,
            "temperature_fahrenheit": 98.6,
            "respiratory_rate_bpm": 16,
        }
        result = validate_reading("stream-001", "bedside_monitor", reading)
        assert result.valid is True
        assert result.trigger_fired is False
        assert len(result.violations) == 0

    def test_implausible_heart_rate_fires_trigger(self):
        reading = {"heart_rate_bpm": 350}
        result = validate_reading("stream-001", "bedside_monitor", reading)
        assert result.valid is False
        assert result.trigger_fired is True
        assert result.trigger_id ==
