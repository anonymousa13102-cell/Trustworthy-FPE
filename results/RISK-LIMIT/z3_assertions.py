#!/usr/bin/env python3
import z3


def run_smt_verification():
    solver = z3.Solver()
    print('[Z3 Runtime] Initializing symbolic verification matrix...')

    # Program: RISK-LIMIT

    # Bool symbols
    COND_1, COND_2 = z3.Bools('COND_1 COND_2')

    # Int symbols
    LIMIT_AMT_0, LIMIT_AMT_1, LIMIT_AMT_2, LIMIT_AMT_3, LIMIT_AMT_4, LIMIT_AMT_5, RISK_CD_0 = z3.Ints('LIMIT_AMT_0 LIMIT_AMT_1 LIMIT_AMT_2 LIMIT_AMT_3 LIMIT_AMT_4 LIMIT_AMT_5 RISK_CD_0')

    # =========================================================
    # PART 1: COBOL program behavior
    # =========================================================

    COBOL_PROGRAM = z3.And(
        # COBOL data-domain constraint
        LIMIT_AMT_0 >= 0,
        # COBOL data-domain constraint
        LIMIT_AMT_0 < 10000000,
        # COBOL data-domain constraint
        LIMIT_AMT_1 >= 0,
        # COBOL data-domain constraint
        LIMIT_AMT_1 < 10000000,
        # COBOL data-domain constraint
        LIMIT_AMT_2 >= 0,
        # COBOL data-domain constraint
        LIMIT_AMT_2 < 10000000,
        # COBOL data-domain constraint
        LIMIT_AMT_3 >= 0,
        # COBOL data-domain constraint
        LIMIT_AMT_3 < 10000000,
        # COBOL data-domain constraint
        LIMIT_AMT_4 >= 0,
        # COBOL data-domain constraint
        LIMIT_AMT_4 < 10000000,
        # COBOL data-domain constraint
        LIMIT_AMT_5 >= 0,
        # COBOL data-domain constraint
        LIMIT_AMT_5 < 10000000,
        # COBOL data-domain constraint
        RISK_CD_0 >= 0,
        # COBOL data-domain constraint
        RISK_CD_0 < 100,
        # MS1: Initial VALUE for LIMIT-AMT
        LIMIT_AMT_0 == 0,
        # MS2: IF condition
        COND_1 == (z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)),
        # MS3: MOVE 500000 TO LIMIT-AMT
        LIMIT_AMT_1 == 500000,
        # MS4: ELSE-IF condition 1
        COND_2 == (z3.And(z3.Not(COND_1), z3.Or(RISK_CD_0 == 5, z3.And(RISK_CD_0 >= 7, RISK_CD_0 <= 9)))),
        # MS5: MOVE 50000 TO LIMIT-AMT
        LIMIT_AMT_2 == 50000,
        # MS6: Merge LIMIT_AMT after IF block
        LIMIT_AMT_3 == z3.If(COND_1, LIMIT_AMT_1, z3.If(COND_2, LIMIT_AMT_2, LIMIT_AMT_0)),
        # MS7: Effective LIMIT_AMT after 'MOVE 500000 TO LIMIT-AMT' (assertion 0)
        LIMIT_AMT_4 == z3.If(COND_1, LIMIT_AMT_1, LIMIT_AMT_0),
        # MS8: Effective LIMIT_AMT after 'MOVE 50000 TO LIMIT-AMT' (assertion 1)
        LIMIT_AMT_5 == z3.If(COND_2, LIMIT_AMT_2, LIMIT_AMT_0)
    )

    # =========================================================
    # PART 2: Safety property assertion
    # =========================================================

    _ASSERT_EXPRS = [
        z3.Or(z3.Not(z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)), LIMIT_AMT_4 == 500000),
        z3.Or(z3.Not(z3.And(z3.Not(z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)), z3.Or(RISK_CD_0 == 5, z3.And(RISK_CD_0 >= 7, RISK_CD_0 <= 9)))), LIMIT_AMT_5 == 50000),
    ]

    # Every individual proof obligation: (assertion index, kind, expr).
    #   postcondition  : the assertion itself, with TARGET-NEW bound to
    #                    the effective value after the operation.
    #   guard_mismatch : the IMPLIES antecedent must be equivalent to
    #                    the operation's real execution path condition.
    _CHECKS = [
        (0, 'postcondition', z3.Or(z3.Not(z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)), LIMIT_AMT_4 == 500000)),
        (0, 'guard_mismatch', ((COND_1) == (z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)))),
        (1, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)), z3.Or(RISK_CD_0 == 5, z3.And(RISK_CD_0 >= 7, RISK_CD_0 <= 9)))), LIMIT_AMT_5 == 50000)),
        (1, 'guard_mismatch', ((COND_2) == (z3.And(z3.Not(z3.And(RISK_CD_0 >= 1, RISK_CD_0 <= 3)), z3.Or(RISK_CD_0 == 5, z3.And(RISK_CD_0 >= 7, RISK_CD_0 <= 9)))))),
    ]

    ASSERTION = z3.And([_c[2] for _c in _CHECKS])

    # =========================================================
    # PART 2.5: Assertion self-consistency check
    #
    # Are the assertions jointly satisfiable at all, for SOME
    # legal input, independent of what this program actually
    # does? Two branch guards that are each written as an
    # unconditional universal truth (e.g. TRANS-TYPE = 'D' vs
    # TRANS-TYPE = 'W', both asserted unconditionally) can never
    # both hold, which makes the whole ASSERTION unsatisfiable
    # by itself -- Z3 would then report a 'counterexample' on
    # every single run regardless of whether the program is
    # actually correct. Catch that case distinctly here instead
    # of letting it masquerade as a real program bug.
    # =========================================================

    _spec_solver = z3.Solver()
    _spec_tags = []
    for _i, _expr in enumerate(_ASSERT_EXPRS):
        _tag = z3.Bool(f'_spec_{_i}')
        _spec_solver.assert_and_track(_expr, _tag)
        _spec_tags.append(_tag)
    _spec_solver.add(LIMIT_AMT_0 >= 0)
    _spec_solver.add(LIMIT_AMT_0 < 10000000)
    _spec_solver.add(LIMIT_AMT_1 >= 0)
    _spec_solver.add(LIMIT_AMT_1 < 10000000)
    _spec_solver.add(LIMIT_AMT_2 >= 0)
    _spec_solver.add(LIMIT_AMT_2 < 10000000)
    _spec_solver.add(LIMIT_AMT_3 >= 0)
    _spec_solver.add(LIMIT_AMT_3 < 10000000)
    _spec_solver.add(LIMIT_AMT_4 >= 0)
    _spec_solver.add(LIMIT_AMT_4 < 10000000)
    _spec_solver.add(LIMIT_AMT_5 >= 0)
    _spec_solver.add(LIMIT_AMT_5 < 10000000)
    _spec_solver.add(RISK_CD_0 >= 0)
    _spec_solver.add(RISK_CD_0 < 100)

    if _spec_solver.check() == z3.unsat:
        _core = {str(t) for t in _spec_solver.unsat_core()}
        _bad = [i for i, t in enumerate(_spec_tags) if str(t) in _core]
        print(
            'SPEC_CONTRADICTION: assertion indices', _bad,
            'are mutually unsatisfiable regardless of program behavior'
        )
        print('CONTRADICTORY_ASSERTION_INDICES:', _bad)
        return {
            'status': 'invalid_spec',
            'model': None,
            'contradictory_assertion_indices': _bad,
        }

    # Reachability: warn when an assertion targets an operation that
    # no program input can reach (such an assertion is vacuous).
    _REACH = [
        (0, COND_1),
        (1, COND_2),
    ]
    for _idx, _pc in _REACH:
        _rs = z3.Solver()
        _rs.add(COBOL_PROGRAM, _pc)
        if _rs.check() == z3.unsat:
            print(f'WARNING: assertion {_idx} targets an unreachable operation (vacuous)')

    # =========================================================
    # Verification query:
    #
    #     COBOL_PROGRAM AND NOT(ASSERTION)
    #
    # SAT   means a counterexample exists.
    # UNSAT means the assertion is verified.
    # =========================================================

    solver.add(
        z3.And(
            COBOL_PROGRAM,
            z3.Not(ASSERTION)
        )
    )

    status = solver.check()

    if status == z3.unsat:
        print('VERIFIED: The program satisfies the assertion.')
        return {
            'status': 'verified',
            'model': None,
        }

    if status == z3.sat:
        print('COUNTEREXAMPLE: ASSERTION VIOLATION DETECTED:')
        model = solver.model()
        print(model)
        _failed = []
        _failed_checks = []
        for _idx, _kind, _expr in _CHECKS:
            if z3.is_false(model.eval(_expr, model_completion=True)):
                print(f'FAILED_CHECK: assertion {_idx} {_kind}')
                _failed_checks.append((_idx, _kind))
                if _idx not in _failed:
                    _failed.append(_idx)
        print('FAILED_ASSERTION_INDICES:', sorted(_failed))
        return {
            'status': 'failed',
            'model': str(model),
            'failed_assertion_indices': sorted(_failed),
            'failed_checks': _failed_checks,
        }

    print('UNKNOWN: The verification query could not be resolved.')
    return {
        'status': 'unknown',
        'model': None,
    }


if __name__ == '__main__':
    run_smt_verification()