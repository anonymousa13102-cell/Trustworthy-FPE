#!/usr/bin/env python3
import z3
import time


def run_smt_verification():
    solver = z3.Solver()
    print('[Z3 Runtime] Initializing symbolic verification matrix...', flush=True)

    # Program: C03EX02

    # Bool symbols
    COND_1 = z3.Bool('COND_1')

    # Int symbols
    INPUT_WS_A, INPUT_WS_B, WS_A_0, WS_A_1, WS_B_0, WS_B_1, WS_DSP_R_0, WS_DSP_R_1, WS_DSP_R_2, WS_DSP_R_3, WS_DSP_R_4, WS_DSP_R_5, WS_R_0, WS_R_1, WS_R_2, WS_R_3, WS_R_4, WS_R_5, WS_R_6 = z3.Ints('INPUT_WS_A INPUT_WS_B WS_A_0 WS_A_1 WS_B_0 WS_B_1 WS_DSP_R_0 WS_DSP_R_1 WS_DSP_R_2 WS_DSP_R_3 WS_DSP_R_4 WS_DSP_R_5 WS_R_0 WS_R_1 WS_R_2 WS_R_3 WS_R_4 WS_R_5 WS_R_6')

    # String symbols
    INPUT_WS_ENTER, WS_ENTER_0, WS_ENTER_1 = z3.Strings('INPUT_WS_ENTER WS_ENTER_0 WS_ENTER_1')

    # =========================================================
    # PART 1: COBOL program behavior
    # =========================================================

    COBOL_PROGRAM = z3.And(
        # COBOL data-domain constraint
        WS_A_0 >= 0,
        # COBOL data-domain constraint
        WS_A_0 < 1000,
        # COBOL data-domain constraint
        WS_A_1 >= 0,
        # COBOL data-domain constraint
        WS_A_1 < 1000,
        # COBOL data-domain constraint
        WS_B_0 >= 0,
        # COBOL data-domain constraint
        WS_B_0 < 1000,
        # COBOL data-domain constraint
        WS_B_1 >= 0,
        # COBOL data-domain constraint
        WS_B_1 < 1000,
        # COBOL data-domain constraint
        z3.Length(WS_ENTER_0) <= 1,
        # COBOL data-domain constraint
        z3.Length(WS_ENTER_1) <= 1,
        # COBOL data-domain constraint
        WS_R_0 >= 0,
        # COBOL data-domain constraint
        WS_R_0 < 10000,
        # COBOL data-domain constraint
        WS_R_1 >= 0,
        # COBOL data-domain constraint
        WS_R_1 < 10000,
        # COBOL data-domain constraint
        WS_R_2 >= 0,
        # COBOL data-domain constraint
        WS_R_2 < 10000,
        # COBOL data-domain constraint
        WS_R_3 >= 0,
        # COBOL data-domain constraint
        WS_R_3 < 10000,
        # COBOL data-domain constraint
        WS_R_4 >= 0,
        # COBOL data-domain constraint
        WS_R_4 < 10000,
        # COBOL data-domain constraint
        WS_R_5 >= 0,
        # COBOL data-domain constraint
        WS_R_5 < 10000,
        # COBOL data-domain constraint
        WS_R_6 >= 0,
        # COBOL data-domain constraint
        WS_R_6 < 10000,
        # MS1: ACCEPT WS_A
        WS_A_1 == INPUT_WS_A,
        # MS2: ACCEPT WS_B
        WS_B_1 == INPUT_WS_B,
        # MS3: COMPUTE WS-R = WS-A + WS-B
        WS_R_1 == WS_A_1 + WS_B_1,
        # MS4: IF condition
        COND_1 == (WS_R_1 >= 10),
        # MS5: ADD 5 TO WS-R
        WS_R_2 == WS_R_1 + (5),
        # MS6: MOVE WS-R TO WS-DSP-R
        WS_DSP_R_1 == WS_R_2,
        # MS7: SUBTRACT 7 FROM WS-R
        WS_R_3 == WS_R_1 - (7),
        # MS8: MOVE WS-R TO WS-DSP-R
        WS_DSP_R_2 == WS_R_3,
        # MS9: Merge WS_DSP_R after IF block
        WS_DSP_R_3 == z3.If(COND_1, WS_DSP_R_1, WS_DSP_R_2),
        # MS10: Merge WS_R after IF block
        WS_R_4 == z3.If(COND_1, WS_R_2, WS_R_3),
        # MS11: ACCEPT WS_ENTER
        WS_ENTER_1 == INPUT_WS_ENTER,
        # MS12: Effective WS_R after 'ADD 5 TO WS-R' (assertion 1)
        WS_R_5 == z3.If(COND_1, WS_R_2, WS_R_1),
        # MS13: Effective WS_DSP_R after 'MOVE WS-R TO WS-DSP-R' (assertion 2)
        WS_DSP_R_4 == z3.If(COND_1, WS_DSP_R_1, WS_DSP_R_0),
        # MS14: Effective WS_R after 'SUBTRACT 7 FROM WS-R' (assertion 3)
        WS_R_6 == z3.If(z3.And(z3.Not(COND_1)), WS_R_3, WS_R_1),
        # MS15: Effective WS_DSP_R after 'MOVE WS-R TO WS-DSP-R' (assertion 4)
        WS_DSP_R_5 == z3.If(z3.And(z3.Not(COND_1)), WS_DSP_R_2, WS_DSP_R_0)
    )

    # =========================================================
    # PART 2: Safety property assertion
    # =========================================================

    _ASSERT_EXPRS = [
        WS_R_1 == WS_A_1 + WS_B_1,
        z3.Or(z3.Not(WS_R_1 >= 10), WS_R_5 == WS_R_1 + 5),
        z3.Or(z3.Not(WS_R_1 >= 10), WS_DSP_R_4 == WS_R_2),
        z3.Or(z3.Not(z3.Not(WS_R_1 >= 10)), WS_R_6 == WS_R_1 - 7),
        z3.Or(z3.Not(z3.Not(WS_R_1 >= 10)), WS_DSP_R_5 == WS_R_3),
    ]

    # Every individual proof obligation: (assertion index, kind, expr).
    #   postcondition  : the assertion itself, with TARGET-NEW bound to
    #                    the effective value after the operation.
    #   guard_mismatch : the IMPLIES antecedent must be equivalent to
    #                    the operation's real execution path condition.
    _CHECKS = [
        (0, 'postcondition', WS_R_1 == WS_A_1 + WS_B_1),
        (1, 'postcondition', z3.Or(z3.Not(WS_R_1 >= 10), WS_R_5 == WS_R_1 + 5)),
        (1, 'guard_mismatch', ((COND_1) == (WS_R_1 >= 10))),
        (2, 'postcondition', z3.Or(z3.Not(WS_R_1 >= 10), WS_DSP_R_4 == WS_R_2)),
        (2, 'guard_mismatch', z3.Or(((COND_1) == (WS_R_2 >= 10)), ((COND_1) == (WS_R_1 >= 10)))),
        (3, 'postcondition', z3.Or(z3.Not(z3.Not(WS_R_1 >= 10)), WS_R_6 == WS_R_1 - 7)),
        (3, 'guard_mismatch', ((z3.And(z3.Not(COND_1))) == (z3.Not(WS_R_1 >= 10)))),
        (4, 'postcondition', z3.Or(z3.Not(z3.Not(WS_R_1 >= 10)), WS_DSP_R_5 == WS_R_3)),
        (4, 'guard_mismatch', z3.Or(((z3.And(z3.Not(COND_1))) == (z3.Not(WS_R_3 >= 10))), ((z3.And(z3.Not(COND_1))) == (z3.Not(WS_R_1 >= 10))))),
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
    _spec_solver.add(WS_A_0 >= 0)
    _spec_solver.add(WS_A_0 < 1000)
    _spec_solver.add(WS_A_1 >= 0)
    _spec_solver.add(WS_A_1 < 1000)
    _spec_solver.add(WS_B_0 >= 0)
    _spec_solver.add(WS_B_0 < 1000)
    _spec_solver.add(WS_B_1 >= 0)
    _spec_solver.add(WS_B_1 < 1000)
    _spec_solver.add(z3.Length(WS_ENTER_0) <= 1)
    _spec_solver.add(z3.Length(WS_ENTER_1) <= 1)
    _spec_solver.add(WS_R_0 >= 0)
    _spec_solver.add(WS_R_0 < 10000)
    _spec_solver.add(WS_R_1 >= 0)
    _spec_solver.add(WS_R_1 < 10000)
    _spec_solver.add(WS_R_2 >= 0)
    _spec_solver.add(WS_R_2 < 10000)
    _spec_solver.add(WS_R_3 >= 0)
    _spec_solver.add(WS_R_3 < 10000)
    _spec_solver.add(WS_R_4 >= 0)
    _spec_solver.add(WS_R_4 < 10000)
    _spec_solver.add(WS_R_5 >= 0)
    _spec_solver.add(WS_R_5 < 10000)
    _spec_solver.add(WS_R_6 >= 0)
    _spec_solver.add(WS_R_6 < 10000)

    print('[Z3 Runtime] 1/3 Starting assertion consistency check...', flush=True)
    _started = time.perf_counter()
    _spec_status = _spec_solver.check()
    print(f'[Z3 Runtime] 1/3 Assertion consistency finished: {_spec_status} ({time.perf_counter() - _started:.2f}s)', flush=True)
    if _spec_status == z3.unknown:
        print(f'[Z3 Runtime] 1/3 Reason unknown: {_spec_solver.reason_unknown()}', flush=True)
    if _spec_status == z3.unsat:
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
        (1, COND_1),
        (2, COND_1),
        (3, z3.And(z3.Not(COND_1))),
        (4, z3.And(z3.Not(COND_1))),
    ]
    print(f'[Z3 Runtime] 2/3 Starting {len(_REACH)} reachability check(s)...', flush=True)
    for _position, (_idx, _pc) in enumerate(_REACH, start=1):
        print(f'[Z3 Runtime] 2/3 Reachability {_position}/{len(_REACH)} for assertion {_idx}...', flush=True)
        _rs = z3.Solver()
        _rs.add(COBOL_PROGRAM, _pc)
        _started = time.perf_counter()
        _reach_status = _rs.check()
        print(f'[Z3 Runtime] 2/3 Reachability assertion {_idx}: {_reach_status} ({time.perf_counter() - _started:.2f}s)', flush=True)
        if _reach_status == z3.unknown:
            print(f'[Z3 Runtime] 2/3 Reason unknown: {_rs.reason_unknown()}', flush=True)
        if _reach_status == z3.unsat:
            print(f'WARNING: assertion {_idx} targets an unreachable operation (vacuous)', flush=True)

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

    print('[Z3 Runtime] 3/3 Starting final verification...', flush=True)
    _started = time.perf_counter()
    status = solver.check()
    print(f'[Z3 Runtime] 3/3 Final verification finished: {status} ({time.perf_counter() - _started:.2f}s)', flush=True)

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

    print('UNKNOWN: The verification query could not be resolved.', solver.reason_unknown(), flush=True)
    return {
        'status': 'unknown',
        'model': None,
    }


if __name__ == '__main__':
    run_smt_verification()