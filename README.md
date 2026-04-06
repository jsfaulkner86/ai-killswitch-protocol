<div align="center">

<br />

```
       ██╗  ██╗██╗██╗     ██╗     ███████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗
       ██║ ██╔╝██║██║     ██║     ██╔════╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║
       █████╔╝ ██║██║     ██║     ███████╗██║ █╗ ██║██║   ██║   ██║     ███████║
       ██╔═██╗ ██║██║     ██║     ╚════██║██║███╗██║██║   ██║   ██║     ██╔══██║
       ██║  ██╗██║███████╗███████╗███████║╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║
       ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
```

### AI Kill Switch Protocol

**The safety-critical, audit-defensible governance framework for AI agents and healthcare digital twins.**

<br />

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![HIPAA](https://img.shields.io/badge/HIPAA-45%20CFR%20164-blue.svg)](./docs/compliance-mapping.md)
[![FDA 21 CFR Part 11](https://img.shields.io/badge/FDA-21%20CFR%20Part%2011-red.svg)](./docs/compliance-mapping.md)
[![ISO 13485](https://img.shields.io/badge/ISO-13485%3A2016-orange.svg)](./docs/compliance-mapping.md)
[![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)](./CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](#)

<br />

[Documentation](./docs/architecture-overview.md) · [Escalation Tiers](./protocol/escalation-tiers.md) · [Override Procedures](./protocol/override-procedures.md) · [Compliance Mapping](./docs/compliance-mapping.md)

<br />

</div>

---

## What is AKSP?

The **AI Kill Switch Protocol (AKSP)** is a structured governance framework that ensures every AI agent and digital twin operating in a healthcare environment can be **safely halted, auditably overridden, and compliantly reinstated** — in milliseconds or minutes depending on the threat tier.

Built for health systems that can't afford to find out what happens when AI goes wrong in a clinical environment.

```
Anomaly Detected  →  Watchdog Fires  →  Agent Halted (<500ms)  →  Audit Logged  →  Clinician Notified
```

---

## Why It Exists

Most AI governance frameworks tell you *what* to do. AKSP tells your system *exactly what to execute* — with SLAs, role-based authority, immutable audit trails, and a tested path back to operation.

- ⚡ **Tier 0 auto-halt in ≤500ms** — no human required
- 🔒 **Immutable audit logs** — SHA-256 chain hash, WORM-compliant storage
- 🏥 **EHR-native** — Epic FHIR R4 webhooks, graceful disconnect on halt
- 👩‍⚕️ **Clinician-first** — Override authority flows from bedside to boardroom
- 📋 **Regulation-ready** — HIPAA, FDA 21 CFR Part 11, ISO 13485, ONC HTI-1

---

## Escalation Tiers

| Tier | Name | Trigger | SLA | Authority |
|:---:|---|---|---|---|
| **0** | Automated Safety Halt | Confidence breach, hallucination, drift, IoT anomaly, runaway loop | ≤ 500ms | System (Watchdog) |
| **1** | Clinician-Initiated Halt | Clinician disagreement, latency impact, unexpected behavior | ≤ 5 sec | Charge RN / Hospitalist |
| **2** | CMIO Escalation | Patient safety event, multiple Tier 1 halts, PHI breach suspected | ≤ 30 sec | CMIO / CMO |
| **3** | Full Platform Shutdown | Catastrophic failure, ransomware, regulatory mandate | ≤ 15 min | CIO + CEO (dual auth) |

→ See [`/protocol/escalation-tiers.md`](./protocol/escalation-tiers.md) for full trigger lists, actions, and recovery paths.

---

## Repository Structure

```
ai-killswitch-protocol/
│
├── protocol/                    ← Core policy, escalation tiers, override & reinstatement
│   ├── killswitch-policy.yaml
│   ├── escalation-tiers.md
│   ├── override-procedures.md
│   └── reinstatement-checklist.md
│
├── agents/                      ← Agent registry, watchdog, circuit breaker, confidence thresholds
│   ├── agent-registry.yaml
│   ├── watchdog.yaml
│   ├── circuit-breaker.yaml
│   └── confidence-threshold.yaml
│
├── digital-twins/               ← Twin registry, drift detection, FHIR sync validation, sim guard
│   ├── twin-registry.yaml
│   ├── drift-detection.py
│   ├── fhir-sync-validation.yaml
│   └── sim-guard.yaml
│
├── integrations/                ← Epic webhook, FHIR R4 client, IoT validator, alert dispatcher
│   ├── epic-webhook.yaml
│   ├── fhir-r4-client.py
│   ├── iot-validator.py
│   └── alert-dispatcher.py
│
├── governance/                  ← Audit log schema, RBAC, incident response, data retention
│   ├── audit-log-schema.yaml
│   ├── roles-and-permissions.yaml
│   ├── incident-response-template.md
│   └── data-retention-policy.md
│
├── docs/                        ← Architecture overview, threat taxonomy, compliance mapping
│   ├── architecture-overview.md
│   ├── threat-taxonomy.md
│   └── compliance-mapping.md
│
└── tests/                       ← Unit tests and mock fixtures
    ├── test_drift_detection.py
    ├── test_iot_validator.py
    └── fixtures/
```

---

## Scope

| Domain | Coverage |
|---|---|
| **AI Agents** | Clinical decision support, care coordination, autonomous triage, medical coding, prior authorization, patient outreach, pharmacy verification |
| **Digital Twins** | Patient-in-silico models, operational workflow twins, population health models, hospital capacity twins, surgical simulation twins |
| **EHR Integrations** | Epic (FHIR R4), Oracle Health, Meditech (HL7 v2) |
| **Data Streams** | IoT sensors, wearables, real-time bedside telemetry |
| **Governance** | RBAC override authority, immutable audit logs, RCA templates, data retention |

---

## Automated Trigger Reference

| Trigger ID | Name | Action |
|---|---|---|
| AT-001 | Confidence threshold breach | Immediate halt |
| AT-002 | Hallucination / clinical implausibility | Immediate halt |
| AT-003 | FHIR sync validation failure (≥2 cycles) | Suspend twin updates |
| AT-004 | Model drift — PSI or KL divergence exceeded | Suspend twin inference |
| AT-005 | Physiologically impossible IoT values | Quarantine stream + halt agents |
| AT-006 | Agent attempts out-of-scope action | Immediate halt + security alert |
| AT-007 | Latency SLA breach (>5s, ≥3 consecutive) | Graceful halt |
| AT-008 | Runaway loop detected (>50 iterations) | Immediate halt |

→ Manual triggers (MT-001–MT-004) defined in [`/protocol/killswitch-policy.yaml`](./protocol/killswitch-policy.yaml)

---

## Compliance

| Framework | Coverage |
|---|---|
| **HIPAA** 45 CFR 164 | Access control, audit logs, incident procedures, data retention |
| **FDA 21 CFR Part 11** | Electronic records, tamper-evident audit trails, authority checks, digital signatures |
| **ISO 13485:2016** | Medical device QMS — records control, corrective action, internal audit |
| **ONC HTI-1 (2024)** | FHIR R4 interoperability, information blocking prohibition |
| **The Joint Commission** | Sentinel event reporting, clinical alarm management SLAs |

→ Full mapping in [`/docs/compliance-mapping.md`](./docs/compliance-mapping.md)

---

## Quick Start

**1. Register your agents**
```yaml
# agents/agent-registry.yaml
- agent_id: "agt-001"
  agent_name: "Your-Agent-Name"
  agent_type: clinical_decision_support
  watchdog_enabled: true
  confidence_threshold_ref: "/agents/confidence-threshold.yaml#your-agent"
```

**2. Set confidence thresholds**
```yaml
# agents/confidence-threshold.yaml
your-agent:
  minimum_confidence: 0.85
  action_on_breach: "immediate_halt"
```

**3. Configure your EHR webhook**
```yaml
# integrations/epic-webhook.yaml
epic_connection:
  api_standard: "FHIR R4"
  auth_method: "OAuth 2.0 SMART on FHIR"
  tls_version: "TLS 1.3"
```

**4. Run tests**
```bash
pytest tests/ -v
```

---

## Maintainer

<table>
  <tr>
    <td align="center">
      <strong>John Faulkner</strong><br />
      Agentic AI Architect<br />
      The Faulkner Group<br />
      <a href="https://thefaulknergroupadvisors.com">thefaulknergroupadvisors.com</a>
    </td>
  </tr>
</table>

---

## License

MIT — See [LICENSE](./LICENSE).

---

<div align="center">

*Built for health systems where AI failure is not an option.*

</div>
