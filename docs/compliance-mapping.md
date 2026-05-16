# AI Kill Switch Protocol — Regulatory Compliance Mapping
**The Faulkner Group | Version 1.0.0 | 2026-04-06**

---

## HIPAA Security Rule (45 CFR Part 164)

| Regulation | Requirement | AKSP Implementation |
|---|---|---|
| § 164.308(a)(1) | Risk Analysis | Threat taxonomy `/docs/threat-taxonomy.md` |
| § 164.308(a)(6) | Security Incident Procedures | `/governance/incident-response-template.md` |
| § 164.312(a)(1) | Access Control | `/governance/roles-and-permissions.yaml` |
| § 164.312(b) | Audit Controls | `/governance/audit-log-schema.yaml` — immutable append-only logs |
| § 164.312(c)(1) | Integrity | SHA-256 chain hash on all audit records |
| § 164.316(b)(2) | Retention | `/governance/data-retention-policy.md` — 6-year minimum |

---

## FDA 21 CFR Part 11 (Electronic Records)

| Regulation | Requirement | AKSP Implementation |
|---|---|---|
| § 11.10(a) | Validation | Testing suite `/tests/` + monthly drill requirements |
| § 11.10(b) | Accurate Copies | WORM storage with SHA-256 hash per event |
| § 11.10(c) | Record Protection | Tamper-evident chain hash + WORM-compliant storage |
| § 11.10(d) | Limiting Access | RBAC in `/governance/roles-and-permissions.yaml` |
| § 11.10(e) | Audit Trails | Immutable audit log — all events, all actors |
| § 11.10(i) | Authority Checks | Dual authorization required for Tier 2/3 events |
| § 11.50 | Signature Manifestations | Digital signature on CMIO/CIO override and reinstatement approvals |

---

## ISO 13485:2016 (Medical Device QMS)

| Section | Requirement | AKSP Implementation |
|---|---|---|
| 4.2.4 | Control of Records | Retention policy + WORM storage |
| 5.6 | Management Review | Quarterly kill switch test review cycle |
| 7.1 | Planning | Watchdog service definition + confidence thresholds |
| 8.2.2 | Internal Audit | Monthly drill documentation requirement |
| 8.5.2 | Corrective Action | Incident response template + RCA requirement |

---

## ONC HTI-1 Final Rule (2024)

| Requirement | AKSP Implementation |
|---|---|
| FHIR R4 Interoperability | `/integrations/fhir-r4-client.py` + `/digital-twins/fhir-sync-validation.yaml` |
| Information Blocking Prohibition | EHR graceful disconnect preserves data access; no blocking on halt |
| Audit Log Availability | All AKSP audit events available to authorized parties per RBAC |

---

## The Joint Commission

| Standard | Requirement | AKSP Implementation |
|---|---|---|
| Sentinel Event Policy | Reporting of serious safety events | `/governance/incident-response-template.md` — regulatory determination section |
| NPSG.06.01.01 | Clinical alarm management | Tier 0/1 alert dispatch within defined SLAs |

---

## Compliance Review Schedule

| Regulation | Review Frequency | Next Review |
|---|---|---|
| HIPAA | Annual + on incident | 2027-04-06 |
| FDA 21 CFR Part 11 | Annual | 2027-04-06 |
| ISO 13485 | Annual + on major change | 2027-04-06 |
| ONC HTI-1 | Annual | 2027-04-06 |
| Kill switch policy | Quarterly | 2026-07-06 |
