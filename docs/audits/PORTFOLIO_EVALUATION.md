# Clean-Hub — Portfolio Evaluation

## Purpose

This document defines what Clean-Hub can currently prove and what still needs measurement.

The central portfolio claim is not that the AI is unusually capable.

The central claim is that **AI-assisted business writes are forced through deterministic authority and reliability boundaries**.

That claim should be evaluated directly.

## Evidence vocabulary

Use these terms precisely:

- **Implemented** — source is present and wired.
- **Tested** — relevant tests have actually executed successfully.
- **Evaluated** — a reproducible scenario dataset and metric exist.
- **Experimental** — source exists but verification is incomplete.
- **Planned** — no implementation claim is made.

## Remediation status after the reviewed runs

Several failures described below were subsequently repaired directly on `main`:

- the source verifier now points to `docs/archive/plans/2026-07/titan-zero-chatbot-pwa-upgrade-plan.md`;
- the source-verifier fixture uses the same canonical archived path;
- the repository baseline now excludes the deterministic test-only APP keys in `.env.testing` and `.env.verification` while continuing to reject other populated tracked APP keys;
- the root Vite config no longer imports the Tailwind 4 Vite plugin and now relies on the existing Tailwind 3/PostCSS configuration.

These are code/configuration remediations, not new passing evidence. A fresh workflow run is still required before any of those lanes can be called green.

## Current executed CI evidence

### Titan Zero Source Verification — reviewed run #70

Workflow run: `37176822035`

Result:

- source-verifier regression tests: **2 passed / 0 failed**
- required-source verification: failed
- remaining steps: skipped after failure

Failure:

```text
MISSING: TITAN_ZERO_CHATBOT_PWA_UPGRADE_PLAN.md
```

This proves the source-verifier's own regression tests execute successfully, but not the entire source-verification workflow.

## Repository Baseline — reviewed run #62

Workflow run: `37176822074`

### Source-integrity job

Passed:

- required application file checks
- forbidden tracked runtime-file checks

Failed on populated Laravel key detection:

```text
.env.testing
.env.verification
```

Both contain populated placeholder APP keys and are rejected by the baseline policy.

### PHP baseline job

Composer strict validation failed because:

```text
composer.json requires phpoffice/phpspreadsheet ^5.8
composer.lock contains 4.5.0
```

Later PHP syntax and local-package checks were skipped.

## Laravel CI — reviewed run #40

Workflow run: `37176822034`

### Architecture tools

`php tools/titan_verify.php` completed:

```text
Titan verification: 42917 passed, 15 failed
```

Total checks executed:

```text
42,932
```

Failures included:

- incomplete WorkCore Rewind quarantine contract
- incomplete WorkCore Intelligence quarantine contract
- canonical Documents module registration
- canonical Assurance module registration
- governed read executor registration
- Titan operations named route
- company setup fallback route
- authenticated + active-company route protection
- company public identifier creation
- company-scoped presence channel
- active membership presence authorization
- company-scoped conversation broadcast authorization
- company-scoped private user broadcast channel
- missing `/.worktrees` gitignore protection
- missing `/storage/integration-evidence` gitignore protection

### Composer validation

Failed because the lock file is stale relative to the current root manifest.

### Frontend build

`npm ci` succeeded:

```text
608 packages installed
```

npm reported:

```text
39 vulnerabilities
2 low
4 moderate
33 high
```

The build then failed:

```text
Cannot find module '@tailwindcss/vite'
```

### Main Laravel tests

The install/lint/boot/test job and migration-validation job were skipped because the Composer validation dependency failed first.

Therefore there is no current executed full-suite pass/fail count that should be promoted as application-health evidence.

## Focused Titan AI standalone test source

`tests/Standalone/TitanAI/run.php` contains 8 focused assertions covering:

1. valid tool envelope acceptance
2. rejection of extra envelope fields
3. rejection of model-generated confirmation
4. ordinary text not treated as a tool call
5. nested snake-case company override rejection
6. camel-case company override rejection
7. legitimate identifier preservation
8. message role/content normalisation

