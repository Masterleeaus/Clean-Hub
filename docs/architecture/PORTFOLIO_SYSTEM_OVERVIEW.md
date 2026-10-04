# Clean-Hub — Portfolio System Architecture

## Purpose

This document describes the source-backed architecture most relevant to Clean-Hub as an AI systems engineering portfolio project.

It does not replace the broader documentation library. For full project authority and documentation policy, see `docs/README.md`.

## Architectural proposition

Clean-Hub separates:

1. conversational AI
2. company/tenant context
3. tool registration
4. business-action authority
5. transactional state mutation
6. audit and domain-event evidence

The key rule is:

> A model may propose an action, but it does not supply its own authority to execute that action.

## Governed AI execution path

```text
Conversation
    │
    ▼
ConversationContextBuilder
    │
    ▼
TitanZeroOrchestrator
    │
    ├──── ordinary response ─────► return text
    │
    ▼
strict tool envelope
    │
    ▼
ToolRouter
    │
    ├──── capability
    ├──── WorkCore action
    └──── WorkCore read model
             │
             ▼
BusinessActionDispatcher
             │
    ┌────────┼────────┬────────────┬──────────────┐
    ▼        ▼        ▼            ▼              ▼
 tenant  entitlement permission confirmation  idempotency
 context
             │
             ▼
       database transaction
             │
             ├─ handler
             ├─ domain events
             ├─ audit record
             └─ idempotency completion
```

## 1. Titan Zero orchestration

Primary implementation:

- `app/Titan/AI/TitanZeroOrchestrator.php`
- `app/Titan/AI/ConversationContextBuilder.php`

The orchestrator:

- receives conversation context
- constructs the system instruction
- invokes the configured assistant
- distinguishes ordinary text from executable tool requests
- only accepts a narrow JSON envelope for tool execution
- supplies conversation, confirmation, idempotency, and correlation metadata to the tool layer

### Tool envelope invariant

The accepted object contains exactly:

```json
{
  "tool": "registered.tool.id",
  "arguments": {},
  "confirmation_id": null
}
```

The parser rejects:

- extra keys
- malformed JSON
- blank tool names
- non-object arguments
- non-null confirmation IDs supplied by model output

This prevents the model from manufacturing application confirmation authority.

## 2. Tool routing

Primary implementation:

- `app/Titan/AI/ToolRouter.php`

The router can dispatch:

- registered Titan capabilities
- registered WorkCore business actions
- registered WorkCore read models

Before dispatch it rejects tenant/company overrides supplied through arguments.

The guard recursively normalises keys so both forms such as:

- `company_id`
- `companyId`

are rejected.

The company context must come from the application.

## 3. Business action kernel

Primary implementation:

- `app/Domains/WorkCore/System/Actions/BusinessActionDispatcher.php`

The dispatcher checks:

1. action registration
2. tenant context consistency
3. operation context consistency
4. company entitlement
5. actor permission
6. explicit confirmation
7. idempotent replay

Only then does it open a database transaction and execute the registered handler.

Inside the transaction it records:

- idempotency reservation
- handler result
- domain events
- audit completion
- idempotency completion

On failure, it attempts to record failed idempotency and failed audit state while preserving the original exception.

## 4. Company-scoped provider configuration

Primary implementation:

- `app/Services/AIAssistantService.php`

The company assistant path:

- resolves the active company
- reads company-specific AI configuration
- resolves credentials via the Vault
- requires HTTPS
- restricts endpoints to configured allowed hosts
- maps provider failures to safe application errors
- truncates context and content
- rejects invalid message roles

Currently this path supports:

- OpenAI-format provider requests
- OpenRouter-style configuration
- Gemini

## 5. General AI completion layer

Primary implementation:

- `app/Services/Ai/AiCompletionService.php`

Text completion paths exist for:

- OpenAI
- Anthropic
- Gemini
- DeepSeek
- xAI

Image-aware completion paths exist for:

- OpenAI
- Anthropic
- Gemini

This layer is broader than `AIAssistantService` and is not yet fully consolidated with it.

## 6. WorkCore operational domain

Primary root:

- `app/Domains/WorkCore/`

WorkCore provides the deterministic business domain behind AI-assisted operations.

Its responsibilities include:

- actions
- read models
- tenancy
- permissions
- capabilities
- operational modules
- events
- audit/outbox-related behavior
- scheduling/dispatch and service workflows

The important architectural point is not any single module. It is that AI-assisted work must pass through the same business rules as ordinary application operations.

## 7. Interaction definitions

`interactions/` contains declarative interaction definitions.

These can describe:

- fields/questions
- validation
- permissions
- capability/action references
- workflow sequencing

This separates parts of interaction behavior from ad hoc controller code.

## 8. Verification layers

The repository has multiple verification systems:

### Repository baseline

`.github/workflows/repository-baseline.yml`

Checks source presence, secrets, Composer metadata, PHP syntax, and local package structure.

### Titan Zero source verification

`.github/workflows/titan-zero-verify.yml`

Checks source contracts, JSON, registration contracts, syntax, Composer metadata, Interaction Engine standalone behavior, and shell syntax.

### Laravel CI

`.github/workflows/ci-laravel.yml`

Checks Composer validity, architecture tools, Pint, Unit/Feature/Architecture tests, boot, migrations, and frontend build.

### Titan architecture verifier

`tools/titan_verify.php`

This is a large source/architecture integrity verifier. In the latest reviewed PR run it executed 42,932 checks, with 42,917 passing and 15 failing.

## 9. Trust boundaries

### Model boundary

The model produces intent or a registered tool request.

It does not own:

- company scope
- permissions
- entitlement
- confirmation
- idempotency authority

### Tool boundary

The tool router decides whether a requested capability/action/read model is registered and whether request input attempts to override tenant authority.

### Business action boundary

The dispatcher owns deterministic execution policy and state mutation.

### Provider boundary

Provider credentials and endpoints remain application configuration and Vault concerns.

## 10. Current architecture limitations

The architecture is stronger than the current runtime proof.

Current CI evidence still reports:

- 15 Titan verifier failures
- stale Composer lock state
- source-contract drift
- test APP keys rejected by the baseline workflow
- missing frontend `@tailwindcss/vite` dependency
- incomplete full-suite execution

Therefore this document establishes architectural implementation, not production certification.
