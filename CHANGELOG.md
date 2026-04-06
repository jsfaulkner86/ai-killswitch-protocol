# Changelog

All notable changes to the AI Kill Switch Protocol will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-04-06

### Added
- Initial protocol core: `killswitch-policy.yaml`, `escalation-tiers.md`, `override-procedures.md`, `reinstatement-checklist.md`
- Agent layer: manifest, watchdog, circuit breaker, state schema, confidence thresholds
- Digital twin layer: manifest, drift detection, FHIR sync validator, twin state schema, simulation guard
- Integration layer: Epic webhook listener, FHIR R4 client, IoT stream validator, alert dispatcher
- Governance layer: audit log schema, RBAC definitions, incident response template, data retention policy
- Documentation: architecture overview, threat taxonomy, compliance mapping, glossary
- Test suite: circuit breaker, drift detection, FHIR validator unit tests with mock fixtures
