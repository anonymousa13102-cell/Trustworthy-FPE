# Prompt P4: Refinement (Triage and Repair)

Refinement is a two-node loop invoked whenever Z3 returns SAT with a
counterexample, or reports `invalid_spec` (mutual unsatisfiability). Node 1
is the Triage Agent, which identifies the narrowest suspect BR/MS set using a
deterministic priority queue and calls an LLM only when that queue remains
ambiguous after all passes. Node 2 is the Repair Agent, which routes to one
of four repair paths depending on the failure kind, and within each path
applies a top-down BR → MS → Assertion slicing strategy using a
plan-then-execute design, patching only the affected IDs without re-running
the full generation pipeline.

---

## P4.1 Triage Agent

The triage agent runs a deterministic priority queue before any LLM call.
The queue executes the following passes in order, each narrowing the candidate
set:

1. **Exact invalid-spec assertion numbers** — when `verification_status` is
   `invalid_spec`, one-based assertion numbers from
   `contradictory_assertion_indices` are mapped to artifact positions
   (number − 1) and the linked BR/MS IDs are set directly; the queue stops
   and `contradiction_mode` is set to `True`.
2. **Exact Z3 assertion indices** — `FAILED_ASSERTION_INDICES` from Z3
   diagnostics are used to attribute the failing MS and its linked BRs
   exactly; the queue stops.
3. **Exact failed-check indices** — indices from `FAILED_CHECK` diagnostics
   are used in the same way; the queue stops.
4. **NEW target** — the failing assignment target reported by the verifier
   narrows the candidate set to specs whose expression contains that
   `VARIABLE-NEW`.
5. **Source block** — the failing source block narrows candidates by matching
   `source_block` on the spec or its linked BR.
6. **Antecedent-consistency filter** — a candidate is dropped only when the
   counterexample provides positive evidence that the candidate rule's own
   antecedent is false (vacuously satisfied and cannot be the violated one).
   Fails open: anything unparseable or absent from the counterexample is left
   in. If filtering would remove every candidate, the unfiltered list is kept.
7. **Variable overlap** — applied only to the already-narrowed set; candidates
   whose linked BR `source_variables` share no base name with the
   counterexample variables are removed.

The LLM is called only when the queue remains ambiguous after all seven
passes. It receives only the surviving candidate BRs, never the full rule set.

### P4.1.1 LLM Triage Prompt

````text
A Z3 SMT solver produced this counterexample:
{ce_vars}

Business rules available:
{br_summary}

Which BR IDs are most likely the root cause of this counterexample?
Return ONLY a JSON list of BR IDs, e.g. ["BR1","BR3"]. No other text.
````

### P4.1.2 Triage Placeholders

| Placeholder    | Meaning                                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------------------- |
| `{ce_vars}`    | JSON-serialised counterexample variable map produced by Z3                                                  |
| `{br_summary}` | Newline-separated list of `id: rule[:120]` for every surviving candidate BR (never the full rule set)       |

---

## P4.2 Repair Agent

- **Contradiction path** — when `contradiction_mode` is `True`; uses
  `_check_ms_contradiction` (P4.2.2). Business rules are not touched.
- **Counterexample path** — the standard counterexample
  path; uses a plan-then-execute design with `_plan_prompt` (P4.2.3). Operates
  one layer at a time (BR → MS → ASSERTION), determined by
  `_select_repair_layer`. If all candidates at a layer return KEEP, the agent
  advances to the next layer automatically.

Every proposed correction is validated before being written to disk: it must
not contain numbered SSA names, must reference only declared COBOL variables
(and level-88 condition names), and for formal expressions must parse as a
valid Boolean expression. A correction that fails validation receives one retry
with the specific rejection reason; if it still fails, the original text is
preserved and the rejection is recorded in the repair log.

---
````

### P4.2.1 MS Contradiction Prompt (`_check_ms_contradiction`)