The file exists as focused verification source.

Do not report these 8 as an executed passing result unless the standalone runner is actually executed in a verified environment.

---

# Proposed Evaluation 1 — Governed Action Safety

## Hypothesis

The governed AI path prevents invalid or unauthorized state mutation more reliably than direct handler invocation.

## Systems

### Governed

```text
TitanZeroOrchestrator
→ ToolRouter
→ BusinessActionDispatcher
→ handler
```

### Baseline

A controlled test harness that invokes the same handler without the ToolRouter/BusinessActionDispatcher policy stack.

This baseline exists only for evaluation. It should not be exposed as a production path.

## Scenario dataset

Include at least:

- valid entitled action
- valid action with insufficient permission
- unentitled company
- missing confirmation
- fabricated confirmation
- company mismatch
- actor mismatch
- operation-context mismatch
- tenant override in root arguments
- nested tenant override
- unknown action
- invalid handler class
- handler exception
- first idempotent request
- repeated identical request
- repeated key with altered payload
- concurrent duplicate request
- read-only operation
- malformed model envelope
- ordinary non-tool model text

## Metrics

### Unauthorized mutation rate

```text
unauthorized mutations / unauthorized scenarios
```

Target for governed path: 0%.

### Valid execution rate

```text
correctly executed valid actions / valid scenarios
```

### Confirmation bypass rate

```text
confirmed-required actions executed without valid application confirmation
---------------------------------------------------------------
all confirmation-required negative scenarios
```

### Tenant override rejection rate

### Idempotent replay correctness

### Transaction rollback correctness

### Audit completeness

For every attempted write, record whether expected audit evidence exists.

### Domain-event completeness

For successful writes, verify expected event IDs are present.

## Contribution analysis

Compare governed and baseline results.

The evaluation should show whether the control boundary itself changes unsafe-mutation behavior.

---

# Proposed Evaluation 2 — Tool Envelope Robustness

Test:

- valid JSON
- key order variation
- markdown-fenced JSON
- extra fields
- missing fields
- malformed JSON
- blank tool
- scalar arguments
- non-null confirmation
- nested company ID
- unicode keys/values
- oversized arguments
- prompt-injection text around JSON
- multiple JSON objects
- ordinary prose

Metrics:

- false tool activation rate
- valid envelope acceptance rate
- invalid envelope rejection rate

---

# Proposed Evaluation 3 — Provider Conformance

The repository currently has overlapping provider abstractions.

Test equivalent prompts across:

- OpenAI
- Anthropic
- Gemini
- DeepSeek
- xAI
- OpenRouter-style assistant configuration where applicable

Measure:

- successful completion
- error mapping
- empty-response handling
- message normalization
- image support where implemented
- timeout behavior
- credential rejection mapping

Do not claim provider equivalence until these scenarios have been executed.

---

# Proposed Evaluation 4 — Failure Recovery

Test:

- provider timeout
- provider 401/403
- provider 429
- database handler exception
- audit recorder failure
- domain event recorder failure
- idempotency-store failure
- confirmation verifier failure
- missing active company
- missing tool registration

Key question:

> Does failure remain visible and leave the business state in a safe, explainable condition?

---

# Required result format

Every published evaluation should record:

- repository commit SHA
- evaluation version
- scenario count
- seed where applicable
- runtime version
- database
- provider/model versions
- baseline definition
- raw or machine-readable results
- pass/failure breakdown
- reproduction command

Example:

```text
Commit:                  <sha>
Scenarios:               120
Valid:                   40
Unauthorized:            40
Malformed/adversarial:   40
Governed unsafe writes:  0
Baseline unsafe writes:  <measured>
Confirmation bypasses:   0
Tenant bypasses:         0
Idempotency failures:    <measured>
```

No numbers should be inserted until the suite is actually run.

## Current conclusion

Clean-Hub has strong **mechanism evidence** but incomplete **evaluation evidence**.

The most valuable next step is not adding more architecture claims. It is converting the governed-action invariants into a fixed adversarial benchmark and publishing the failures as openly as the passes.
