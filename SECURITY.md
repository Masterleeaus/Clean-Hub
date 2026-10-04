# Security Policy

## Scope

Clean-Hub contains AI-assisted business workflows, customer and property records, workforce operations, finance-related functionality, provider credentials, file/document flows, and external integrations.

Security-sensitive areas include:

- company/tenant isolation
- authentication and authorization
- AI tool execution
- WorkCore business actions
- provider credentials
- confirmation and approval flows
- idempotency / replay
- audit and domain events
- payments and financial records
- file/document access
- realtime/broadcast channels
- external webhooks and integrations

## Reporting a vulnerability

Please do **not** publish exploitable details, credentials, customer data, or destructive proof-of-concept material in a public issue.

Preferred reporting path:

1. use GitHub Private Vulnerability Reporting / Security Advisories for this repository when available
2. otherwise contact the repository owner privately through the account's published contact channel
3. include the affected path, impact, reproduction steps, and a minimal non-destructive proof

## AI execution security model

Clean-Hub is designed around a separation between model intent and application authority.

A model-generated request should not bypass:

```text
active company
    ↓
registered tool/action
    ↓
entitlement
    ↓
permission
    ↓
explicit confirmation
    ↓
idempotency
    ↓
transactional business action
```

### Company authority

Tool arguments must not be trusted to establish tenant authority.

The current ToolRouter rejects recursive `company_id` and `companyId` overrides.

### Confirmation authority

Model output is not considered valid confirmation.

The Titan Zero tool envelope parser rejects non-null model-supplied confirmation IDs.

### Tool registration

Unknown tools should fail closed.

### Business action authority

Sensitive writes should enforce authorization at the deterministic domain/action layer, not only in prompts or UI.

## Provider credentials

Provider credentials should:

- remain server-side
- be stored through the configured Vault/secret mechanism
- never be committed
- never be returned in API responses
- never be written to logs
- only be used against explicitly allowed HTTPS hosts

## Secrets

Do not commit:

- production `.env`
- real APP keys
- OAuth client secrets
- provider API keys
- database credentials
- webhook signing secrets
- private certificates
- real session tokens
- customer exports

Test fixtures should use clearly synthetic values and should align with repository secret-detection policy.

## Multi-tenancy testing

Changes touching tenant/company-owned data should include negative tests for:

- another company ID
- another actor
- stale active-company context
- nested tenant override
- unauthorized read
- unauthorized write
- cross-company broadcast channel subscription

## Financial and irreversible actions

Payments, refunds, payroll, destructive deletion, compliance actions and other high-impact writes should receive stronger controls than ordinary reads.

Where applicable include:

- explicit user approval
- replay/idempotency protection
- audit evidence
- domain event evidence
- rollback or compensation behavior
- targeted regression tests

## Current verification boundary

The repository's CI is currently red.

Known issues include:

- stale Composer lock metadata
- source-contract drift
- baseline rejection of populated test APP keys
- missing frontend `@tailwindcss/vite`
- 15 Titan architecture-verifier failures

A security-sensitive change should not be described as fully verified unless the relevant tests actually ran.

## Responsible disclosure

Good-faith testing should:

- minimize access to data not owned by the researcher
- avoid service disruption
- use synthetic/test accounts
- avoid extracting secrets
- allow reasonable remediation time before public disclosure
