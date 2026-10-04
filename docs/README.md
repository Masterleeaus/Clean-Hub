# Titan Zero Documentation

This directory is the canonical human project-documentation library. It separates current engineering guidance from evidence, historical records and the extracted Titan reference library.

Titan Agent OS has a second complementary documentation tree at [`/.titan/documentation`](../.titan/documentation/README.md). That layer serves agent onboarding, generated system views, status, progress, decisions, reviews, learning, dashboards, visualisations, history and the Project Chronicle. The two trees must not become competing manually maintained sources of truth.

## Mandatory reading for every agent

Before changing code or documentation, read:

1. the root [`README.md`](../README.md);
2. [`AGENTS.md`](../.titan/docs/AGENTS.md);
3. [`.titan/README.md`](../.titan/README.md);
4. [`.titan/MANDATE.md`](../.titan/MANDATE.md) when acting as Claude or architecture authority;
5. the [Agent OS current status](../.titan/documentation/status/current.md);
6. this file;
7. every canonical document listed below;
8. every document in the subject cluster affected by the work;
9. current source, tests and runtime wiring.

New long-form project documentation belongs under `/docs`, not at the repository root. Agent OS-native status, decisions, reviews, lessons, generated views and Chronicle records belong under `/.titan/documentation`.

## Start here

Portfolio evidence entry points:

- [Portfolio system architecture](architecture/PORTFOLIO_SYSTEM_OVERVIEW.md)
- [Portfolio evaluation and current CI evidence](audits/PORTFOLIO_EVALUATION.md)

1. [Agent working agreement](../.titan/docs/AGENTS.md)
2. [Titan Agent OS](../.titan/README.md)
3. [Claude Architecture Authority mandate](../.titan/MANDATE.md)
4. [Current upgrade plan](plans/CURRENT_UPGRADE_PLAN.md)
5. [Canonical authority map](architecture/TITAN_ZERO_AUTHORITY_MAP.md)
6. [Tenancy, trust and governed action execution](architecture/TENANCY_TRUST_AND_ACTION_EXECUTION.md)
7. [Interaction Engine, Wizard and five-tier intelligence architecture](architecture/INTERACTION_WIZARD_AND_FIVE_TIER_INTELLIGENCE.md)
8. [PWA, offline runtime and Chatbot extension architecture](architecture/PWA_OFFLINE_AND_CHATBOT_EXTENSION_ARCHITECTURE.md)
9. [Extension platform, manifest and lifecycle architecture](architecture/EXTENSION_PLATFORM_AND_LIFECYCLE_ARCHITECTURE.md)
10. [Documentation policy](governance/DOCUMENTATION_POLICY.md)
11. [Documentation reconciliation status](DOCUMENTATION_RECONCILIATION_STATUS.md)

## Two documentation systems

| Tree | Purpose | Editing authority |
|---|---|---|
| `/docs` | Human-authored canonical architecture, governance, plans, audits, provenance, setup, reference and history | Humans and authorised agents |
| `/.titan/documentation` | Agent onboarding, system-generated views, status, progress, decisions, reviews, learning, dashboards, visualisations and Chronicle | Control plane, authorised agents and generators according to section policy |

A `.titan` derived view identifies its canonical `/docs` source and source commit. Do not copy a document into both trees and maintain both manually.

## Evidence and provenance

- [MagicAI v11.00 import audit](audits/magicai-v1100-source-inventory.md)
- [Pass 1 dispositions](inventory/PASS1_DISPOSITIONS.md)
- [Pass 2 architecture consolidation](inventory/PASS2_ARCHITECTURE_CONSOLIDATION.md)
- [Root document consolidation](inventory/ROOT_DOCUMENT_CONSOLIDATION.md)
- [Interaction, Wizard and five-tier runtime inventory](inventory/INTERACTION_INTELLIGENCE_RUNTIME_INVENTORY.md)
- [PWA, offline and Chatbot extension runtime inventory](inventory/PWA_OFFLINE_RUNTIME_INVENTORY.md)
- [Extension platform runtime inventory](inventory/EXTENSION_PLATFORM_INVENTORY.md)
- [Extension registry gaps](inventory/EXTENSION_PLATFORM_GAPS.md)
- `inventory/archive_inventory.json` records the two uploaded archive contents and hashes.
- `inventory/documentation_catalogue.json` is the generated Pass 1 catalogue snapshot.
- `inventory/root_document_moves.json` records documentation moved from the repository root.
- `inventory/INTERACTION_INTELLIGENCE_RUNTIME_INVENTORY.json` contains the file-level Pass 3 evidence.
- `inventory/PWA_OFFLINE_RUNTIME_INVENTORY.json` contains the file-level Pass 4 evidence.
- `inventory/EXTENSION_PLATFORM_INVENTORY.json` contains the per-extension Pass 5 evidence.
- [Agent OS documentation source registry](../.titan/registry/documentation.yaml) maps canonical and reference sources into Agent OS views.

