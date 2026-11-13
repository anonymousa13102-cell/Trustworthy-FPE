#!/usr/bin/env python3
import z3
import time


def run_smt_verification():
    solver = z3.Solver()
    print('[Z3 Runtime] Initializing symbolic verification matrix...', flush=True)

    # Program: FIBBASE

    # Bool symbols
    COND_1, COND_2, COND_3 = z3.Bools('COND_1 COND_2 COND_3')

    # Int symbols
    LK_ANT_0, LK_ATU_0, LK_FIB_0, LK_FIB_1, LK_FIB_2, LK_FIB_3, LK_FIB_4, LK_FIB_5, LK_FIB_6, LK_FIB_7, LK_FIB_8, LK_FIB_9, LK_NUM_0, LS_ATU_0, LS_ATU_1, LS_ATU_2, LS_ATU_3, LS_NUM_0, LS_NUM_1, LS_NUM_2, LS_NUM_3, LS_PRX_0, LS_PRX_1, LS_PRX_2, LS_PRX_3, LS_PRX_4, LS_PRX_5 = z3.Ints('LK_ANT_0 LK_ATU_0 LK_FIB_0 LK_FIB_1 LK_FIB_2 LK_FIB_3 LK_FIB_4 LK_FIB_5 LK_FIB_6 LK_FIB_7 LK_FIB_8 LK_FIB_9 LK_NUM_0 LS_ATU_0 LS_ATU_1 LS_ATU_2 LS_ATU_3 LS_NUM_0 LS_NUM_1 LS_NUM_2 LS_NUM_3 LS_PRX_0 LS_PRX_1 LS_PRX_2 LS_PRX_3 LS_PRX_4 LS_PRX_5')

    FIBBASE = z3.Function('FIBBASE', z3.IntSort(), z3.IntSort(), z3.IntSort(), z3.IntSort())

    # =========================================================
    # PART 1: COBOL program behavior
    # =========================================================

    COBOL_PROGRAM = z3.And(
        # COBOL data-domain constraint
        LK_ANT_0 >= 0,
        # COBOL data-domain constraint
        LK_ANT_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_ATU_0 >= 0,
        # COBOL data-domain constraint
        LK_ATU_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_0 >= 0,
        # COBOL data-domain constraint
        LK_FIB_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_1 >= 0,
        # COBOL data-domain constraint
        LK_FIB_1 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_2 >= 0,
        # COBOL data-domain constraint
        LK_FIB_2 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_3 >= 0,
        # COBOL data-domain constraint
        LK_FIB_3 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_4 >= 0,
        # COBOL data-domain constraint
        LK_FIB_4 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_5 >= 0,
        # COBOL data-domain constraint
        LK_FIB_5 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_6 >= 0,
        # COBOL data-domain constraint
        LK_FIB_6 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_7 >= 0,
        # COBOL data-domain constraint
        LK_FIB_7 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_8 >= 0,
        # COBOL data-domain constraint
        LK_FIB_8 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_FIB_9 >= 0,
        # COBOL data-domain constraint
        LK_FIB_9 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LK_NUM_0 >= 0,
        # COBOL data-domain constraint
        LK_NUM_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_ATU_0 >= 0,
        # COBOL data-domain constraint
        LS_ATU_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_ATU_1 >= 0,
        # COBOL data-domain constraint
        LS_ATU_1 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_ATU_2 >= 0,
        # COBOL data-domain constraint
        LS_ATU_2 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_ATU_3 >= 0,
        # COBOL data-domain constraint
        LS_ATU_3 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_NUM_0 >= 0,
        # COBOL data-domain constraint
        LS_NUM_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_NUM_1 >= 0,
        # COBOL data-domain constraint
        LS_NUM_1 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_NUM_2 >= 0,
        # COBOL data-domain constraint
        LS_NUM_2 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_NUM_3 >= 0,
        # COBOL data-domain constraint
        LS_NUM_3 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_PRX_0 >= 0,
        # COBOL data-domain constraint
        LS_PRX_0 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_PRX_1 >= 0,
        # COBOL data-domain constraint
        LS_PRX_1 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_PRX_2 >= 0,
        # COBOL data-domain constraint
        LS_PRX_2 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_PRX_3 >= 0,
        # COBOL data-domain constraint
        LS_PRX_3 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_PRX_4 >= 0,
        # COBOL data-domain constraint
        LS_PRX_4 < 100000000000000000000000000000000000000,
        # COBOL data-domain constraint
        LS_PRX_5 >= 0,
        # COBOL data-domain constraint
        LS_PRX_5 < 100000000000000000000000000000000000000,
        # MS1: IF condition
        COND_1 == (LK_NUM_0 == 0),
        # MS2: COMPUTE LK-FIB = LK-ANT
        LK_FIB_1 == LK_ANT_0,
        # MS3: ELSE-IF condition 1
        COND_2 == (z3.And(z3.Not(COND_1), LK_NUM_0 == 1)),
        # MS4: COMPUTE LK-FIB = LK-ATU
        LK_FIB_2 == LK_ATU_0,
        # MS5: ELSE-IF condition 2
        COND_3 == (z3.And(z3.Not(COND_1), z3.Not(COND_2), LK_NUM_0 == 2)),
        # MS6: COMPUTE LS-PRX = LK-ANT + LK-ATU
        LS_PRX_1 == LK_ANT_0 + LK_ATU_0,
        # MS7: COMPUTE LK-FIB = LS-PRX
        LK_FIB_3 == LS_PRX_1,
        # MS8: MOVE LK-ATU TO LS-ATU
        LS_ATU_1 == LK_ATU_0,
        # MS9: COMPUTE LS-NUM = LK-NUM - 1
        LS_NUM_1 == LK_NUM_0 - 1,
        # MS10: COMPUTE LS-PRX = LK-ANT + LK-ATU
        LS_PRX_2 == LK_ANT_0 + LK_ATU_0,
        # MS11: COMPUTE LK-FIB = NUMVAL ( FIBBASE ( LS-NUM , LS-ATU , LS-PRX ) )
        LK_FIB_4 == FIBBASE(LS_NUM_1, LS_ATU_1, LS_PRX_2),
        # MS12: Merge LK_FIB after IF block
        LK_FIB_5 == z3.If(COND_1, LK_FIB_1, z3.If(COND_2, LK_FIB_2, z3.If(COND_3, LK_FIB_3, LK_FIB_4))),
        # MS13: Merge LS_ATU after IF block
        LS_ATU_2 == z3.If(COND_1, LS_ATU_0, z3.If(COND_2, LS_ATU_0, z3.If(COND_3, LS_ATU_0, LS_ATU_1))),
        # MS14: Merge LS_NUM after IF block
        LS_NUM_2 == z3.If(COND_1, LS_NUM_0, z3.If(COND_2, LS_NUM_0, z3.If(COND_3, LS_NUM_0, LS_NUM_1))),
        # MS15: Merge LS_PRX after IF block
        LS_PRX_3 == z3.If(COND_1, LS_PRX_0, z3.If(COND_2, LS_PRX_0, z3.If(COND_3, LS_PRX_1, LS_PRX_2))),
        # MS16: Effective LK_FIB after 'COMPUTE LK-FIB = LK-ANT' (assertion 0)
        LK_FIB_6 == z3.If(COND_1, LK_FIB_1, LK_FIB_0),
        # MS17: Effective LK_FIB after 'COMPUTE LK-FIB = LK-ATU' (assertion 1)
        LK_FIB_7 == z3.If(COND_2, LK_FIB_2, LK_FIB_0),
        # MS18: Effective LS_PRX after 'COMPUTE LS-PRX = LK-ANT + LK-ATU' (assertion 2)
        LS_PRX_4 == z3.If(COND_3, LS_PRX_1, LS_PRX_0),
        # MS19: Effective LK_FIB after 'COMPUTE LK-FIB = LS-PRX' (assertion 3)
        LK_FIB_8 == z3.If(COND_3, LK_FIB_3, LK_FIB_0),
        # MS20: Effective LS_ATU after 'MOVE LK-ATU TO LS-ATU' (assertion 4)
        LS_ATU_3 == z3.If(z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3)), LS_ATU_1, LS_ATU_0),
        # MS21: Effective LS_NUM after 'COMPUTE LS-NUM = LK-NUM - 1' (assertion 5)
        LS_NUM_3 == z3.If(z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3)), LS_NUM_1, LS_NUM_0),
        # MS22: Effective LS_PRX after 'COMPUTE LS-PRX = LK-ANT + LK-ATU' (assertion 6)
        LS_PRX_5 == z3.If(z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3)), LS_PRX_2, LS_PRX_0),
        # MS23: Effective LK_FIB after 'COMPUTE LK-FIB = NUMVAL ( FIBBASE ( LS-NUM , LS-ATU , LS-PRX ) )' (assertion 7)
        LK_FIB_9 == z3.If(z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3)), LK_FIB_4, LK_FIB_0)
    )

    # =========================================================
    # PART 2: Safety property assertion
    # =========================================================

    _ASSERT_EXPRS = [
        z3.Or(z3.Not(LK_NUM_0 == 0), LK_FIB_6 == LK_ANT_0),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), LK_NUM_0 == 1)), LK_FIB_7 == LK_ATU_0),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), LK_NUM_0 == 2)), LS_PRX_4 == LK_ANT_0 + LK_ATU_0),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), LK_NUM_0 == 2)), LK_FIB_8 == LS_PRX_1),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LS_ATU_3 == LK_ATU_0),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LS_NUM_3 == LK_NUM_0 - 1),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LS_PRX_5 == LK_ANT_0 + LK_ATU_0),
        z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LK_FIB_9 == FIBBASE(LS_NUM_1, LS_ATU_1, LS_PRX_2)),
    ]

    # Every individual proof obligation: (assertion index, kind, expr).
    #   postcondition  : the assertion itself, with TARGET-NEW bound to
    #                    the effective value after the operation.
    #   guard_mismatch : the IMPLIES antecedent must be equivalent to
    #                    the operation's real execution path condition.
    _CHECKS = [
        (0, 'postcondition', z3.Or(z3.Not(LK_NUM_0 == 0), LK_FIB_6 == LK_ANT_0)),
        (0, 'guard_mismatch', ((COND_1) == (LK_NUM_0 == 0))),
        (1, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), LK_NUM_0 == 1)), LK_FIB_7 == LK_ATU_0)),
        (1, 'guard_mismatch', ((COND_2) == (z3.And(z3.Not(LK_NUM_0 == 0), LK_NUM_0 == 1)))),
        (2, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), LK_NUM_0 == 2)), LS_PRX_4 == LK_ANT_0 + LK_ATU_0)),
        (2, 'guard_mismatch', ((COND_3) == (z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), LK_NUM_0 == 2)))),
        (3, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), LK_NUM_0 == 2)), LK_FIB_8 == LS_PRX_1)),
        (3, 'guard_mismatch', ((COND_3) == (z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), LK_NUM_0 == 2)))),
        (4, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LS_ATU_3 == LK_ATU_0)),
        (4, 'guard_mismatch', ((z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))) == (z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))))),
        (5, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LS_NUM_3 == LK_NUM_0 - 1)),
        (5, 'guard_mismatch', ((z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))) == (z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))))),
        (6, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LS_PRX_5 == LK_ANT_0 + LK_ATU_0)),
        (6, 'guard_mismatch', ((z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))) == (z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))))),
        (7, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))), LK_FIB_9 == FIBBASE(LS_NUM_1, LS_ATU_1, LS_PRX_2))),
        (7, 'guard_mismatch', ((z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))) == (z3.And(z3.Not(LK_NUM_0 == 0), z3.Not(LK_NUM_0 == 1), z3.Not(LK_NUM_0 == 2))))),
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
    _spec_solver.add(LK_ANT_0 >= 0)
    _spec_solver.add(LK_ANT_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_ATU_0 >= 0)
    _spec_solver.add(LK_ATU_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_0 >= 0)
    _spec_solver.add(LK_FIB_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_1 >= 0)
    _spec_solver.add(LK_FIB_1 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_2 >= 0)
    _spec_solver.add(LK_FIB_2 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_3 >= 0)
    _spec_solver.add(LK_FIB_3 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_4 >= 0)
    _spec_solver.add(LK_FIB_4 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_5 >= 0)
    _spec_solver.add(LK_FIB_5 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_6 >= 0)
    _spec_solver.add(LK_FIB_6 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_7 >= 0)
    _spec_solver.add(LK_FIB_7 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_8 >= 0)
    _spec_solver.add(LK_FIB_8 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_FIB_9 >= 0)
    _spec_solver.add(LK_FIB_9 < 100000000000000000000000000000000000000)
    _spec_solver.add(LK_NUM_0 >= 0)
    _spec_solver.add(LK_NUM_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_ATU_0 >= 0)
    _spec_solver.add(LS_ATU_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_ATU_1 >= 0)
    _spec_solver.add(LS_ATU_1 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_ATU_2 >= 0)
    _spec_solver.add(LS_ATU_2 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_ATU_3 >= 0)
    _spec_solver.add(LS_ATU_3 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_NUM_0 >= 0)
    _spec_solver.add(LS_NUM_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_NUM_1 >= 0)
    _spec_solver.add(LS_NUM_1 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_NUM_2 >= 0)
    _spec_solver.add(LS_NUM_2 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_NUM_3 >= 0)
    _spec_solver.add(LS_NUM_3 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_PRX_0 >= 0)
    _spec_solver.add(LS_PRX_0 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_PRX_1 >= 0)
    _spec_solver.add(LS_PRX_1 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_PRX_2 >= 0)
    _spec_solver.add(LS_PRX_2 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_PRX_3 >= 0)
    _spec_solver.add(LS_PRX_3 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_PRX_4 >= 0)
    _spec_solver.add(LS_PRX_4 < 100000000000000000000000000000000000000)
    _spec_solver.add(LS_PRX_5 >= 0)
    _spec_solver.add(LS_PRX_5 < 100000000000000000000000000000000000000)

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
        (0, COND_1),
        (1, COND_2),
        (2, COND_3),
        (3, COND_3),
        (4, z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))),
        (5, z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))),
        (6, z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))),
        (7, z3.And(z3.Not(COND_1), z3.Not(COND_2), z3.Not(COND_3))),
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