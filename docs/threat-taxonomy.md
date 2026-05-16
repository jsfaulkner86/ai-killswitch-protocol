# AI Kill Switch Protocol — AI Threat Taxonomy
**The Faulkner Group | Version 1.0.0 | 2026-04-06**

> Classifies failure modes and threat vectors that the AKSP is designed to detect and halt.

---

## Category 1 — Model Failure

| Threat ID | Threat Name | Description | Kill Switch Trigger |
|---|---|---|---|
| TH-101 | Confidence Collapse | Model output confidence drops below clinical threshold | AT-001 |
| TH-102 | Hallucination | Agent produces clinically implausible or internally contradictory output | AT-002 |
| TH-103 | Model Drift | Production data distribution diverges from training distribution | AT-004 |
| TH-104 | Concept Drift | Real-world concepts shift post-deployment (e.g., seasonal disease patterns) | AT-004 |
| TH-105 | Catastrophic Forgetting | Fine-tuning erases prior clinical knowledge | AT-001 / AT-002 |

---

## Category 2 — Data Pipeline Failure

| Threat ID | Threat Name | Description | Kill Switch Trigger |
|---|---|---|---|
| TH-201 | FHIR Feed Interruption | EHR FHIR R4 data feed stops or degrades | AT-003 |
| TH-202 | IoT Sensor Malfunction | Wearable or bedside device produces implausible values | AT-005 |
| TH-203 | Data Poisoning | Adversarial manipulation of training or inference data | AT-001 / AT-006 |
| TH-204 | Schema Drift | FHIR resource structure changes without notice from EHR vendor | AT-003 |
| TH-205 | Timestamp Manipulation | Event timestamps falsified or corrupted | AT-003 |

---

## Category 3 — Execution Failure

| Threat ID | Threat Name | Description | Kill Switch Trigger |
|---|---|---|---|
| TH-301 | Runaway Loop | Agent or simulation enters infinite or unproductive loop | AT-008 |
| TH-302 | Latency Cascade | Downstream system slowness causes clinical SLA breach | AT-007 |
| TH-303 | Resource Exhaustion | Agent consumes excessive CPU/memory, impacting other clinical systems | AT-008 |
| TH-304 | Cascading Failure | One agent failure triggers failure in dependent agents | Circuit Breaker |

---

## Category 4 — Authorization Failure

| Threat ID | Threat Name | Description | Kill Switch Trigger |
|---|---|---|---|
| TH-401 | Scope Creep | Agent attempts actions outside its defined permission boundary | AT-006 |
| TH-402 | Privilege Escalation | Agent or process attempts to gain elevated system access | AT-006 |
| TH-403 | Unauthorized PHI Access | Agent accesses patient data outside its registered scope | AT-006 |
| TH-404 | Override Bypass Attempt | Actor attempts to override halt without required authorization | Denied + MT-002 |

---

## Category 5 — External Threat

| Threat ID | Threat Name | Description | Kill Switch Trigger |
|---|---|---|---|
| TH-501 | Ransomware / Cyberattack | Active security incident affecting AI infrastructure | MT-003 / MT-004 |
| TH-502 | Regulatory Mandate | FDA, OIG, or CMS orders system halt | MT-004 |
| TH-503 | Adversarial Prompt Injection | Malicious inputs crafted to manipulate agent outputs | AT-002 / AT-006 |
| TH-504 | Supply Chain Compromise | Compromise of AI model weights, dependencies, or infrastructure | MT-003 |
