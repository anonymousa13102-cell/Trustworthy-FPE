# Model and Runtime Configuration

This file records the shared setup, runtime environment, verification protocol, refinement protocol, batch-processing settings, and metrics used for the COBOL functional-property extraction and formal-verification framework.

The framework processes COBOL source code through the following chain:

```text
COBOL source
  -> Koopa XML
  -> parsed JSON
  -> business rules
  -> mathematical specifications
  -> formal assertions
  -> generated Z3 program model
  -> verification
  -> optional counterexample-guided refinement
```

---

## 1. Shared Experimental Setup

| Item | Setting |
|---|---|
| LLM model | `GPT-5.2 (version:2025-12-11)` |
| API | Azure OpenAI Chat Completions API |
| LLM execution | Remote API call |
| Credentials | Environment variables (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`); not included |
| Input language | COBOL |
| Platform | Windows |
| Supported source extensions | `.cbl`, `.cob`, `.cobol` |
| COBOL parser | Koopa AST in XML format |
| Parsed representation | JSON generated from Koopa XML |
| Formal solver | Z3 through the Python `z3-solver` package |
| Unit of evaluation | One COBOL source program |
| Parsing and verification | Local execution |

--- 

## 2. Hardware and Software Environment

All reported experiments should use the same machine and software environment unless a deviation is explicitly documented.

### 2.1 Hardware

| Component | Specification |
|---|---|
| Processor | Intel(R) Core(TM) 5 220U, Intel(R) Graphics, 1.40 GHz |
| Memory | 16 GB RAM, 5200 MT/s |
| Storage | 477 GB SSD |
| Operating system | Windows 11 Pro, version 25H2 (OS build 26200.9711) |

### 2.2 Software

| Component | Version / Setting |
|---|---|
| Python | 3.11.6 |
| Java runtime | 17.0.17 |
| Koopa | v20260516 |
| `z3-solver` | 5.1.0 |
| Azure OpenAI SDK or client | 3.20.0 |

### 2.3 Timing

Reported durations are wall-clock times measured on the experiment machine. End-to-end timing includes:

- local preprocessing;
- Koopa execution;
- LLM API latency;
- artifact generation;
- SMT compilation;
- Z3 execution;
- automatic refinement, when triggered.

---
## 3. Intermediate Artifacts

Each program can produce the following artifacts:

| Artifact | Purpose |
|---|---|
| `<program>_koopa.xml` | Concrete parse output produced by Koopa |
| `parsed.json` | Normalized program structure, variables, paragraphs, statements, and control flow |
| `business_rules.json` | Source-backed business rules for explicit state-changing operations |
| `math_specs.json` | Formal transition specifications linked to business rules |
| `assertions.txt` | Assertion-language representation of the mathematical specifications |
| `z3_assertions.py` | Executable symbolic program model and verification query |
| `verification_result.json` | Initial or final Z3 result |
| `refinement_log.json` | Refinement candidates, attempts, accepted/rejected repairs, and verification history |
---

## 4. Pipeline Configuration

| Stage | Input | Output | Main responsibility |
|---|---|---|---|
| Koopa XML | COBOL source | Koopa XML | Parse COBOL syntax |
| Parse | Koopa XML | `parsed.json` | Normalize declarations, paragraphs, operations, and control flow |
| Rules | `parsed.json` | `business_rules.json` | Extract source-backed state-transition rules |
| Specs | BRs and parsed source | `math_specs.json` | Formalize each BR using `OLD/NEW` state notation |
| Assertions | Math specs | `assertions.txt` | Convert transitions to formal assertions |
| SMT compilation | Parsed source and assertions | `z3_assertions.py` | Build the symbolic executable model and proof obligations |
| Verify | Generated Z3 script | Verification result | Run consistency, reachability, and final verification checks |
| Refine | Failed result and artifacts | Updated artifacts and log | Localize and repair selected BR/MS/assertion chains |

### 4.1 Parser Setting

| Item | Setting |
|---|---|
| Default parser | `koopa` |
| Parser failure behavior | Record `error`; preserve logs; continue with the next source in batch mode |

### 4.2 LLM Setting

| Item | Setting |
|---|---|
| LLM selection argument | `--llm azure>` |
| Temperature | 0.0 |
| Maximum tokens | Not explicitly configured; |
| Retry policy | Retried once with the validation error as feedback; if the retry also fails, the artifact is kept unchanged |
| Prompt files | `<FILL IN: paths to BR, MS, assertion, triage, and repair prompts>` |
| Hard-coding restriction | Generated artifacts must be source-derived and must not encode counterexample-specific expected outputs |

---