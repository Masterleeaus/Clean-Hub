# Contributing to Clean-Hub

## Principle

Clean-Hub is a large repository with current runtime code, imported/upstream material, extension trees, historical plans, and generated documentation.

A change is complete only when its implementation boundary and verification boundary are clear.

## Read first

Before substantial work, read:

1. `README.md`
2. `docs/README.md`
3. `.titan/docs/AGENTS.md`
4. the canonical architecture documents relevant to the change
5. current source and tests

Do not treat reference documents as proof of runtime behavior.

## Choose the boundary

Identify whether the change affects:

- Titan Zero orchestration
- ToolRouter
- WorkCore actions
- WorkCore reads
- company/tenant context
- permissions/entitlements
- provider integration
- Vault/secrets
- interactions
- frontend/PWA
- finance
- communications
- integrations
- verification tooling
- documentation only

## Local verification

Aim to run:

```bash
composer validate --strict
php tools/titan_verify.php
php tools/titan_namespace_scan.php
php tools/titan_route_provider_scan.php
php tools/titan_migration_order.php

composer install --no-interaction --prefer-dist
composer test:lint
composer test

npm ci
npm run build
```

For Titan AI boundary changes:

```bash
php tests/Standalone/TitanAI/run.php
python3 tests/contracts/titan_zero_source_verification_test.py
```

If the repository's existing CI blockers prevent a full run:

- record the exact command
- record the exact failure
- state what did run
- state what did not run
- do not convert source presence into a passing-test claim

## AI / tool changes

Changes to AI-assisted execution should cover applicable cases:

- ordinary text response
- valid tool envelope
- malformed envelope
- extra envelope fields
- AI-manufactured confirmation
- unknown tool
- tenant override
- missing permission
- missing entitlement
- missing confirmation
- duplicate/replayed request
- handler exception
- safe public error mapping

## WorkCore business action changes

Changes to the action kernel should preserve:

- active tenant consistency
- operation context consistency
- entitlement checks
- permission checks
- confirmation checks
- idempotency
- transactional execution
- audit recording
- domain-event recording

High-impact actions should add targeted negative tests.

## Multi-tenancy

Do not accept client/model-supplied company authority when active company context already exists.

Add cross-company negative cases for new domain queries and mutations.

## Migrations

For migration changes:

- validate creation order
- test fresh migration
- test rollback where supported
- avoid duplicate creation of canonical tables
- keep extension/donor migrations from silently colliding with runtime migrations

## Documentation

Place documents according to `docs/README.md`.

Use:

- `docs/architecture/` for canonical system boundaries
- `docs/audits/` for executed evidence
- `docs/governance/` for policy
- `docs/plans/` for future work
- `docs/reference/` for non-authoritative concepts

## Evidence language

Use these labels consistently:

- **Implemented**
- **Tested**
- **Evaluated**
- **Experimental**
- **Planned**

Do not use them interchangeably.

## Pull-request / commit notes

Even when working directly on `main`, commits should describe:

- what changed
- why
- what was verified
- what remains unverified
- whether behavior, architecture, or documentation changed

## Provenance

Preserve upstream attribution and component-specific licenses.

Do not describe imported or donor code as original repository-local implementation without evidence.
