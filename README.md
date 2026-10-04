![Clean-Hub — Laravel AI business workspace with Titan orchestration and WorkCore-governed business actions](docs/images/clean-hub-banner.svg)

<div align="center">

# Titan Zero Cleaning Platform Recovery Lab

**Titan Zero cleaning-platform development and branch-recovery workspace.**

</div>

## Product architecture and engineering highlights

<p align="center">
  <img src="docs/images/clean-hub-architecture.svg" alt="Clean-Hub governed business-action path from TitanZeroOrchestrator through ToolRouter and WorkCoreActionController to BusinessActionDispatcher, with permission, confirmation, idempotency, and audit boundaries." width="100%" />
</p>

A branch-recovery and source-integrity workspace for complex Titan Zero development histories.

- **Architecture:** Its recovery flow scans branches, identifies repeated implementations, builds a recovery plan, replays selected commits, validates the result, and emits review reports.
- **Distinctive engineering:** The distinctive focus is controlled recovery of valuable work from fragmented branches rather than ordinary feature development.

> **Status: development repository.** This repository contains a substantial Laravel codebase and branch recovery tooling. The repository name is generic, so its relationship to the current Titan Zero platform is documented here to prevent it being mistaken for the canonical product.

## Purpose

The repository contains cleaning-platform development work and a Titan Zero branch recovery system. The recovery system scans branches, detects duplicate implementations, plans recovery, replays commits, validates merges, and generates reports.

For the current TypeScript field-service product, see [Titan Zero Field Service Workforce](https://github.com/Masterleeaus/Titan-Zero-Field-Service-Workforce). Keep this repository as a historical or experimental source only where its code has a documented migration or maintenance purpose.

## Current evidence

- Primary language: PHP
- Default branch: `main`
- Implementation summary: [Titan system implementation summary](TITAN_SYSTEM_IMPLEMENTATION_SUMMARY.md)
- Repository has active issue tracking; resolve or migrate useful work before archiving.
- No release or production deployment was independently verified during this portfolio review.

## Development

Inspect the repository's Composer manifests and CI workflows before installing or running the Laravel application. Use a local environment file and never commit credentials or customer data.

### Runnable branch-recovery tooling

The root `package.json` exposes the recovery pipeline as local Node.js commands. They inspect the Git refs available in the checkout and write reports under `.titan/`:

```bash
npm install
npm run titan:scan
npm run titan:detect-duplicates
npm run titan:plan -- <source-branch>
npm run titan:validate -- <branch>
npm run titan:report
```

The implementation is in [`.titan/scripts/`](.titan/scripts/) and the design/index is [`.titan/README.md`](.titan/README.md). The validator now fails on an unsuccessful build or test command and marks duplicate, import, and architecture checks as `not_run` because those checks are not implemented in that script. Treat its result as review evidence, not an automatic merge approval.

The Laravel application's Composer test and lint scripts are present in [`composer.json`](composer.json), but they were not executed as part of this README change.

## Portfolio status

**Candidate for predecessor/archive classification.** Compare this repository with `cleanly`, `modules`, `Titan-BOS`, and the current workforce monorepo before deciding whether to retain it as an independent project or archive it.

## Banner

A checked-in project-specific banner is displayed above.

