# Trustworthy-FPE

**Trustworthy Functional Property Extraction and Verification for COBOL Programs**

---

## 1. Overview

Legacy COBOL systems encode decades of business logic with no machine-checkable specification of what that logic actually guarantees. Trustworthy-FPE is a research artifact that uses an LLM to extract functional properties from COBOL source — business rules, mathematical specifications and formal assertions — and then **validates every generated property against the program's own semantics using the Z3 SMT solver**, rather than trusting the LLM's output as-is.

When Z3 finds a counterexample (the generated property does not actually match the program), the framework does not discard the result or regenerate everything from scratch. It runs a **counterexample-guided refinement loop** that localizes the fault to the smallest responsible business rule / mathematical specification / assertion chain and repairs only that chain, then re-verifies.

This repository contains the input programs, the prompt templates used to drive the LLM at every stage, the environment/runtime configuration, and the full set of intermediate and final artifacts produced for each program.

---

## 2. Pipeline

```text
COBOL source (.cbl/.cob)
      │
      ▼
Koopa parser  ───────────────►  <program>_koopa.xml        (concrete parse tree)
      │
      ▼
Deterministic normalization ──►  parsed.json                (declarations, paragraphs, control flow)
      │
      ▼
P1: Business-Rule Generation (LLM) ──►  business_rules.json (SBVR-style rules, one per functional op)
      │
      ▼
P2: Math Spec Generation (LLM) ─────►  math_specs.json      (OLD/NEW transition specs per rule)
      │
      ▼
P3: Assertion Generation (LLM) ─────►  assertions.txt       (raw assert() statements)
      │
      ▼
Deterministic SMT compilation ──────►  z3_assertions.py     (executable Z3 program model + checks)
      │
      ▼
Z3 verification ────────────────────►  verification_result.json
      │
      ├── UNSAT → done, property set validated
      │
      └── SAT / invalid_spec → P4: Refinement (Triage + Repair) ──► refinement_log.json
                                        │
                                        └── patched BR/MS/assertion → re-verify (loops until UNSAT or budget exhausted)
```

Only the BR/MS/assertion chain identified by refinement is patched — the rest of the generation pipeline is not re-run.

---

## 3. Repository structure

```
Trustworthy-FPE/
├── README.md
├── environment/
│   └── model_runtime_config.md
├── inputs/
│   ├── CNWYLIFE.cbl
│   ├── EMPPAY.CBL
│   ├── RISK-LIMIT.cbl
│   ├── c03ex02.cob
│   ├── fibbase.cbl
│   ├── httpstatus.cbl
│   └── prtrpt1.cbl
├── prompts_templates/
│   ├── business_rules_prompt_template.md
│   ├── math_specs_prompt_template.md
│   ├── assertions_prompt_template.md
│   └── refinement_prompt_template.md
└── results/
    ├── CNWYLIFE/
    ├── EMPPAY/
    ├── RISK-LIMIT/
    ├── c03ex02/
    ├── fibbase/
    ├── httpstatus/
    └── prtrpt1/
```

---

## 4. Inputs

The framework is evaluated on **7 COBOL programs** (`inputs/`), covering recursion, nested conditionals, level-88 condition-names, table/array indexing, string formatting, and payroll/report-generation logic:

| # | File | Program | Notes |
|---|------|---------|-------|
| 1 | `CNWYLIFE.cbl` | CNWYLIFE | Conway's Game of Life — grid update, neighbor counting |
| 2 | `EMPPAY.CBL` | EMPPAY | Employee payroll calculation |
| 3 | `RISK-LIMIT.cbl` | RISK-LIMIT | Risk-code banding (the motivating example — level-88 `VALUE ... THRU ...` ranges) |
| 4 | `c03ex02.cob` | c03ex02 | Textbook COBOL control-flow example |
| 5 | `fibbase.cbl` | FIBBASE | Fibonacci sequence via recursion/iteration (`LK-NUM`, `LK-ANT`, `LK-ATU`, `LK-FIB`) |
| 6 | `httpstatus.cbl` | HTTPSTATUS | HTTP status-code classification |
| 7 | `prtrpt1.cbl` | PRTRPT1 | Print-report generation |

