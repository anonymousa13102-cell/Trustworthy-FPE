# Prompt P2: Mathematical Specification Generation

P2 converts each SBVR business rule (output of P1) into a local mathematical
verification property expressed in an OLD/NEW variable contract. The
deterministic SMT compiler downstream handles numbered SSA versions and branch
merges; P2 produces only the one-operation pre/post view of each rule. The
parsed COBOL AST is provided as a secondary authority for name resolution,
declaration lookup, and execution-order verification, but every condition and
formula in the output must derive from the business-rule text, not from the AST.

---

## P2.1 Prompt

````text
You convert COBOL business rules into local mathematical verification
properties.

INPUTS:
1. DETERMINISTIC AST STRUCTURAL JSON
2. BUSINESS RULES

Use BUSINESS RULES as the authoritative functional source, including the exact
condition representation used by each rule. Use the AST only to verify COBOL
names, declarations, types, literals, formulas, execution order, statement
structure, and later assignments.

Do not use the AST to rewrite a business-rule condition into a different but
equivalent representation. In particular, if a level-88 condition-name has
already been expanded in a business rule into comparisons over its parent data
item, preserve those comparisons and do not restore the level-88 name.

Never invent behavior.

PROPERTY KINDS:
- precondition: an explicit requirement that must hold before an operation.
  An IF condition alone is not a precondition.
- invariant: an explicit property required to remain true across applicable
  states. Assigning a constant does not by itself create an invariant.
  If a supplied business rule describes a non-assigning control-flow effect,
  use invariant as the existing schema-compatible classification. Preserve its
  complete triggering condition using OLD values and preserve the control-flow
  consequence in the description. Do not invent a stored variable or NEW
  target.
- transition: the local effect of MOVE, ADD, SUBTRACT, COMPUTE, initialization,
  status update, or branch update.
- postcondition: an explicit final guarantee. Use this only when the source
  states a final result or the AST proves that it cannot be overwritten.

CLASSIFICATION:
1. Assignments, calculations, initializations, and branch updates are normally
   transitions.
2. If a target may be assigned later, use transition.
3. If finality is uncertain, use transition.
4. Never turn an IF condition into a separate precondition.
5. Generate at least one specification for every supplied business rule.
6. When the represented operation assigns a declared stored variable, that
   variable must be TARGET-NEW.
7. If a conditional rule describes a control-flow effect without assigning a
   declared stored variable, classify it as an invariant. Preserve the complete
   triggering condition using OLD values and IMPLIES. Use TRUE as the Boolean
   control-flow consequence. Preserve the actual control-flow effect in the
   description. Do not invent a NEW target, control-state variable, or
   assignment.

LOCAL OLD/NEW CONTRACT:
1. Preserve original COBOL variable names exactly.
2. Do not generate numbered SSA names such as BALANCE_0 or STATUS-CODE_2.
3. Do not generate ITE, PHI, COND, PATH, or BRANCH symbols.
4. OLD and NEW are local to the one operation represented by the current rule.
5. If the operation assigns a declared stored variable, that variable must be
   TARGET-NEW. A non-assigning control-flow invariant has no NEW target.
6. Every stored variable read by the operation must be VARIABLE-OLD, including:
   - variables in the branch condition
   - the previous value of the target
   - operands used to calculate the result
   - values assigned by earlier operations and consumed by this operation
7. Never use TARGET-OLD as the assignment result.
8. Never use a non-target VARIABLE-NEW.
9. Never leave a declared stored variable unsuffixed.
10. Do not add OLD or NEW to constants, literals, keywords, or
    level-88 condition-names.
11. Do not generate frame conditions for unchanged variables.
12. The deterministic SMT compiler will map OLD to the exact state before the
    matching COBOL operation and NEW to the exact state after it.

ASSIGNMENT PATTERNS:
- MOVE literal TO TARGET:
  TARGET-NEW = literal
- MOVE SOURCE TO TARGET:
  TARGET-NEW = SOURCE-OLD
- MOVE indexed/table SOURCE(INDEX) TO TARGET:
  TARGET-NEW = SOURCE-OLD(INDEX-OLD)
  Apply OLD to both the declared table variable and every declared variable
  used inside its parentheses. Preserve numeric subscripts unchanged.
- ADD SOURCE TO TARGET:
  TARGET-NEW = TARGET-OLD + SOURCE-OLD
- SUBTRACT SOURCE FROM TARGET:
  TARGET-NEW = TARGET-OLD - SOURCE-OLD
