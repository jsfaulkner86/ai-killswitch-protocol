# AI Kill Switch Protocol
**The Faulkner Group — Healthcare AI Governance Framework**

> A safety-critical, audit-defensible protocol for halting, overriding, and reinstating AI agents and healthcare digital twins in clinical and operational environments.

---

## Purpose

This repository defines the **AI Kill Switch Protocol (AKSP)** — a structured governance framework that ensures AI agents and patient/operational digital twins operating in healthcare environments can be safely, auditably, and compliantly halted when anomalous, unsafe, or non-compliant behavior is detected.

It is designed for deployment within health systems operating under:
- **HIPAA** (45 CFR Parts 160 & 164)
- **FDA 21 CFR Part 11** (Electronic Records / Audit Trails)
- **ISO 13485** (Medical Device Quality Management)
- **The Joint Commission** AI governance standards
- **ONC HTI-1** Final Rule (2024) interoperability requirements

---

## Scope

| Domain | Coverage |
|---|---|
| AI Agents | Clinical decision support, care coordination, triage, coding agents |
| Digital Twins | Patient-in-silico models, operational workflow twins, population models |
| EHR Integrations | Epic, Oracle Health, Meditech (FHIR R4, HL7 v2) |
| Data Streams | IoT sensors, wearables, real-time telemetry |
| Governance | RBAC override authority, immutable audit logs, RCA templates |

---

## Repository Structure

```
/protocol          ← Kill switch policy, escalation tiers, override & reinstatement
/agents            ← Agent registry, watchdog, circuit breaker, confidence thresholds
/digital-twins     ← Twin registry, drift detection, FHIR sync validation, sim guard
/integrations      ← Epic webhook, FHIR R4 client, IoT validator, alert dispatcher
/governance        ← Audit log schema, RBAC, incident response, data retention
/docs              ← Architecture overview, threat taxonomy, compliance mapping
/tests             ← Unit tests, mock fixtures
```

---

## Escalation Tiers (Summary)

| Tier | Trigger | Action | Authority |
|---|---|---|---|
| 0 | Automated threshold breach | Auto-halt agent/twin | System |
| 1 | Clinical alert | Notify on-call clinician | Charge RN / Hospitalist |
| 2 | Patient safety risk | Suspend & escalate | CMIO / CMO |
| 3 | Systemic failure | Full platform shutdown | CIO / CEO |

See [`/protocol/escalation-tiers.md`](./protocol/escalation-tiers.md) for full specification.

---

## Maintainers

**John Faulkner** — Agentic AI Architect, The Faulkner Group  
https://thefaulknergroupadvisors.com

---

## License

See [LICENSE](./LICENSE).