Each program is processed independently; there is no cross-program state.

---

## 5. Prompt templates (`prompts_templates/`)

Four prompt templates drive the four LLM-facing stages of the pipeline. Each file documents the agent's role, its inputs/outputs, and the exact prompt text used.

| File | Stage | Role | Input | Output |
|---|---|---|---|---|
| [`business_rules_prompt_template.md`](prompts_templates/business_rules_prompt_template.md) | **P1** — Business-Rule Generation | Classifies each functional COBOL operation as an SBVR `NECESSITY` / `OBLIGATION` / `PROHIBITION` rule, expands level-88 condition-names into parent-variable comparisons, and writes a natural-language sentence per rule. Non-functional operations (logging, display, control-flow-only `PERFORM`) are excluded. | `parsed.json` (functional operations + deterministic execution conditions) | `business_rules.json` |
| [`math_specs_prompt_template.md`](prompts_templates/math_specs_prompt_template.md) | **P2** — Mathematical Specification Generation | Converts each business rule into a local, one-operation pre/post transition property using an `OLD`/`NEW` variable contract. Classifies each property as `precondition`, `invariant`, or a state transition. The AST is consulted only to verify names/types/literals, never to rewrite a rule's condition. | `business_rules.json` + `parsed.json` (as secondary authority) | `math_specs.json` |
| [`assertions_prompt_template.md`](prompts_templates/assertions_prompt_template.md) | **P3** — Assertion Generation | Converts each mathematical specification's `expression` field into a raw declarative `assert()` statement (`P IMPLIES Q` → `!P \|\| Q`), preserving every `OLD`/`NEW` identifier exactly. One assertion is produced per math spec, in the same order. | `math_specs.json` | `assertions.txt` |
| [`refinement_prompt_template.md`](prompts_templates/refinement_prompt_template.md) | **P4** — Refinement (Triage + Repair) | A two-node loop invoked when Z3 returns `SAT` (counterexample) or `invalid_spec` (mutual unsatisfiability). **Triage** runs a 7-pass deterministic priority queue (exact invalid-spec indices → exact Z3 failed-assertion indices → exact failed-check indices → NEW-target match → source-block match → antecedent-consistency filter → variable-overlap filter) and only falls back to an LLM call when the candidate set is still ambiguous. **Repair** routes to one of four repair paths depending on the failure kind and patches only the implicated BR → MS → Assertion chain. | Failed `verification_result.json` + the current BR/MS/assertion artifacts | Patched `business_rules.json` / `math_specs.json` / `assertions.txt` + an entry in `refinement_log.json` |

The Koopa-XML-to-`parsed.json` normalization step and the `assertions.txt`-to-`z3_assertions.py` SMT compilation step are both **deterministic** (no LLM call) and therefore have no prompt template.

---

## 6. Outputs (`results/<program>/`)

Each of the 7 input programs produces its own result folder. A folder contains **up to 8 artifact files**; two programs (`EMPPAY`, `httpstatus`) verified successfully on the first attempt and therefore have no `refinement_log.json` — the other **5 programs required at least one refinement round**.

