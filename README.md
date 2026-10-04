![Clean-Hub — governed AI business operations over a company-scoped WorkCore action kernel](docs/images/clean-hub-banner.svg)

<div align="center">

# Clean-Hub

**A Laravel AI business workspace that lets conversational workflows reach real operational actions only through company scope, permissions, confirmation, idempotency, transactions, audit records, and domain events.**

*Engineering focus: governed AI execution over ordinary business software boundaries.*

[![Repository Baseline](https://github.com/Masterleeaus/Clean-Hub/actions/workflows/repository-baseline.yml/badge.svg)](https://github.com/Masterleeaus/Clean-Hub/actions/workflows/repository-baseline.yml)
[![Laravel CI](https://github.com/Masterleeaus/Clean-Hub/actions/workflows/ci-laravel.yml/badge.svg)](https://github.com/Masterleeaus/Clean-Hub/actions/workflows/ci-laravel.yml)
[![Titan Zero Verification](https://github.com/Masterleeaus/Clean-Hub/actions/workflows/titan-zero-verify.yml/badge.svg)](https://github.com/Masterleeaus/Clean-Hub/actions/workflows/titan-zero-verify.yml)
![PHP](https://img.shields.io/badge/PHP-8.2%2B-777BB4?logo=php&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-10-FF2D20?logo=laravel&logoColor=white)

[Architecture](docs/architecture/PORTFOLIO_SYSTEM_OVERVIEW.md) · [Evaluation](docs/audits/PORTFOLIO_EVALUATION.md) · [Documentation](docs/README.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

</div>

---

## Overview

Clean-Hub combines a conversational AI layer with WorkCore business domains for customers, properties, workforce, scheduling, service operations, finance, and field workflows.

The important engineering distinction is **where AI stops**.

A model can propose a registered tool call, but business writes still cross ordinary deterministic software boundaries:

- active company context
- capability / action registration
- entitlement checks
- actor permissions
- explicit confirmation
- idempotency
- database transaction
- audit recording
- domain-event recording

> **Core principle:** the model may propose work; the application remains authoritative for whether that work is allowed to happen.

---

## Measured evidence

The first screen intentionally separates source evidence from runtime claims.

| Evidence | Verified state | Reproduce / inspect |
| --- | --- | --- |
| Strict AI tool envelope | Only exactly `tool`, `arguments`, and `confirmation_id` are accepted; model-generated confirmation IDs are rejected | `app/Titan/AI/TitanZeroOrchestrator.php` |
| Standalone Titan AI contract checks | **8 assertions present** for envelope parsing, confirmation rejection, tenant override rejection, and message normalisation | `tests/Standalone/TitanAI/run.php` |
| Tenant override protection | Recursive `company_id` / `companyId` input is rejected before tool execution | `app/Titan/AI/ToolRouter.php` |
| Governed write boundary | Entitlement, permission, confirmation, idempotency, transaction, audit and event checks are implemented in one dispatcher | `BusinessActionDispatcher.php` |
| Provider completion paths | **5 text provider paths** in `AiCompletionService`: OpenAI, Anthropic, Gemini, DeepSeek, xAI | `app/Services/Ai/AiCompletionService.php` |
| Source verifier regression tests | **2/2 passed** in reviewed PR CI run #70 before the next source-contract check failed | workflow run 37176822035 |
| Titan architecture verifier | **42,917 passed / 15 failed** = **42,932 checks executed** in reviewed Laravel CI run #40 | workflow run 37176822034 |
| Frontend dependency install | `npm ci` completed: **608 packages** installed | workflow run 37176822034 |
| Frontend audit reported by npm | **39 vulnerabilities**: 2 low, 4 moderate, 33 high | workflow run 37176822034 |
| Full application CI | **Red / not claimed as passing** | see [Evaluation](docs/audits/PORTFOLIO_EVALUATION.md) |
| Repository-level AI benchmark | **Not established** | see [Evaluation](docs/audits/PORTFOLIO_EVALUATION.md) |

### Current CI blockers from executed runs

The latest reviewed PR evidence identified concrete failures:

- source-verifier plan-path drift was repaired on `main`; the next CI run must confirm the canonical archived plan path
- the baseline now explicitly permits deterministic `.env.testing` / `.env.verification` APP keys while still rejecting production-style tracked keys
- `composer.lock` still does not satisfy the current `phpoffice/phpspreadsheet ^5.8` constraint
- the root Vite config was realigned to the existing Tailwind 3/PostCSS stack; the next CI run must confirm the frontend build
- Titan architecture verification still reports **15 remaining failures** in the last executed run

These are repository facts, not hidden caveats.

---

# What Is New

## Governed AI → business-action boundary

Clean-Hub's strongest repository-specific mechanism is the path from conversational AI to deterministic business execution.

```text
User conversation
       │
       ▼
TitanZeroOrchestrator
       │
       │ strict JSON tool envelope only
       ▼
ToolRouter
       │
       ├──── reject tenant/company override
       ├──── registered capability
       ├──── registered WorkCore action
       └──── registered WorkCore read model
                 │
                 ▼
        BusinessActionDispatcher
                 │
       ┌─────────┼─────────────┬───────────────┐
       ▼         ▼             ▼               ▼
   tenant     entitlement   permission     confirmation
   context
       │
       ▼
   idempotency replay check
       │
       ▼
   database transaction
       │
       ├──── handler
       ├──── domain events
       ├──── audit record
       └──── idempotency completion
```

### Why it matters

**AI does not become authority.** The LLM cannot grant itself company scope or manufacture an explicit confirmation token.

**Retries are designed into the action contract.** Each action request carries an idempotency key, while the dispatcher supports replay of already-completed work.

**Operational state remains inspectable.** Successful actions return correlation, audit and event evidence rather than existing only inside conversation text.

**Direct and AI-assisted operations can converge on the same kernel.** WorkCore policy does not need to trust where the request originated.

### Implementation

```text
app/Titan/AI/
├── TitanZeroOrchestrator.php
├── ToolRouter.php
└── ConversationContextBuilder.php

app/Domains/WorkCore/System/Actions/
├── BusinessActionDispatcher.php
├── BusinessActionRegistry.php
├── ActionRequest.php
├── ActionResult.php
└── Contracts/
```

### Current boundary

This mechanism is implemented in source and has focused structural/standalone checks. The repository does **not yet publish a full adversarial benchmark** proving every registered tool and action obeys these invariants under every failure condition.

---

## Strict tool-envelope separation

The orchestrator does not interpret arbitrary prose as an action.

For ordinary assistant output:

```text
"Your next cleaning visit is Tuesday."
          │
          ▼
ordinary conversation result
```

For executable work, the model must return exactly:

```json
{
  "tool": "registered.tool.id",
  "arguments": {},
  "confirmation_id": null
}
```

The parser rejects:

- malformed JSON
- extra fields
- blank tool IDs
- non-object arguments
- any model-supplied non-null confirmation ID

That last rule is important: **confirmation comes from the application/user workflow, not from the model.**

Focused standalone source tests include:

```text
✓ valid envelope in arbitrary JSON key order
✓ reject extra envelope fields
✓ reject AI-manufactured confirmation
✓ ordinary text is not a tool call
✓ reject nested company_id override
✓ reject companyId override
✓ preserve legitimate non-tenant identifiers
✓ discard invalid AI message roles
```

---

## Company-scoped provider configuration

Clean-Hub also contains a separate company-aware assistant service.

`AIAssistantService`:

- resolves the active company
- reads company AI settings
- resolves provider credentials through the application Vault
- requires HTTPS endpoints
- enforces an allowed-host list
- normalises message roles
- limits context/message sizes
- converts provider failures into safe public error codes
- avoids exposing raw provider exceptions to the user

The currently supported assistant configuration path is narrower than the general-purpose completion service: it supports configured **OpenAI/OpenRouter-format** and **Gemini** providers.

The lower-level `AiCompletionService` additionally contains text adapters for:

- OpenAI
- Anthropic
- Gemini
- DeepSeek
- xAI

and image-aware paths for OpenAI, Anthropic and Gemini.

These two layers serve different parts of the current codebase; this README does not pretend they are already one fully consolidated provider abstraction.

---

# Verified Capabilities

| Capability | Implemented | Focused test / verifier evidence | Evaluated |
| --- | :---: | :---: | :---: |
| Titan Zero conversation orchestration | ✓ | ✓ | — |
| Strict tool-envelope parsing | ✓ | ✓ | — |
| Tenant override rejection | ✓ | ✓ | — |
| Registered capability routing | ✓ | structural verifier | — |
| WorkCore action routing | ✓ | structural verifier | — |
| WorkCore read routing | ✓ | structural verifier | — |
| Permission checks | ✓ | structural / domain tests present | — |
| Explicit confirmation boundary | ✓ | focused assertion present | — |
| Idempotent action dispatch | ✓ | source/test evidence present | — |
| Transactional action handling | ✓ | source-backed | — |
| Audit + domain event recording | ✓ | source-backed | — |
| Multi-provider completion | ✓ | partial | — |
| Company Vault-backed assistant credentials | ✓ | structural verifier | — |
| Full green CI | — | **No** | — |
| AI/tool safety benchmark | — | — | **No** |

**Implemented**, **tested**, **evaluated**, and **production-ready** are not interchangeable.

---

# Example

The primary example is the governed action path.

A model response may request:

```json
{
  "tool": "crm.customer.create",
  "arguments": {
    "name": "Example Customer"
  },
  "confirmation_id": null
}
```

The model does **not** provide company authority.

The application supplies:

```text
active company
authenticated actor
conversation ID
explicit confirmation from workflow, if required
idempotency key
correlation ID
```

Then the business action can either:

```text
ALLOW
  ↓
transaction → handler → events → audit → idempotency complete
```

or fail before mutation because of:

```text
tenant mismatch
entitlement denied
permission denied
confirmation missing
unregistered action
invalid handler
execution failure
```

That is the core engineering proposition of Clean-Hub.

---

# Installation and Quick Start

## Requirements

- PHP **8.2+**
- Composer
- Node.js + npm
- a Laravel-supported database

## Install

```bash
git clone https://github.com/Masterleeaus/Clean-Hub.git
cd Clean-Hub

composer install --no-interaction --prefer-dist
cp .env.example .env
php artisan key:generate
php artisan migrate

npm ci
npm run build
```

## Verify architecture contracts

```bash
php tools/titan_verify.php
php tools/titan_namespace_scan.php
php tools/titan_route_provider_scan.php
php tools/titan_migration_order.php
```

## Run focused Titan AI checks

```bash
php tests/Standalone/TitanAI/run.php
```

## Test

```bash
composer test
composer test:lint
```

### Current reproducibility boundary

A clean clone → install → build → test path is **not currently proven green** by CI.

The exact blockers and latest executed evidence are documented in [docs/audits/PORTFOLIO_EVALUATION.md](docs/audits/PORTFOLIO_EVALUATION.md).

---

# Reproducible Evaluation

Clean-Hub already has substantial verification machinery, but it does not yet have a portfolio-quality evaluation proving the contribution of the governed AI boundary.

## Current executed evidence

### Titan Zero Source Verification — run #70

- source-verifier regression tests: **2/2 passed**
- required-source verification: failed because `TITAN_ZERO_CHATBOT_PWA_UPGRADE_PLAN.md` is missing
- later checks were skipped after that failure

### Repository Baseline — run #62

Source-integrity checks passed until the populated APP-key rule found:

```text
.env.testing
.env.verification
```

The PHP baseline independently failed because `composer.lock` is stale relative to the current `phpoffice/phpspreadsheet ^5.8` requirement.

### Laravel CI — run #40

The architecture verifier completed:

```text
Titan verification: 42917 passed, 15 failed
```

The frontend job completed `npm ci`, then failed because:

```text
Cannot find module '@tailwindcss/vite'
```

Composer validation failed before the install/test jobs could proceed, so the main Unit/Feature/Architecture suite and migration validation were skipped.

## Evaluation target: governed-action effectiveness

The future portfolio evaluation should directly test the repository's distinctive mechanism.

| Scenario | Expected outcome |
| --- | --- |
| valid registered action + permission | execute |
| missing entitlement | reject |
| missing permission | reject |
| confirmation-required action without confirmation | reject |
| AI-manufactured confirmation | reject before dispatch |
| nested company override | reject before dispatch |
| actor/company mismatch | reject |
| operation-context mismatch | reject |
| repeated idempotency key | replay safe result |
| handler failure | transaction rollback + failed audit/idempotency state |
| unknown tool | reject |
| read-only tool | no write mutation |

### Metrics

- unauthorized mutation rate
- valid-action success rate
- tenant-override rejection rate
- confirmation-bypass rate
- idempotent replay correctness
- failed-action rollback correctness
- audit/event evidence completeness

### Ablation

Compare:

1. **governed path** — Orchestrator → ToolRouter → BusinessActionDispatcher
2. **direct handler path** — same scenario dataset without the policy/confirmation/idempotency boundary

The goal is not to show that the governed system is “more intelligent.” It is to quantify how much the boundary reduces unsafe or invalid state mutation.

Detailed methodology: [docs/audits/PORTFOLIO_EVALUATION.md](docs/audits/PORTFOLIO_EVALUATION.md).

---

# Known Limitations

1. **CI is currently red.** Do not interpret the badges as passing certification.

2. **Composer metadata is inconsistent.** The current lock file contains `phpoffice/phpspreadsheet 4.5.0`, which does not satisfy the root `^5.8` constraint.

3. **The previous frontend build failure was caused by a Tailwind 4 Vite plugin import in a Tailwind 3/PostCSS project.** The root Vite config has been corrected on `main`; a fresh CI run is still required.

4. **The source-verification workflow previously referenced a missing root-level historical plan.** It now targets the canonical archived plan path; a fresh CI run is still required.

5. **The deterministic test APP keys are intentional fixtures.** The baseline rule now excludes `.env.testing` and `.env.verification` while continuing to reject other tracked populated APP keys.

6. **Titan architecture verification still has 15 failures**, including unresolved WorkCore module wiring, route/company-scope checks and missing gitignore protections.

7. **Provider abstractions are not fully consolidated.** `AIAssistantService` and `AiCompletionService` expose overlapping but different provider sets and contracts.

8. **No project-level adversarial tool/action benchmark is currently published.**

9. **The optional AI site-builder bridge is an integration surface, not evidence of a deployed production capability.**

10. **The repository contains upstream MagicAI/Laravel material and large imported/reference trees.** Provenance should remain explicit.

---

# Testing

The repository contains several different verification layers:

```text
tests/
├── Unit/
├── Feature/
├── Architecture/
├── Standalone/
│   └── TitanAI/
└── contracts/
```

The main Laravel workflow intends to run:

```text
Composer validation
        │
        ├──── Titan architecture tools
        │
        ├──── install + Pint
        │       └──── Unit / Feature / Architecture tests
        │
        ├──── SQLite migration / rollback / remigrate
        │
        └──── npm ci → Vite build
```

The current pipeline stops before the full test stage because earlier gates are failing.

That is useful evidence: it shows exactly what must be repaired before the repository can claim reproducible application health.

---

# System Behaviour

## Conversational path

```text
conversation
    │
    ▼
company-scoped context
    │
    ▼
configured assistant
    │
    ├──── ordinary text ─────► conversation result
    │
    ▼
strict tool envelope
    │
    ▼
ToolRouter
```

## Write path

```text
ToolRouter
    │
    ▼
BusinessActionDispatcher
    │
    ├─ tenant context
    ├─ operation context
    ├─ entitlement
    ├─ permission
    ├─ explicit confirmation
    └─ idempotency
          │
          ▼
      transaction
          │
          ├─ handler
          ├─ events
          ├─ audit
          └─ completion record
```

## Failure path

```text
invalid / unauthorized request
         │
         ▼
safe application error
         │
         ├─ failure audit where available
         └─ no silent model-authorized mutation
```

---

# Architecture

<p align="center">
  <img src="docs/images/clean-hub-architecture.svg" alt="Clean-Hub governed business action path from TitanZeroOrchestrator through ToolRouter to BusinessActionDispatcher with permission, confirmation, idempotency and audit boundaries." width="100%" />
</p>

```text
┌─────────────────────────────────────────────────────────────┐
│                 USER / APPLICATION REQUEST                  │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              COMPANY-SCOPED CONVERSATION CONTEXT            │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   TITAN ZERO ORCHESTRATOR                   │
│             plain text OR strict tool envelope              │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                       TOOL ROUTER                           │
│ capability · action · read model · tenant override guard   │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                WORKCORE BUSINESS ACTION KERNEL              │
│ tenant · entitlement · permission · confirmation           │
│ idempotency · transaction · audit · domain events          │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                CONTROLLED BUSINESS STATE CHANGE             │
└─────────────────────────────────────────────────────────────┘
```

Detailed architecture: [docs/architecture/PORTFOLIO_SYSTEM_OVERVIEW.md](docs/architecture/PORTFOLIO_SYSTEM_OVERVIEW.md)

---

# Reliability Engineering

The action boundary contains several concrete reliability mechanisms:

- idempotency replay before execution
- idempotency reservation inside the transaction
- database transaction with retry count
- completion state after successful execution
- failure state recording on exceptions
- correlation IDs
- causation IDs for events
- completed and failed audit records
- safe public error mapping at the ToolRouter boundary

These mechanisms do not guarantee production reliability by themselves. They make failure and replay **design concerns in the code**, rather than afterthoughts.

---

# Safety & Authority

Clean-Hub's most important safety invariant is:

> **Model intelligence and execution authority are different things.**

```text
AI intent
  ↓
registered tool
  ↓
active company
  ↓
entitlement
  ↓
permission
  ↓
confirmation
  ↓
idempotency
  ↓
transactional execution
```

The model cannot legitimately expand its authority by adding `company_id` to arguments or inventing a confirmation identifier.

Security-sensitive registered actions should continue to enforce authorization inside the deterministic application layer even if future model capabilities improve.

---

# Observability

The current action path includes identifiers and records useful for reconstruction:

- conversation ID
- company ID
- actor/user ID
- tool/action ID
- correlation ID
- causation ID
- audit record
- domain-event IDs
- idempotency record
- success/failure state

A future improvement is to standardise one trace ID across AI provider calls, tool routing, action dispatch, queues and external integrations.

---

# Continuous Integration

Three workflows are particularly relevant to portfolio evidence.

## Repository Baseline

Checks:

- required application files
- tracked secret/runtime files
- obvious populated Laravel keys
- destructive workflow patterns
- Composer metadata
- PHP syntax
- local Composer path packages

## Titan Zero Source Verification

Checks:

- verifier regression tests
- required source/JSON
- host registration contracts
- PHP syntax
- Composer metadata
- Interaction Engine standalone tests
- shell syntax

## Laravel CI

Checks:

- strict Composer validation
- Titan architecture verifier
- namespace scan
- route/provider scan
- migration-order scan
- dependency install
- Pint
- Unit / Feature / Architecture tests
- Laravel boot
- SQLite migrate / rollback / remigrate
- frontend build

The pipeline is broad; the repository's current job is to make those gates green rather than lower them.

---

# Security

Security-relevant design areas include:

- company/tenant isolation
- AI tool authority
- Vault-backed provider credentials
- allowed provider hosts
- explicit confirmations
- business-action permissions
- idempotency/replay
- financial operations
- file/document access
- external integrations
- audit evidence

See [SECURITY.md](SECURITY.md).

---

# Project Status

| Area | Status |
| --- | --- |
| Titan Zero orchestrator | 🟢 Implemented |
| Strict tool envelope | 🟢 Implemented + focused checks |
| Tenant override guard | 🟢 Implemented + focused checks |
| ToolRouter | 🟢 Implemented |
| WorkCore business-action dispatcher | 🟢 Implemented |
| Confirmation boundary | 🟢 Implemented |
| Idempotency boundary | 🟢 Implemented |
| Audit + domain events | 🟢 Implemented |
| Provider completion adapters | 🟢 Implemented |
| Architecture verifier | 🟡 Active — 15 failures remain |
| Source verification | 🔴 Red |
| Repository baseline | 🔴 Red |
| Laravel CI | 🔴 Red |
| Frontend build | 🔴 Red |
| Adversarial governed-action evaluation | ⚪ Not yet established |
| Production certification | ⚪ Not claimed |

---

# Why This Exists

An ordinary LLM integration answers:

> “Can the model call a function?”

Clean-Hub is more interested in:

> **“What deterministic software boundaries must still hold when the model can call a function?”**

The current answer encoded in the repository is:

1. model output must match a narrow tool contract
2. company authority comes from application context
3. tools must be registered
4. actions pass through entitlements and permissions
5. sensitive actions require explicit confirmation
6. retries are handled through idempotency
7. writes execute transactionally
8. outcomes produce audit and domain-event evidence

That governed transition from **language → tool request → authorized business state** is the repository's strongest technical contribution.

---

# Repository Structure

```text
Clean-Hub/
├── app/
│   ├── Titan/
│   │   ├── AI/
│   │   ├── Audit/
│   │   ├── Capabilities/
│   │   ├── Permissions/
│   │   ├── Tenancy/
│   │   └── Vault/
│   ├── Domains/
│   │   └── WorkCore/
│   └── Services/
│       ├── AI/
│       └── AIAssistantService.php
├── interactions/                  # declarative interaction definitions
├── integrations/
│   └── ai-site-builder/           # isolated optional integration
├── packages/
│   └── titanzero/
├── tests/
│   ├── Unit/
│   ├── Feature/
│   ├── Architecture/
│   ├── Standalone/
│   └── contracts/
├── tools/                         # architecture / integrity verification
├── docs/
│   ├── architecture/
│   ├── audits/
│   ├── governance/
│   ├── inventory/
│   └── README.md
├── .github/workflows/
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── composer.json
└── package.json
```

---

# Design Decisions

## Why reject company IDs from tool arguments?

Because the company/tenant boundary should come from authenticated application context, not from model-generated input.

## Why reject model-generated confirmation?

Because confirmation represents user/application authority. Allowing a model to manufacture it would collapse the distinction between recommendation and authorization.

## Why put idempotency inside the dispatcher?

Because retries can occur regardless of whether the request came from AI, HTTP, queues or another system. Safe replay belongs at the business-action boundary.

## Why record domain events and audit records?

Because the important output is not just what the assistant said—it is what business state changed, who caused it, and what evidence remains.

## Why keep provider code behind services?

Because provider selection should be replaceable without giving provider-specific SDK behavior authority over application policy.

---

# Technology

| Area | Technology |
| --- | --- |
| Backend | PHP 8.2+, Laravel 10 |
| Testing | Pest / PHPUnit + standalone PHP/Python contract tests |
| AI providers | OpenAI, Anthropic, Gemini, DeepSeek, xAI; company assistant path also supports OpenRouter-style API |
| Auth | Laravel Passport / Sanctum surfaces |
| Frontend | Vite, Tailwind, Alpine-related tooling, React dependencies for selected surfaces |
| Realtime | Laravel Echo / Pusher-related tooling |
| Storage | Laravel/Flysystem-compatible storage |
| CI | GitHub Actions |
| Architecture verification | repository-local PHP/Python/shell tools |

---

# Performance

No p50/p95/p99 latency, throughput, provider-cost or tool-execution benchmark is currently published.

Future performance results should include:

- commit SHA
- runtime version
- provider/model
- scenario dataset
- test environment
- sample size
- reproduction command
- raw or machine-readable result artifact

---

# Model & Provider Support

| Provider path | Source implementation | Evaluated equivalence |
| --- | :---: | :---: |
| OpenAI | ✓ | — |
| Anthropic | ✓ | — |
| Gemini | ✓ | — |
| DeepSeek | ✓ | — |
| xAI | ✓ | — |
| OpenRouter-style company assistant | ✓ | — |

Provider source presence is not the same as provider conformance testing.

---

# Roadmap

## Immediate

- [ ] resolve Composer lock / `phpoffice/phpspreadsheet` mismatch
- [ ] add or remove the stale source-verifier requirement for `TITAN_ZERO_CHATBOT_PWA_UPGRADE_PLAN.md`
- [ ] remove populated tracked APP keys or explicitly redesign the baseline rule for test fixtures
- [ ] restore the `@tailwindcss/vite` frontend dependency contract
- [ ] resolve the remaining 15 Titan verifier failures
- [ ] get Repository Baseline green
- [ ] get Titan Zero Source Verification green
- [ ] get Laravel CI and frontend build green

## Next

- [ ] add executable BusinessActionDispatcher adversarial scenarios
- [ ] measure confirmation bypass rate
- [ ] measure tenant-override rejection rate
- [ ] verify idempotent replay across representative writes
- [ ] test transaction rollback and audit evidence after handler failures
- [ ] add cross-provider conformance fixtures

## Later

- [ ] latency / provider-cost measurements
- [ ] end-to-end trace IDs
- [ ] feature ablation of governed vs direct action execution
- [ ] deployment smoke tests

Roadmap items are intentions, not existing capabilities.

---

# Engineering Principles

### Evidence over claims

Source paths, executed tests, CI logs and reproducible commands outrank product language.

### AI does not grant authority

A model can identify or propose an action. Authorization remains application code.

### Deterministic controls around probabilistic systems

Company scope, permissions, confirmation, idempotency and transactions should not depend on model compliance.

### Failure should leave evidence

Failed dispatch, denied authorization and replay behavior should remain observable.

### One business-action boundary

AI-assisted writes and direct application writes should converge on the same policy kernel wherever practical.

### Honest scope

A source-present integration is not automatically a deployed or evaluated capability.

---

# Documentation

The repository already maintains a structured documentation library.

Start with:

- [docs/README.md](docs/README.md)
- [Portfolio architecture overview](docs/architecture/PORTFOLIO_SYSTEM_OVERVIEW.md)
- [Portfolio evaluation](docs/audits/PORTFOLIO_EVALUATION.md)
- [Authority map](docs/architecture/TITAN_ZERO_AUTHORITY_MAP.md)
- [Tenancy, trust and action execution](docs/architecture/TENANCY_TRUST_AND_ACTION_EXECUTION.md)
- [SECURITY.md](SECURITY.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

Historical and reference documents do not become implementation evidence merely because they are detailed or labelled “canonical.”

---

# Contributing

Before submitting changes, aim to run:

```bash
composer validate --strict
php tools/titan_verify.php
php tools/titan_namespace_scan.php
php tools/titan_route_provider_scan.php
php tools/titan_migration_order.php

composer test
composer test:lint

npm ci
npm run build
```

For AI/business-action changes, also run:

```bash
php tests/Standalone/TitanAI/run.php
```

If an existing repository blocker prevents full verification, report the exact failing command and distinguish targeted verification from full-suite verification.

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

# Responsible Use

This repository is not evidence that autonomous AI execution is safe in financial, employment, compliance, medical, safety-critical or other high-impact domains.

Human review, domain authorization, access controls, tenant isolation, credential management and deployment-specific safeguards may still be required.

---

# Provenance & Licensing

Clean-Hub contains upstream MagicAI/Laravel application material alongside Titan Zero, WorkCore, imported packages, extension trees and repository-local integration work.

The root Composer manifest declares MIT, but there is currently no single root `LICENSE` file establishing uniform provenance for every retained component.

Before redistribution:

- preserve upstream notices
- inspect package-specific licenses
- distinguish imported material from repository-local implementation
- avoid treating donor/reference trees as original work

---

# Author

**Jason Lee / Masterleeaus**

Focus: **AI systems · governed agent execution · business operating systems · evaluation · reliability**

---

<div align="center">

### Clean-Hub

**AI can propose the action. The application decides whether it happens.**

Built around a governed mechanism that can be inspected, tested and challenged.

</div>
