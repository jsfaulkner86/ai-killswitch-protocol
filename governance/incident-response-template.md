# AI Kill Switch Protocol — Incident Response Template
**The Faulkner Group | Version 1.0.0 | 2026-04-06**

> Classification: RESTRICTED — Clinical Safety Critical  
> Regulatory Basis: HIPAA 45 CFR 164.308(a)(6), FDA 21 CFR Part 11, Joint Commission Sentinel Event Policy

---

## Incident Identification

| Field | Value |
|---|---|
| **Incident ID** | `INC-[YYYY-MM-DD]-[NNN]` |
| **Date/Time of Detection (UTC)** | |
| **Date/Time of Kill Switch Activation (UTC)** | |
| **Kill Switch Tier Activated** | [ ] 0  [ ] 1  [ ] 2  [ ] 3 |
| **Trigger ID(s)** | e.g., AT-001, MT-002 |
| **Agent(s) / Twin(s) Affected** | |
| **Scope of Impact** | Individual patient / Unit / System-wide |
| **Detected By** | System Watchdog / Clinician / CMIO / Other |
| **Reported By (Name, Role, Employee ID)** | |

---

## Initial Impact Assessment

**Was active patient care affected?**  
[ ] Yes — describe below  
[ ] No  

**Description of Clinical Impact:**  
_(Minimum 100 characters required)_

**Was PHI exposed, exfiltrated, or potentially compromised?**  
[ ] Yes — initiate HIPAA Breach Assessment (see /governance/data-retention-policy.md)  
[ ] No  
[ ] Under investigation  

**Were any downstream clinical systems impacted (EHR, monitoring, pharmacy)?**  
[ ] Yes — list systems:  
[ ] No  

---

## Timeline Narrative

| Time (UTC) | Event |
|---|---|
| | Anomaly first detected |
| | Kill switch activated |
| | On-call clinician notified |
| | CMIO notified |
| | CIO notified (Tier 2+) |
| | EHR vendor notified |
| | AI systems confirmed halted |
| | Incident Response Team convened |

---

## Root Cause Analysis

**Immediate Cause:**  
_(What directly triggered the kill switch?)_

**Contributing Factors:**  
_(What conditions allowed the immediate cause to occur?)_

**Systemic Factors:**  
_(What gaps in process, design, or governance created the conditions?)_

**Root Cause Statement:**  
_(One concise statement — e.g., "Model drift exceeded PSI threshold due to distribution shift in ICU patient cohort following seasonal influenza surge, not captured in last quarterly recalibration.")_

---

## Corrective Actions

| Action | Owner | Due Date | Status |
|---|---|---|---|
| | | | |
| | | | |

---

## Regulatory Determination

| Question | Answer |
|---|---|
| Does this meet HIPAA Breach notification threshold? | [ ] Yes [ ] No [ ] TBD |
| Does this require FDA MedWatch report? | [ ] Yes [ ] No [ ] TBD |
| Does this require Joint Commission report? | [ ] Yes [ ] No [ ] TBD |
| Does this require CMS notification? | [ ] Yes [ ] No [ ] TBD |
| External notification deadline (if applicable) | |

---

## Sign-Off

| Role | Name | Signature | Date |
|---|---|---|---|
| Incident Lead | | | |
| CMIO | | | |
| CIO (Tier 2+) | | | |
| Compliance Officer | | | |
| Legal Counsel (Tier 3 or PHI breach) | | | |

---

## Attachments

- [ ] Audit log export (Audit Event ID range: _______)
- [ ] Watchdog alert log
- [ ] PHI impact assessment (if applicable)
- [ ] Communications log (notifications sent)
- [ ] Reinstatement checklist (once recovery authorized)