Used only when `contradiction_mode = True`. There is no counterexample; Z3
proved the assertion set is mutually unsatisfiable independent of any program
input.

````text
A Z3 SMT solver proved that the following math spec is UNCONDITIONALLY
contradictory with at least one sibling spec in the same program's assertion
set. This was determined with NO program input involved at all — the specs
simply cannot all be true at the same time, as unconditional universal
properties.

Math spec under review:
  ID: {ms_id}
  Kind: {kind}
  Description: {description}
  Expression: {expression}

Conflicting sibling expression(s) in the same assertion set:
{sibling_expressions}

{feedback}
This pattern usually means the expression above is a branch-specific GUARD
condition (e.g. 'this only applies when TRANS-TYPE is X') that was incorrectly
written as a universal, unconditional property instead of being scoped to only
its own branch.

- If this spec's condition is already used correctly as the antecedent of an
  implication in another spec (i.e. it is truly redundant), the correct fix is
  to return exactly the single word TRUE — this neutralizes it as an assertion
  without deleting it, since it adds nothing the implication-bearing spec
  doesn't already guarantee.
- Otherwise, return the expression properly wrapped as an implication so it
  only applies within its own branch.

Return ONLY the corrected expression (either TRUE, or a full expression).
No JSON, no explanation, no markdown.
````

### P4.2.2 Counterexample Prompt (`_plan_prompt`)

The layer-scoped path uses a single plan prompt that is parameterised by the
active layer (BR, MS, or ASSERTION). The `{layer}`, `{target_field}`, and
`{identity_field}` slots are filled deterministically before the LLM call.

````text
You are the planning component of a verification refinement agent.
Analyze the complete same-layer context and all read-only references together.
The parsed JSON is authoritative at BR layer. Upstream corrected artifacts are
authoritative at later layers. The Z3 counterexample is diagnostic evidence.

You may UPDATE, REMOVE, or KEEP only writable {layer} candidates. Read-only
items may be compared and cited as evidence but must never be changed.
REMOVE is allowed only when evidence proves the writable item is redundant,
duplicated, invalid, or not represented by the authoritative upstream source.
Do not paraphrase. Do not change quoting alone. Do not reverse assignment
direction. Do not introduce paragraph names as variables. BR text must remain
business language: never write -OLD, -NEW, IMPLIES, symbolic &&/||, or IF TRUE
inside a BR. Never place PERFORM, PERFORMING, PERFORMANCE, VARYING, AFTER,
UNTIL, paragraph names, or loop narration in new_rule. Those are compiler
metadata, not business-rule syntax. If parsed_json exposes required execution
context only as Perform-Unsupported, keep the BR unchanged and diagnose a
compiler-model limitation. Derive the complete execution path from parsed_json,
including all enclosing IF/ELSE/EVALUATE conditions represented in the source
evidence.
Never remove an existing IF/THEN guard unless parsed_json proves the operation
is unconditional. Never REMOVE an MS merely because it has a guard absent from
its linked BR; that can mean the BR is incomplete. If the BR matches the parsed
guard and operation, return KEEP.
For MS transitions, the implication antecedent must use OLD/pre-state values
and the consequence must contain exactly one VARIABLE-NEW target. Do not weaken
a property to TRUE outside contradiction mode.

Return one JSON object only:
{
  "root_cause": "precise shared or per-candidate diagnosis",
  "confidence": 0.0,
  "layer_review": "incorrect|correct|uncertain",
  "operations": [
    {
      "action": "UPDATE|REMOVE|KEEP",
      "{identity_field}": "candidate identity",
      "new_{target_field}": "required for UPDATE only",
      "evidence_ids": ["read-only or parsed evidence identifiers"],
      "reason": "source-grounded reason"
    }
  ]
}
Every writable candidate must appear exactly once. No operation may target a
non-candidate.

CONTEXT:
{context}
````

### P4.2.3 Assertion-Patch LLM Fallback Prompt

