# CLAUDE.md — AI Kill Switch Protocol

Operating instructions for AI coding assistants working in this repository.

---

## What This Repo Is

The **AI Kill Switch Protocol (AKSP)** is a governance and implementation framework for safely halting, suspending, or constraining AI agents and healthcare digital twins. It is used by The Faulkner Group to enforce clinical safety boundaries in women's health AI systems.

This repo contains:
- **Protocol specs** (`protocol/`) — YAML and Markdown defining kill switch policies, escalation tiers, override procedures, and reinstatement checklists
- **Python modules** (`integrations/`, `digital-twins/`) — Runnable implementations of IoT validation, FHIR sync, alert dispatch, and drift detection
- **Governance docs** (`governance/`) — Audit log schema, roles/permissions, data retention, incident response
- **Tests** (`tests/`) — pytest suite covering drift detection and IoT validation

---

## Architecture Overview

```
Trigger Signal (IoT / FHIR / Agent Behavior)
    │
    ▼
Kill Switch Evaluator
    ├── integrations/iot-validator.py       ← plausibility gate
    ├── digital-twins/drift-detection.py   ← PSI / KL divergence
    └── integrations/fhir-r4-client.py     ← FHIR sync validation
    │
    ▼
Escalation Tier (protocol/escalation-tiers.md)
    ├── AT-004: suspend_twin_inference
    └── AT-005: quarantine_stream_halt_dependent_agents
    │
    ▼
Alert Dispatcher (integrations/alert-dispatcher.py)
    │
    ▼
Governance Audit Log (governance/audit-log-schema.yaml)
```

---

## Code Standards

- Python 3.11+, async-first where I/O is involved
- Pydantic v2 for any new data models — replace `@dataclass` with Pydantic where schemas cross service boundaries
- Type hints on all functions
- No PHI in logs — `stream_id`, `twin_id`, and `patient_id` are pseudonymized identifiers only
- Structured JSON logging throughout (SIEM-ready)
- `pytest` for all tests — no test file without at least one assertion on the trigger-fired path

---

## PHI Rules

- `stream_id`, `twin_id`, `patient_id` are **pseudonymized identifiers** — never log actual patient names, MRNs, or DOBs
- Audit log events are append-only — no mutation or deletion of logged events
- All FHIR calls must use Bearer tokens over TLS — never plain HTTP
- Kill switch halt events must be written to the audit log **before** any downstream action fires

---

## Trigger IDs Quick Reference

| Trigger | Action | Module |
|---|---|---|
| `AT-001` | Halt agent decision loop | `protocol/killswitch-policy.yaml` |
| `AT-002` | Revoke tool permissions | `protocol/killswitch-policy.yaml` |
| `AT-003` | Escalate to human reviewer | `protocol/escalation-tiers.md` |
| `AT-004` | Suspend twin inference | `digital-twins/drift-detection.py` |
| `AT-005` | Quarantine IoT stream + halt dependent agents | `integrations/iot-validator.py` |

---

## Common Commands

```bash
make install     # install all dependencies
make test        # run pytest suite
make lint        # ruff check
make format      # black format
make validate    # run IoT validator example
make drift       # run drift detection example
```

---

## Never Do

- Do not log PHI fields (name, MRN, DOB, diagnosis) — use pseudonymized IDs only
- Do not remove or alter the `_audit_log()` call sequence — audit must fire before halt
- Do not change trigger IDs (`AT-001` through `AT-005`) without updating `protocol/killswitch-policy.yaml`
- Do not add new plausibility rules to `iot-validator.py` without a matching test in `tests/test_iot_validator.py`
- Do not mock the audit log in production — only mock in tests
