# Security Policy

> **Project:** AI Killswitch Protocol  
> **Maintainer:** The Faulkner Group  
> **Effective Date:** 2026-05-20  
> **Scope:** This policy covers all code, configurations, agent definitions, digital-twin schemas, governance rules, and integration adapters in this repository.

---

## ⚠️ Healthcare & PHI Notice

This project is designed to operate in or adjacent to **women's health clinical environments** and may interact with protected health information (PHI) via FHIR R4/R5 APIs, EHR integrations (Epic), and digital twin pipelines.

- **Do not include real patient data, PHI, or PII in any issue, pull request, commit, or bug report.**
- All killswitch trigger events, audit logs, and agent state snapshots used in reports must be **fully de-identified or synthetic** before submission.
- Suspected PHI exposure via a security vulnerability must be treated as a **potential HIPAA breach** and escalated accordingly (see Reporting section).

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main` branch (latest) | ✅ Active |
| Tagged releases (`v1.x`) | ✅ Patch support for 12 months post-release |
| All prior versions | ❌ No longer supported |

---

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

### Preferred Channel

Report vulnerabilities via **GitHub's private Security Advisory** feature:

1. Navigate to the [Security tab](https://github.com/jsfaulkner86/ai-killswitch-protocol/security/advisories/new) of this repository.
2. Click **"Report a vulnerability"**.
3. Complete the advisory form with as much detail as possible (see template below).

### Backup Channel

If GitHub advisories are unavailable, email:

```
security@thefaulknergroupadvisors.com
```

Encrypt sensitive disclosures with the project maintainer's GPG key (published at `https://thefaulknergroupadvisors.com/.well-known/security.txt`).

---

## Response SLA

| Severity | Initial Acknowledgment | Triage Complete | Target Patch |
|----------|----------------------|-----------------|--------------|
| Critical (CVSS ≥ 9.0) | 24 hours | 48 hours | 7 days |
| High (CVSS 7.0–8.9) | 48 hours | 5 business days | 30 days |
| Medium (CVSS 4.0–6.9) | 5 business days | 10 business days | 60 days |
| Low (CVSS < 4.0) | 10 business days | 20 business days | Next release cycle |

**PHI Exposure Path:** Any vulnerability that could expose PHI is automatically escalated to **Critical**, regardless of base CVSS score, and triggers HIPAA breach assessment procedures.

---

## Vulnerability Report Template

Please include the following in your report:

```
### Summary
[One-paragraph description of the vulnerability]

### Affected Component
[ ] agents/          [ ] digital-twins/    [ ] governance/
[ ] protocol/        [ ] integrations/     [ ] core config / secrets handling

### Severity Estimate
CVSS Score (if known): ___
PHI Exposure Risk: [ ] Yes  [ ] No  [ ] Unknown

### Steps to Reproduce
1.
2.
3.

### Proof of Concept
[Code snippet, curl command, or description — NO real PHI]

### Suggested Fix (optional)
[Your recommendation]

### Environment
- Python version:
- Dependency versions (requirements.txt or pyproject.toml snapshot):
- Deployment context (local / staging / production):
```

---

## Scope

### In Scope

- **Agent logic flaws** — killswitch bypass, race conditions in trigger evaluation, unsafe state transitions
- **Secrets exposure** — API keys, LLM provider tokens, EHR credentials leaked in logs, environment files, or committed config
- **PHI leakage paths** — agent scratchpad or memory layers persisting identifiable patient data
- **Governance rule bypass** — mechanisms that allow agents to circumvent audit trails, override approvals, or suppress kill events
- **Digital twin promotion vulnerabilities** — paths that allow synthetic twin state to overwrite live EHR data without authorization
- **FHIR/HL7 integration injection** — malformed payloads that manipulate clinical resource reads/writes
- **Dependency vulnerabilities** — CVEs in `requirements.txt` / `pyproject.toml` dependencies with exploitable attack surfaces in this context

### Out of Scope

- Vulnerabilities in upstream LLM provider infrastructure (OpenAI, Anthropic, etc.) — report directly to those vendors
- Social engineering attacks against The Faulkner Group staff
- Physical security issues
- Issues in forked or derivative works not maintained by this repository
- Theoretical vulnerabilities without a realistic attack path

---

## Security Design Principles

This project is built on the following security invariants. Reports that demonstrate a violation of these principles are treated as high priority:

1. **Kill events are irreversible at the agent layer** — no agent action can cancel a killswitch trigger once emitted; only an authorized human operator can resume.
2. **No PHI in agent memory or logs by default** — all patient identifiers must be tokenized before entering agent context windows.
3. **Audit trail integrity** — killswitch events, overrides, and state transitions must be append-only and tamper-evident.
4. **Least-privilege tool access** — agents are scoped to minimum required FHIR resource permissions; no agent holds write access to clinical resources unless explicitly granted.
5. **Digital twin / live EHR isolation** — twin environments are network-isolated from production EHR by default; promotion requires explicit human approval and dual-write confirmation.

---

## Coordinated Disclosure Policy

- The Faulkner Group follows a **90-day coordinated disclosure** window from initial report to public advisory.
- We will work with reporters to validate the fix before public disclosure.
- Reporters who follow this policy in good faith will be credited in the Security Advisory (if they consent) and are protected from legal action related to good-faith research.
- If a vulnerability is being actively exploited in the wild, we reserve the right to accelerate disclosure timelines.

---

## Dependency & Supply Chain Security

- Dependencies are pinned in `pyproject.toml` and `requirements.txt`.
- Maintainers run `pip-audit` and `safety check` on every release branch before tagging.
- GitHub Dependabot alerts are enabled on this repository.
- Contributors must not introduce new dependencies without a documented rationale in the PR description.

---

## Secret Scanning & CI Enforcement

- GitHub Secret Scanning is enabled on this repository.
- Pre-commit hooks (see `.github/hooks/`) enforce `detect-secrets` checks before any commit reaches the remote.
- `.env` files are gitignored; use `.env.example` for configuration templates only.
- Any committed secret (even in a branch) must be rotated immediately; do not rely on git history rewriting as the sole remediation.

---

## Contact

| Role | Contact |
|------|---------|
| Security Disclosure | security@thefaulknergroupadvisors.com |
| General Maintainer | John Faulkner — github.com/jsfaulkner86 |
| Organization | [The Faulkner Group](https://thefaulknergroupadvisors.com) |

---

*This policy is reviewed quarterly and updated with each major release. Last reviewed: 2026-05-20.*