Used only when the deterministic `ms_expression_to_assert_body` conversion of
a corrected MS expression fails validation. The LLM rewrites only the Boolean
body inside `assert(...)`, not the full file.

````text
Here is a single assertion statement:

assert({old_body});

The math spec {ms_id} changed from:
  OLD: {old_ssa}
  NEW: {new_ssa}

Rewrite ONLY the boolean expression that should go inside assert(...) using
!(P) || (Q) for IMPLIES, && for AND, || for OR, ! for NOT and == for =.
Keep every -OLD / -NEW name exactly. Return ONLY that expression — no
'assert(' wrapper, no semicolon, no markdown.
````

### P4.2.4 Assertion Full-File Fallback Prompt

Used as a last resort when the target `assert()` statement cannot be isolated
by index or literal-overlap matching.

````text
Here is the full assertions file:

{assertions_content}

The math spec {ms_id} had its expression changed from:
  OLD: {old_ssa}
  NEW: {new_ssa}

Rewrite ONLY the assert() statement(s) that encode this math spec to reflect
the new expression. Return the COMPLETE updated assertions file. No markdown,
no comments, only assert(...); lines.
````

---

## P4.3 Placeholders

| Placeholder             | Meaning                                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `{ce_vars}`             | JSON-serialised counterexample variable map produced by Z3 (triage LLM fallback)                                             |
| `{br_summary}`          | Newline-separated `id: rule[:120]` for every surviving candidate BR (triage LLM fallback only, never the full rule set)      |
| `{context}`             | JSON-serialised layer context object: writable candidates, read-only references, counterexample, repair history, permissions |
| `{layer}`               | Active repair layer: `BR`, `MS`, or `ASSERTION`                                                                               |
| `{identity_field}`      | Key used to identify a candidate in plan operations: `id` for BR/MS, `index` for ASSERTION                                   |
| `{target_field}`        | Field name for the corrected value in plan operations: `rule`, `expression`, or `body`                                        |
| `{ms_id}`               | Math-specification ID being reviewed or patched                                                                               |
| `{kind}`                | Specification kind (`transition`, `precondition`, `invariant`, or `postcondition`)                                            |
| `{description}`         | Description field of the math spec under review                                                                               |
| `{expression}`          | Current formal expression from `math_specs.json`                                                                              |
| `{sibling_expressions}` | Expressions of other math specs Z3 identified as mutually contradictory with the spec under review                            |
| `{feedback}`            | Rejection reason from the most recent failed validation attempt, fed back for a single retry                                  |
| `{old_body}`            | The existing `assert(...)` body being replaced (assertion-patch fallback)                                                     |
| `{old_ssa}`             | The previous MS expression before the correction                                                                              |
| `{new_ssa}`             | The corrected MS expression                                                                                                   |
| `{assertions_content}`  | The full current content of `assertions.txt` (full-file fallback only)                                                        |

## P4.4 Reproducibility

- **Model:** accessed through the Azure OpenAI Chat Completions API.
- **Temperature:** 0.0 (deterministic).
- **Repair rounds:** each BR, MS, and assertion correction receives at most one
  validation retry with the specific rejection reason before the original text
  is preserved and the rejection is recorded in the repair log without
  corrupting downstream state.
- **Assertion patching:** after an MS correction, the matching `assert()`
  statement is located by index (assertion `i` corresponds to `math_specs[i]`)
  and replaced in place; the LLM fallback prompt (P4.2.4) is used only when
  deterministic conversion fails validation; the full-file fallback (P4.2.5)
  is used only when the target statement cannot be isolated. The entire
  assertion file is test-compiled before anything is written.
- **Cascade:** a BR REMOVE cascades to remove all linked MS and assertion
  entries deterministically. A BR UPDATE triggers targeted regeneration of the
  linked MS and assertion via the same P2/P3 prompts on the single affected
  pair. All mutable artifacts are snapshotted before any write; any
  compile error restores all files from the snapshot.