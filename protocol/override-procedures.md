# AI Kill Switch Protocol — Override Procedures
**The Faulkner Group | Version 1.0.0 | 2026-04-06**

> Classification: RESTRICTED — Clinical Safety Critical  
> Regulatory Basis: FDA 21 CFR Part 11.10(e), HIPAA 45 CFR 164.312(b)

---

## Purpose

This document defines the authorized procedures for overriding an active AI agent or digital twin kill switch event. Override authority is strictly role-based and every override action must be auditably logged. **No override is permitted without a documented clinical or operational justification.**

---

## Override Authority Matrix

| Halt Tier | Minimum Override Authority | Dual Authorization Required | Justification Required |
|---|---|---|---|
| Tier 0 (Auto) | Charge RN or Hospitalist | No | Yes — reason code |
| Tier 1 (Clinician) | CMIO or designee | No | Yes — narrative |
| Tier 2 (CMIO) | CIO + CMIO jointly | Yes | Yes — written directive |
| Tier 3 (Full Shutdown) | CEO + CIO | Yes | Yes — executive memo + regulatory clearance |

---

## Override Workflow

### Step 1 — Identify Halt Context
- Retrieve halt event ID from audit log
- Confirm affected agent(s)/twin(s) IDs and scope
- Review automated trigger report or clinician halt reason

### Step 2 — Assess Patient Safety Status
- Confirm no active patient safety event is in progress
- Check for concurrent Tier 1+ events on same unit/system
- Obtain sign-off from charge clinician or Patient Safety Officer

### Step 3 — Document Override Justification
Required fields (must be entered before override is permitted):
```
Override Justification Record
──────────────────────────────
Override Requested By: [Name, Role, Employee ID]
NPI (if clinician): [NPI number]
Date/Time (UTC): [ISO 8601 timestamp]
Halt Event ID: [UUID from audit log]
Agent/Twin ID(s): [list]
Halt Tier: [0 / 1 / 2 / 3]
Justification Narrative: [minimum 50 characters]
Patient Safety Clearance By: [Name, Role]
Dual Auth (if required): [Name, Role, Timestamp]
```

### Step 4 — Execute Override
- Override action logged atomically with justification record
- Override confirmation sent to CMIO and on-call clinician
- Agent/twin enters **SUPERVISED_RESTART** state (not full active)
- Watchdog monitoring elevated for 30 minutes post-override

### Step 5 — Post-Override Monitoring
- Enhanced monitoring window: **30 minutes minimum**
- Any anomaly during monitoring window triggers immediate re-halt
- Clinical team receives real-time status updates every 5 minutes
- Override review required within 24 hours by AI Governance Committee

---

## Prohibited Override Scenarios

Override is **not permitted** under any circumstances when:

1. An active patient safety event is under investigation involving the halted system
2. A regulatory hold (FDA, OIG, CMS) is in place
3. The root cause of the halt has not been identified
4. PHI breach is suspected or confirmed
5. Override would require bypassing dual authorization for Tier 2/3 events
6. System is in forensic hold (legal/judicial)

Any attempt to override under these conditions must be flagged to Legal and Compliance immediately and denied by the system.

---

## Emergency Clinical Override (Tier 0 Only)

In scenarios where an automated halt directly threatens patient care delivery (e.g., an AI-assisted ventilator management agent halts mid-protocol):

1. Charge RN or Attending may invoke **Emergency Clinical Override (ECO)**
2. ECO bypasses the standard 5-step workflow but requires:
   - Voice confirmation recorded (if available)
   - Reason code entered within 5 minutes of override
   - Automatic CMIO notification
3. ECO events are flagged as **PRIORITY REVIEW** in audit log
4. ECO is subject to mandatory 24-hour root cause review

> ⚠️ Emergency Clinical Override does not waive audit requirements — it defers them with a mandatory completion window.
