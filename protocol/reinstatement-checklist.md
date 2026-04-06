# AI Kill Switch Protocol — Reinstatement Checklist
**The Faulkner Group | Version 1.0.0 | 2026-04-06**

> Classification: RESTRICTED — Clinical Safety Critical  
> This checklist must be completed in full before any halted AI agent or digital twin is returned to active status.

---

## Pre-Reinstatement Gate Criteria

All gates must be PASSED before reinstatement workflow begins:

- [ ] **Gate 1**: Root cause of halt has been identified and documented
- [ ] **Gate 2**: Root cause has been remediated (code fix, data fix, or config change deployed)
- [ ] **Gate 3**: No active patient safety event linked to the halted system
- [ ] **Gate 4**: No active regulatory hold on the system
- [ ] **Gate 5**: All audit logs from halt event are complete and validated
- [ ] **Gate 6**: CMIO or designee has reviewed and approved reinstatement

---

## Reinstatement Steps

### Phase 1 — Technical Validation
- [ ] Unit tests passing for affected agent/twin component
- [ ] Integration tests passing against staging FHIR environment
- [ ] Confidence threshold configuration verified
- [ ] Drift detection baseline recalibrated (if model drift was root cause)
- [ ] FHIR sync validator confirms clean data feed
- [ ] Circuit breaker in CLOSED state (not HALF-OPEN)
- [ ] Watchdog process confirmed running and healthy
- [ ] IoT/wearable data stream validation passing

### Phase 2 — Clinical Validation
- [ ] CMIO or clinical designee reviews agent/twin outputs in staging
- [ ] Sample outputs reviewed against clinical guidelines (minimum 10 test cases)
- [ ] No clinical implausibility flags in test run
- [ ] EHR integration smoke test passed (Epic/Oracle sandbox)
- [ ] On-call clinician briefed on reinstatement and monitoring plan

### Phase 3 — Governance Sign-Off
- [ ] Reinstatement Authorization Form completed and signed
- [ ] Dual sign-off obtained for Tier 2/3 reinstatement
- [ ] Incident Response record updated with reinstatement details
- [ ] AI Governance Committee notified
- [ ] Legal/Compliance cleared (for Tier 2/3 events)
- [ ] EHR vendor notified of reinstatement (if applicable)

### Phase 4 — Phased Reinstatement

| Phase | Scope | Duration | Monitoring Level |
|---|---|---|---|
| 4A | Single patient / single unit (shadow mode) | 30 min | Continuous human review |
| 4B | Single unit (active, monitored) | 4 hours | Enhanced watchdog |
| 4C | Full deployment (elevated monitoring) | 72 hours | Elevated watchdog + daily review |
| 4D | Standard operations | Ongoing | Standard watchdog |

> Shadow mode: agent/twin runs in parallel with outputs logged but not delivered to clinical workflow.

### Phase 5 — Post-Reinstatement Review
- [ ] 24-hour post-reinstatement review completed
- [ ] 72-hour post-reinstatement review completed
- [ ] Lessons learned documented in incident record
- [ ] Protocol or configuration updates applied if identified
- [ ] Updated version pushed to repository with changelog entry

---

## Reinstatement Authorization Form

```
REINSTATEMENT AUTHORIZATION
─────────────────────────────────────────────────────────────
Halt Event ID:           [UUID]
Agent/Twin ID:           [ID]
Halt Date/Time (UTC):    [ISO 8601]
Root Cause Summary:      [narrative]
Remediation Summary:     [narrative]

Primary Authorizer
  Name:                  []
  Role:                  []
  Digital Signature:     []
  Date/Time (UTC):       [ISO 8601]

Dual Authorizer (Tier 2/3 only)
  Name:                  []
  Role:                  []
  Digital Signature:     []
  Date/Time (UTC):       [ISO 8601]

Clinical Clearance
  Cleared By:            []
  Role/NPI:              []
  Date/Time (UTC):       [ISO 8601]

Phased Reinstatement Plan Attached: [ ] Yes  [ ] No
Regulatory Clearance Attached:      [ ] Yes  [ ] No  [ ] N/A
─────────────────────────────────────────────────────────────
```