## Where agents add documentation

| Change type | Destination |
|---|---|
| Canonical architecture or system boundaries | `docs/architecture/` |
| Current implementation or upgrade plan | `docs/plans/` |
| Security, engineering or documentation policy | `docs/governance/` |
| Verified audit or test evidence | `docs/audits/` |
| Source origins, checksums or import decisions | `docs/provenance/` |
| Generated catalogues, comparisons and disposition registers | `docs/inventory/` |
| Installation, operations or deployment guidance | `docs/setup/` or an appropriate current operations folder |
| Superseded plans, status reports and obsolete setup material | `docs/archive/` after unique information is preserved |
| Doctrine, proposals, product concepts and unverified blueprints | `docs/reference/titan-library/` |
| Agent onboarding and journals | `.titan/documentation/agents/` |
| Current Agent OS status and progress projections | `.titan/documentation/status/` and `.titan/documentation/progress/` |
| Durable decisions, reviews and learning | `.titan/documentation/decisions/`, `reviews/` and `learning/` |
| Generated Agent OS documentation | `.titan/documentation/system/` — generator-owned, not manually edited |
| Project Chronicle | `.titan/documentation/chronicle/` |

Do not add project plans, status files, architecture notes, audit reports or provenance records to the repository root. The root documentation entry points are `README.md` and `AGENTS.md`; the Agent OS entry points live inside `.titan/`.

## Directory guide

| Directory | Purpose | Authority |
|---|---|---|
| `architecture/` | Current source-backed boundaries, trust and ownership | Canonical when linked above |
| `plans/` | Current coordinated implementation plan | Current guidance |
| `governance/` | Documentation, security and engineering rules | Canonical policy |
| `audits/` | Evidence-based findings and verification | Evidence |
| `provenance/` | Source origins, checksums and import decisions | Evidence |
| `inventory/` | Documentation catalogues, cluster reviews and dispositions | Generated/review evidence |
| `reference/titan-library/` | Extracted doctrine, blueprints, proposed architecture and product concepts | Reference-only |
| `archive/` | Superseded plans, branch reports and old setup instructions | Historical only |

## Authority rule

A reference document does not become current merely because it says `canonical`, `final`, `locked`, has a newer-looking filename or is larger than another file. Current authority requires alignment with accepted ownership boundaries, current source paths, connected runtime behaviour and verification evidence.

Planned, source-present, partially wired and operational are different states. Documentation must state the evidence-supported state precisely.

## Reconciliation progress

- Pass 1: archives extracted, exact duplicates removed and historical records separated.
- Pass 2: ownership, tenancy, trust and action execution consolidated into source-backed canonical documents.
- Pass 3: Interaction Engine, WorkCore Wizards and five-tier intelligence inventoried; one metadata-only duplicate package root removed; canonical runtime roles established; connected Interaction Engine activation remains unverified.
- Pass 4: complete Chatbot extension trees and offline runtimes inventoried; primary Chatbot established as canonical intended extension; secondary near-exact tree frozen; service-worker, IndexedDB, vault, outbox and sync boundaries documented.
- Pass 5: 95 extension directories, 112 provider mappings and the install/uninstall lifecycle inventoried; stale mappings, duplicate symbols/migrations and supply-chain risks documented; canonical qualification and manifest policy established.
- Agent OS bootstrap: federated documentation layer, Claude mandate, status centre, Chronicle, Kernel constitution, source registry and initial metadata schemas established.
- Remaining clusters: communications, automation, data architecture and release/deployment guidance.