| File | Always produced? | Format | Contents |
|---|---|---|---|
| `<program>_koopa.xml` | Yes | XML | Raw concrete parse tree emitted by the Koopa COBOL parser — the only non-normalized artifact in the pipeline. |
| `parsed.json` | Yes | JSON, `{"programs": [...]}` | Deterministic, normalized program representation: data declarations, paragraphs/statements, control flow, and the functional operations (with their deterministic execution conditions) that feed P1. |
| `business_rules.json` | Yes | JSON, `{"program_name", "variable_roles", "business_rules": [...]}` | One entry per extracted rule: `id` (e.g. `BR1`), `sbvr_class`, `verb_concept`, `rule` (formal SBVR text), `natural_language_rule`, `source_variables`, `source_block`. `variable_roles` classifies every COBOL variable (e.g. `BUSINESS_ENTITY`). |
| `math_specs.json` | Yes | JSON, `{"program_name", "math_specs": [...]}` | One `MS<i>` entry per business rule, giving the OLD/NEW transition `expression`, its property kind, and a link back to the source `BR` id. |
| `assertions.txt` | Yes | Plain text | One `assert(...)` line per math spec, in order — the literal input to the Z3 model (e.g. `assert((!(((LK-NUM-OLD == 0))) \|\| ((LK-FIB-NEW == LK-ANT-OLD))));`). |
| `z3_assertions.py` | Yes | Executable Python | The deterministically compiled, runnable Z3 program: declares all SSA-versioned symbols, encodes the COBOL program's own semantics (`COBOL_PROGRAM`), and runs the consistency / reachability / final-verification checks, printing the same `[Z3 Runtime] ...` trace found in `z3_output`. |
| `verification_result.json` | Yes | JSON | `status`, `initial_status`, `final_status`, `rounds`, `refinement_iterations`, full `z3_output` trace, `initial_failed_assertion_indices` / `initial_failed_checks` (first run), and the corresponding fields for the final run (`contradictory_assertion_indices`, `failed_assertion_indices`, `failed_checks`, `vacuous_assertion_indices`). `status: "verified"` means the final Z3 run returned `UNSAT`. |
| `refinement_log.json` | Only if refinement ran | JSON | Per-program refinement trace: `repairs` / `accepted_repairs` / `rejected_repairs` (each with `layer`: `BR`/`MS`/`ASSERTION`, `id`/`index`, `old`, `new`, `reason`), `attempt_history` (triage candidates + proposed repairs per iteration), `counterexample_history` (round, iteration, phase — `initial_verification` or `post_repair_verification` — and the Z3 counterexample variables), and `verification_history` (one entry per re-verification round). |

**Summary of inputs vs. outputs:**

| Metric | Count |
|---|---|
| Input COBOL programs | 7 |
| Result folders produced | 7 (one per input program) |
| Programs verified without refinement | 2 (`EMPPAY`, `httpstatus`) |
| Programs requiring ≥1 refinement round | 5 (`CNWYLIFE`, `RISK-LIMIT`, `c03ex02`, `fibbase`, `prtrpt1`) |
| Artifact files per program | up to 8 (7 when no refinement was needed) |
| Prompt templates (LLM-facing stages) | 4 (`P1` business rules, `P2` math specs, `P3` assertions, `P4` refinement) |

---

## 7. Environment and runtime configuration

Full experimental setup — LLM model/API, hardware, software versions, pipeline stage table, parser and LLM settings — is recorded in [`environment/model_runtime_config.md`](environment/model_runtime_config.md). In brief:

| Item | Setting |
|---|---|
| LLM model | `GPT-5.2 (version: 2025-12-11)`, via Azure OpenAI Chat Completions API, temperature `0.0` |
| COBOL parser | Koopa (AST emitted as XML) |
| Formal solver | Z3 via the Python `z3-solver` package |
| Unit of evaluation | One COBOL source program per run |
| Parsing and verification | Local execution |
| Refinement policy | `MaxIterations = 3` and user can edit it; verification result as context given. If the refinement also fails, the artifact is kept unchanged |

---

## 8. Notes

- All JSON artifacts for a given program are mutually traceable: a `business_rules.json` entry `BR<i>` maps to `math_specs.json` entry `MS<i>`, which maps to the `i`-th `assert()` line in `assertions.txt` and the `i`-th (1-based) assertion index referenced throughout `verification_result.json` / `refinement_log.json`.
- `refinement_log.json` is only written for programs where the initial Z3 run returned `SAT` or `invalid_spec`; its absence for a program is itself informative (first-pass verification succeeded).
- The Koopa-XML and `z3_assertions.py` artifacts are generated by deterministic code, not by the LLM, and are included for full reproducibility of the verification step from any program's business rules onward.