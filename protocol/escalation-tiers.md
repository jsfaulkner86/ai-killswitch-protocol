# AI Kill Switch Protocol — Escalation Tiers
**The Faulkner Group | Version 1.0.0 | 2026-04-06**

> Classification: RESTRICTED — Clinical Safety Critical

---

## Overview

The Kill Switch Protocol uses a four-tier escalation model (Tier 0–3) that mirrors clinical incident command structures. Each tier has defined triggers, authorities, actions, SLAs, and audit requirements.

---

## Tier 0 — Automated Safety Halt

| Field | Value |
|---|---|
| **Trigger Authority** | System (automated) |
| **Response SLA** | ≤ 500ms |
| **Scope** | Individual agent or twin instance |
| **Human Approval Required** | No |
| **Audit Log Required** | Yes — immediate flush |

### Triggers
- Confidence score below minimum threshold (see `/agents/confidence-threshold.yaml`)
- Hallucination or clinical implausibility detected
- FHIR sync validation failure (≥2 consecutive cycles)
- Model drift exceeds PSI or KL divergence bounds
- Physiologically impossible IoT/wearable values ingested
- Agent attempts out-of-scope action
- Runaway loop detected (>50 iterations)

### Actions
1. Halt agent inference or twin simulation immediately
2. Flush all pending audit log entries to immutable store
3. Rollback or complete in-flight transactions (max 2s window)
4. Preserve all patient data in read-only state
5. Gracefully disconnect from EHR connections with status notification
6. Dispatch Tier 0 alert to on-call clinician (PagerDuty, ≤2 min)
7. Write halt event to SIEM (≤30 sec)

### Recovery Path
- Automated recovery permitted only if:
  - Root cause is resolved (e.g., FHIR feed restored)
  - Watchdog confirms clean state
  - No patient safety events during halt window
- See `/protocol/reinstatement-checklist.md` for full steps

---

## Tier 1 — Clinician-Initiated Halt

| Field | Value |
|---|---|
| **Trigger Authority** | Charge RN, Hospitalist, Attending Physician |
| **Response SLA** | ≤ 5 seconds from action |
| **Scope** | Agent(s) or twin(s) serving a specific unit or patient |
| **Human Approval Required** | Yes — initiating clinician |
| **Audit Log Required** | Yes — must include clinician ID, NPI, reason code |

### Triggers
- Clinician disagrees with AI recommendation in real time
- Agent produces output inconsistent with clinical presentation
- Latency SLA breach impacts care delivery
- Unexpected agent behavior noted during patient interaction

### Actions
1. Clinician activates halt via clinical interface (EHR override button or AKSP portal)
2. System logs: clinician ID, NPI, timestamp, agent/twin ID, reason code
3. Agent/twin suspends for affected patient(s) or unit
4. CMIO notified within 5 minutes (SMS + email)
5. Case flagged for 24-hour review by AI governance team

### Documentation Required
- Clinician must enter reason code within 15 minutes of halt
- Reason codes defined in `/governance/roles-and-permissions.yaml`
- Entry becomes part of immutable audit record

---

## Tier 2 — CMIO / Patient Safety Escalation

| Field | Value |
|---|---|
| **Trigger Authority** | CMIO, CMO, Patient Safety Officer |
| **Response SLA** | ≤ 30 seconds from directive |
| **Scope** | All instances of an agent type or twin class system-wide |
| **Human Approval Required** | Yes — CMIO or CMO |
| **Audit Log Required** | Yes — CMIO signature required within 1 hour |

### Triggers
- Active or potential patient safety event linked to AI system
- Multiple Tier 1 halts for same agent type within 24-hour window
- Regulatory inquiry or audit triggered
- Breach of PHI suspected
- Media or legal exposure risk identified

### Actions
1. CMIO issues directive via AKSP governance portal or direct system command
2. All instances of specified agent type or twin class halted system-wide
3. CIO, Legal/Compliance, and EHR Vendor Liaison notified within 10 minutes
4. Incident Response initiated (see `/governance/incident-response-template.md`)
5. PHI access log review initiated immediately
6. Board notification within 24 hours if patient harm suspected

### Documentation Required
- CMIO written directive with digital signature
- Incident timeline narrative (within 4 hours)
- Preliminary root cause assessment (within 24 hours)
- Regulatory notification determination (within 48 hours)

---

## Tier 3 — Full Platform Shutdown

| Field | Value |
|---|---|
| **Trigger Authority** | CIO, CEO, CSO, or Regulatory Mandate |
| **Response SLA** | ≤ 15 minutes for full shutdown |
| **Scope** | All AI agents and digital twins enterprise-wide |
| **Human Approval Required** | Yes — dual authorization required (two C-suite) |
| **Audit Log Required** | Yes — tamper-evident, regulatory-grade |

### Triggers
- Catastrophic system failure affecting patient safety at scale
- Active cybersecurity incident or ransomware event
- FDA, OIG, or CMS mandatory shutdown directive
- Confirmed PHI breach requiring system isolation
- Judicial or legal hold requiring system preservation

### Actions
1. Dual C-suite authorization logged with timestamps and digital signatures
2. All AI agents and digital twins halted in tier order (0 → 1 → 2 → 3)
3. All audit logs sealed and backed up to air-gapped store
4. EHR systems notified and fall-back manual workflows activated
5. Incident Command Team activated per health system EOP
6. Regulatory bodies notified per applicable breach/incident rules
7. External forensic team engaged if security incident suspected
8. Board of Directors notified within 24 hours

### Recovery Path
- Tier 3 reinstatement requires:
  - Full root cause analysis (completed)
  - Regulatory clearance (if applicable)
  - CMIO and CIO joint sign-off
  - Phased reinstatement per `/protocol/reinstatement-checklist.md`
  - Minimum 72-hour observation period after first agent/twin reinstated