- COMPUTE TARGET = expression:
  TARGET-NEW = expression-using-OLD-values

CONDITIONAL RULES:
For IF condition THEN consequence, generate:

(condition-using-OLD-values) IMPLIES (consequence)

For a conditional control-flow rule that does not assign a declared stored
variable, generate:

(condition-using-OLD-values) IMPLIES TRUE

Classify such a rule as invariant. Preserve the actual control-flow effect in
the description. Do not invent a NEW target, control-state variable, or
assignment.

Preserve the complete supplied execution condition, including inherited NOT,
AND, OR, ELSE, and ELSE-IF guards. Never emit only the consequence. Never split
the condition into another property. Never rewrite implication as NOT P OR Q.

The antecedent of IMPLIES must be derived directly from the condition written
in the supplied business rule. Preserve its variables, comparisons, literals,
ranges, negations, AND/OR structure, and parentheses. The only permitted
transformation is adding -OLD to declared stored variables.

Do not replace the supplied condition with an equivalent condition-name,
abbreviation, inferred predicate, or condition taken from the AST.

PRECONDITIONS:
Use OLD for every stored input value, for example:
AMOUNT-OLD > 0

Do not generate NEW in a precondition.

INVARIANTS:
Preserve only invariants explicitly stated by the source rule. When an invariant
compares the state across the represented operation, use OLD and NEW exactly as
required, for example RATE-NEW = RATE-OLD. Do not infer invariants from constant
assignments or absence of later writes.

As a schema-compatible exception, classify a non-assigning control-flow rule as
an invariant. If it is conditional, preserve the complete triggering condition
using OLD values as the antecedent of IMPLIES and use TRUE as the consequence.
Preserve the actual control-flow effect in the description. Do not invent a NEW
target or stored control variable.

PRESERVATION:
1. Preserve every condition, formula, comparison, literal, assigned value, and
   operand order.
2. Preserve string literals exactly.
3. Do not simplify meaning.
4. Do not invent validations, assumptions, fallback behavior, range checks,
   overflow checks, division checks, or failure behavior.
5. Every expression must be Boolean.
6. Generate properties only from supplied business rules.
7. Do not reconstruct, restore, or substitute a COBOL level-88 condition-name
   when the supplied business rule already expresses that condition using its
   associated parent data item. Preserve the condition exactly as expressed in
   the business rule and add OLD to every stored parent-variable occurrence.
8. A level-88 condition-name may be preserved without OLD or NEW only when that
   condition-name explicitly occurs in the supplied business-rule text. Never
   use the AST to replace an expanded parent-variable condition with a level-88
   condition-name.
9. For a non-assigning control-flow rule, preserve its complete triggering
   condition in the expression and its actual control-flow consequence in the
   description.
10. Use IMPLIES TRUE only for a conditional control-flow rule that does not
    assign a declared stored variable.

Do not use:
==  &&  ||  !  ->  =>  THEN  WHEN  ITE  PHI

Do not use Python syntax, Z3 syntax, Markdown, numbered SSA names, or internal
symbols.

TRACEABILITY:
1. Every specification references exactly one valid business-rule ID.
2. Preserve business-rule order.
3. Do not combine unrelated rules.
4. Generate consecutive IDs beginning with MS1.

Return only valid JSON:
{
  "program_name": "...",
  "math_specs": [
    {
      "id": "MS1",
      "source_br_ids": ["BR1"],
      "kind": "precondition|invariant|transition|postcondition",
      "description": "...",
      "expression": "..."
    }
  ]
}

DETERMINISTIC AST STRUCTURAL JSON:
{parsed_json}

BUSINESS RULES INPUT:
{business_rules_json}
````

---

## P2.2 Placeholders

| Placeholder             | Meaning                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| `{parsed_json}`         | Full deterministic AST structural JSON for the program (variable declarations, section order, statements) |
| `{business_rules_json}` | JSON object produced by P1, containing the `business_rules` array and `variable_roles` map               |

## P2.3 Reproducibility

- **Model:** accessed through the Azure OpenAI Chat Completions API.
- **Temperature:** 0.0 (deterministic).
- **Post-processing:** the raw JSON response is validated by a deterministic
  Python layer that checks each specification references exactly one valid BR ID,
  enforces the correct number of NEW targets per kind, rejects numbered SSA names
  and internal symbols, confirms all state-qualified variable names are declared,
  detects declared variables left without OLD/NEW, and rejects forbidden tokens
  (`==`, `&&`, `||`, `->`, `=>`). No partial output is written if any
  specification fails validation.