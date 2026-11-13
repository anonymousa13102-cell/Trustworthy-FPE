#!/usr/bin/env python3
import z3
import time


def run_smt_verification():
    solver = z3.Solver()
    print('[Z3 Runtime] Initializing symbolic verification matrix...', flush=True)

    # Program: EMPPAY

    # Bool symbols
    COND_1, COND_2, COND_3 = z3.Bools('COND_1 COND_2 COND_3')

    # Int symbols
    EMP_HOURS_0, EMP_HOURS_1, REC_COUNTER_0 = z3.Ints('EMP_HOURS_0 EMP_HOURS_1 REC_COUNTER_0')

    # Real symbols
    EMP_HOURLY_RATE_0, EMP_HOURLY_RATE_1, EMP_OT_RATE_0, EMP_OT_RATE_1, EMP_OT_RATE_2, EMP_OT_RATE_3, EMP_OT_RATE_4, EMP_OT_RATE_5, EMP_OT_RATE_6, EMP_OT_RATE_7, EMP_PAY_MONTH_0, EMP_PAY_MONTH_1, EMP_PAY_WEEK_0, EMP_PAY_WEEK_1, EMP_REWARD_0, EMP_REWARD_1, EMP_REWARD_2, EMP_REWARD_3, EMP_REWARD_4, EMP_REWARD_5 = z3.Reals('EMP_HOURLY_RATE_0 EMP_HOURLY_RATE_1 EMP_OT_RATE_0 EMP_OT_RATE_1 EMP_OT_RATE_2 EMP_OT_RATE_3 EMP_OT_RATE_4 EMP_OT_RATE_5 EMP_OT_RATE_6 EMP_OT_RATE_7 EMP_PAY_MONTH_0 EMP_PAY_MONTH_1 EMP_PAY_WEEK_0 EMP_PAY_WEEK_1 EMP_REWARD_0 EMP_REWARD_1 EMP_REWARD_2 EMP_REWARD_3 EMP_REWARD_4 EMP_REWARD_5')

    # String symbols
    EMP_FNAME_0, EMP_FNAME_1, EMP_LNAME_0, EMP_LNAME_1, EMP_NAME_0, EMP_RECORD_0 = z3.Strings('EMP_FNAME_0 EMP_FNAME_1 EMP_LNAME_0 EMP_LNAME_1 EMP_NAME_0 EMP_RECORD_0')

    # =========================================================
    # PART 1: COBOL program behavior
    # =========================================================

    COBOL_PROGRAM = z3.And(
        # COBOL data-domain constraint
        z3.Length(EMP_FNAME_0) <= 15,
        # COBOL data-domain constraint
        z3.Length(EMP_FNAME_1) <= 15,
        # COBOL data-domain constraint
        EMP_HOURLY_RATE_0 >= 0,
        # COBOL data-domain constraint
        EMP_HOURLY_RATE_0 < 1000,
        # COBOL data-domain constraint
        EMP_HOURLY_RATE_1 >= 0,
        # COBOL data-domain constraint
        EMP_HOURLY_RATE_1 < 1000,
        # COBOL data-domain constraint
        EMP_HOURS_0 >= 0,
        # COBOL data-domain constraint
        EMP_HOURS_0 < 1000,
        # COBOL data-domain constraint
        EMP_HOURS_1 >= 0,
        # COBOL data-domain constraint
        EMP_HOURS_1 < 1000,
        # COBOL data-domain constraint
        z3.Length(EMP_LNAME_0) <= 15,
        # COBOL data-domain constraint
        z3.Length(EMP_LNAME_1) <= 15,
        # COBOL data-domain constraint
        EMP_OT_RATE_0 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_1 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_2 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_3 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_4 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_5 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_6 >= 0,
        # COBOL data-domain constraint
        EMP_OT_RATE_7 >= 0,
        # COBOL data-domain constraint
        EMP_PAY_MONTH_0 >= 0,
        # COBOL data-domain constraint
        EMP_PAY_MONTH_0 < 10000000,
        # COBOL data-domain constraint
        EMP_PAY_MONTH_1 >= 0,
        # COBOL data-domain constraint
        EMP_PAY_MONTH_1 < 10000000,
        # COBOL data-domain constraint
        EMP_PAY_WEEK_0 >= 0,
        # COBOL data-domain constraint
        EMP_PAY_WEEK_0 < 10000000,
        # COBOL data-domain constraint
        EMP_PAY_WEEK_1 >= 0,
        # COBOL data-domain constraint
        EMP_PAY_WEEK_1 < 10000000,
        # COBOL data-domain constraint
        EMP_REWARD_0 >= 0,
        # COBOL data-domain constraint
        EMP_REWARD_1 >= 0,
        # COBOL data-domain constraint
        EMP_REWARD_2 >= 0,
        # COBOL data-domain constraint
        EMP_REWARD_3 >= 0,
        # COBOL data-domain constraint
        EMP_REWARD_4 >= 0,
        # COBOL data-domain constraint
        EMP_REWARD_5 >= 0,
        # COBOL data-domain constraint
        REC_COUNTER_0 >= 0,
        # COBOL data-domain constraint
        REC_COUNTER_0 < 10,
        # MS1: Initial VALUE for EMP-FNAME
        EMP_FNAME_0 == 'FRANCISCO',
        # MS2: MOVE "Millard" TO EMP-FNAME
        EMP_FNAME_1 == 'Millard',
        # MS3: MOVE "Fillmore" TO EMP-LNAME
        EMP_LNAME_1 == 'Fillmore',
        # MS4: MOVE 19 TO EMP-HOURS
        EMP_HOURS_1 == 19,
        # MS5: MOVE 23.50 TO EMP-HOURLY-RATE
        EMP_HOURLY_RATE_1 == 23.5,
        # MS6: IF condition
        COND_1 == (EMP_HOURS_1 >= 40),
        # MS7: MOVE .25 TO EMP-OT-RATE
        EMP_OT_RATE_1 == 0.25,
        # MS8: ELSE-IF condition 1
        COND_2 == (z3.And(z3.Not(COND_1), EMP_HOURS_1 >= 50)),
        # MS9: MOVE .50 TO EMP-OT-RATE
        EMP_OT_RATE_2 == 0.5,
        # MS10: MOVE ZERO TO EMP-OT-RATE
        EMP_OT_RATE_3 == 0,
        # MS11: Merge EMP_OT_RATE after IF block
        EMP_OT_RATE_4 == z3.If(COND_1, EMP_OT_RATE_1, z3.If(COND_2, EMP_OT_RATE_2, EMP_OT_RATE_3)),
        # MS12: COMPUTE EMP-PAY-WEEK = ( EMP-HOURS * EMP-HOURLY-RATE ) * ( 1 + EMP-OT-RATE )
        EMP_PAY_WEEK_1 == EMP_HOURS_1 * EMP_HOURLY_RATE_1 * (1 + EMP_OT_RATE_4),
        # MS13: IF condition
        COND_3 == (EMP_HOURS_1 > 150),
        # MS14: MOVE .50 TO EMP-REWARD
        EMP_REWARD_1 == 0.5,
        # MS15: MOVE ZERO TO EMP-REWARD
        EMP_REWARD_2 == 0,
        # MS16: Merge EMP_REWARD after IF block
        EMP_REWARD_3 == z3.If(COND_3, EMP_REWARD_1, EMP_REWARD_2),
        # MS17: COMPUTE EMP-PAY-MONTH = ( EMP-PAY-WEEK * 4 ) * ( 1 + EMP-REWARD )
        EMP_PAY_MONTH_1 == EMP_PAY_WEEK_1 * 4 * (1 + EMP_REWARD_3),
        # MS18: Effective EMP_OT_RATE after 'MOVE .25 TO EMP-OT-RATE' (assertion 4)
        EMP_OT_RATE_5 == z3.If(COND_1, EMP_OT_RATE_1, EMP_OT_RATE_0),
        # MS19: Effective EMP_OT_RATE after 'MOVE .50 TO EMP-OT-RATE' (assertion 5)
        EMP_OT_RATE_6 == z3.If(COND_2, EMP_OT_RATE_2, EMP_OT_RATE_0),
        # MS20: Effective EMP_OT_RATE after 'MOVE ZERO TO EMP-OT-RATE' (assertion 6)
        EMP_OT_RATE_7 == z3.If(z3.And(z3.Not(COND_1), z3.Not(COND_2)), EMP_OT_RATE_3, EMP_OT_RATE_0),
        # MS21: Effective EMP_REWARD after 'MOVE .50 TO EMP-REWARD' (assertion 8)
        EMP_REWARD_4 == z3.If(COND_3, EMP_REWARD_1, EMP_REWARD_0),
        # MS22: Effective EMP_REWARD after 'MOVE ZERO TO EMP-REWARD' (assertion 9)
        EMP_REWARD_5 == z3.If(z3.And(z3.Not(COND_3)), EMP_REWARD_2, EMP_REWARD_0)
    )

    # =========================================================
    # PART 2: Safety property assertion
    # =========================================================

    _ASSERT_EXPRS = [
        EMP_FNAME_1 == 'Millard',
        EMP_LNAME_1 == 'Fillmore',
        EMP_HOURS_1 == 19,
        EMP_HOURLY_RATE_1 == 23.5,
        z3.Or(z3.Not(EMP_HOURS_1 >= 40), EMP_OT_RATE_5 == 0.25),
        z3.Or(z3.Not(z3.And(z3.Not(EMP_HOURS_1 >= 40), EMP_HOURS_1 >= 50)), EMP_OT_RATE_6 == 0.5),
        z3.Or(z3.Not(z3.And(z3.Not(EMP_HOURS_1 >= 40), z3.Not(EMP_HOURS_1 >= 50))), EMP_OT_RATE_7 == 0),
        EMP_PAY_WEEK_1 == EMP_HOURS_1 * EMP_HOURLY_RATE_1 * (1 + EMP_OT_RATE_4),
        z3.Or(z3.Not(EMP_HOURS_1 > 150), EMP_REWARD_4 == 0.5),
        z3.Or(z3.Not(z3.Not(EMP_HOURS_1 > 150)), EMP_REWARD_5 == 0),
        EMP_PAY_MONTH_1 == EMP_PAY_WEEK_1 * 4 * (1 + EMP_REWARD_3),
    ]

    # Every individual proof obligation: (assertion index, kind, expr).
    #   postcondition  : the assertion itself, with TARGET-NEW bound to
    #                    the effective value after the operation.
    #   guard_mismatch : the IMPLIES antecedent must be equivalent to
    #                    the operation's real execution path condition.
    _CHECKS = [
        (0, 'postcondition', EMP_FNAME_1 == 'Millard'),
        (1, 'postcondition', EMP_LNAME_1 == 'Fillmore'),
        (2, 'postcondition', EMP_HOURS_1 == 19),
        (3, 'postcondition', EMP_HOURLY_RATE_1 == 23.5),
        (4, 'postcondition', z3.Or(z3.Not(EMP_HOURS_1 >= 40), EMP_OT_RATE_5 == 0.25)),
        (4, 'guard_mismatch', ((COND_1) == (EMP_HOURS_1 >= 40))),
        (5, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(EMP_HOURS_1 >= 40), EMP_HOURS_1 >= 50)), EMP_OT_RATE_6 == 0.5)),
        (5, 'guard_mismatch', ((COND_2) == (z3.And(z3.Not(EMP_HOURS_1 >= 40), EMP_HOURS_1 >= 50)))),
        (6, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(EMP_HOURS_1 >= 40), z3.Not(EMP_HOURS_1 >= 50))), EMP_OT_RATE_7 == 0)),
        (6, 'guard_mismatch', ((z3.And(z3.Not(COND_1), z3.Not(COND_2))) == (z3.And(z3.Not(EMP_HOURS_1 >= 40), z3.Not(EMP_HOURS_1 >= 50))))),
        (7, 'postcondition', EMP_PAY_WEEK_1 == EMP_HOURS_1 * EMP_HOURLY_RATE_1 * (1 + EMP_OT_RATE_4)),
        (8, 'postcondition', z3.Or(z3.Not(EMP_HOURS_1 > 150), EMP_REWARD_4 == 0.5)),
        (8, 'guard_mismatch', ((COND_3) == (EMP_HOURS_1 > 150))),
        (9, 'postcondition', z3.Or(z3.Not(z3.Not(EMP_HOURS_1 > 150)), EMP_REWARD_5 == 0)),
        (9, 'guard_mismatch', ((z3.And(z3.Not(COND_3))) == (z3.Not(EMP_HOURS_1 > 150)))),
        (10, 'postcondition', EMP_PAY_MONTH_1 == EMP_PAY_WEEK_1 * 4 * (1 + EMP_REWARD_3)),
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
    _spec_solver.add(z3.Length(EMP_FNAME_0) <= 15)
    _spec_solver.add(z3.Length(EMP_FNAME_1) <= 15)
    _spec_solver.add(EMP_HOURLY_RATE_0 >= 0)
    _spec_solver.add(EMP_HOURLY_RATE_0 < 1000)
    _spec_solver.add(EMP_HOURLY_RATE_1 >= 0)
    _spec_solver.add(EMP_HOURLY_RATE_1 < 1000)
    _spec_solver.add(EMP_HOURS_0 >= 0)
    _spec_solver.add(EMP_HOURS_0 < 1000)
    _spec_solver.add(EMP_HOURS_1 >= 0)
    _spec_solver.add(EMP_HOURS_1 < 1000)
    _spec_solver.add(z3.Length(EMP_LNAME_0) <= 15)
    _spec_solver.add(z3.Length(EMP_LNAME_1) <= 15)
    _spec_solver.add(EMP_OT_RATE_0 >= 0)
    _spec_solver.add(EMP_OT_RATE_1 >= 0)
    _spec_solver.add(EMP_OT_RATE_2 >= 0)
    _spec_solver.add(EMP_OT_RATE_3 >= 0)
    _spec_solver.add(EMP_OT_RATE_4 >= 0)
    _spec_solver.add(EMP_OT_RATE_5 >= 0)
    _spec_solver.add(EMP_OT_RATE_6 >= 0)
    _spec_solver.add(EMP_OT_RATE_7 >= 0)
    _spec_solver.add(EMP_PAY_MONTH_0 >= 0)
    _spec_solver.add(EMP_PAY_MONTH_0 < 10000000)
    _spec_solver.add(EMP_PAY_MONTH_1 >= 0)
    _spec_solver.add(EMP_PAY_MONTH_1 < 10000000)
    _spec_solver.add(EMP_PAY_WEEK_0 >= 0)
    _spec_solver.add(EMP_PAY_WEEK_0 < 10000000)
    _spec_solver.add(EMP_PAY_WEEK_1 >= 0)
    _spec_solver.add(EMP_PAY_WEEK_1 < 10000000)
    _spec_solver.add(EMP_REWARD_0 >= 0)
    _spec_solver.add(EMP_REWARD_1 >= 0)
    _spec_solver.add(EMP_REWARD_2 >= 0)
    _spec_solver.add(EMP_REWARD_3 >= 0)
    _spec_solver.add(EMP_REWARD_4 >= 0)
    _spec_solver.add(EMP_REWARD_5 >= 0)
    _spec_solver.add(REC_COUNTER_0 >= 0)
    _spec_solver.add(REC_COUNTER_0 < 10)

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
        (4, COND_1),
        (5, COND_2),
        (6, z3.And(z3.Not(COND_1), z3.Not(COND_2))),
        (8, COND_3),
        (9, z3.And(z3.Not(COND_3))),
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