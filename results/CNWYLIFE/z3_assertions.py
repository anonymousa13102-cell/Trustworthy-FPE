#!/usr/bin/env python3
import z3
import time


def run_smt_verification():
    solver = z3.Solver()
    print('[Z3 Runtime] Initializing symbolic verification matrix...', flush=True)

    # Program: CNWYLIFE

    NG_COLUMN_0 = z3.Const('NG_COLUMN_0', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_COLUMN_1 = z3.Const('NG_COLUMN_1', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_COLUMN_2 = z3.Const('NG_COLUMN_2', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_COLUMN_3 = z3.Const('NG_COLUMN_3', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_COLUMN_4 = z3.Const('NG_COLUMN_4', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_COLUMN_5 = z3.Const('NG_COLUMN_5', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_COLUMN_6 = z3.Const('NG_COLUMN_6', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    NG_ROW_0 = z3.Const('NG_ROW_0', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    PG_COLUMN_0 = z3.Const('PG_COLUMN_0', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    PG_ROW_0 = z3.Const('PG_ROW_0', z3.ArraySort(z3.IntSort(), z3.StringSort()))
    PG_ROW_1 = z3.Const('PG_ROW_1', z3.ArraySort(z3.IntSort(), z3.StringSort()))

    # Bool symbols
    COND_1, COND_2 = z3.Bools('COND_1 COND_2')

    # Int symbols
    COLUMN_COUNTER_0, GENERATION_0, MAX_COLUMNS_0, MAX_GEN_0, MAX_ROWS_0, NEIGHBOR_COUNTER_0, NEIGHBOR_X_0, NEIGHBOR_Y_0, ROW_COUNTER_0, X_0, Y_0 = z3.Ints('COLUMN_COUNTER_0 GENERATION_0 MAX_COLUMNS_0 MAX_GEN_0 MAX_ROWS_0 NEIGHBOR_COUNTER_0 NEIGHBOR_X_0 NEIGHBOR_Y_0 ROW_COUNTER_0 X_0 Y_0')

    # String symbols
    BOUNDARY_0, DEAD_CELL_0, END_OF_FILE_FLAG_0, END_OF_FILE_FLAG_1, INITIAL_CONDX_RECORD_0, LIVING_CELL_0, NEXT_GENERATION_0, NEXT_GENERATION_1, PREVIOUS_GENERATION_0, PREVIOUS_GENERATION_1 = z3.Strings('BOUNDARY_0 DEAD_CELL_0 END_OF_FILE_FLAG_0 END_OF_FILE_FLAG_1 INITIAL_CONDX_RECORD_0 LIVING_CELL_0 NEXT_GENERATION_0 NEXT_GENERATION_1 PREVIOUS_GENERATION_0 PREVIOUS_GENERATION_1')

    # =========================================================
    # PART 1: COBOL program behavior
    # =========================================================

    COBOL_PROGRAM = z3.And(
        # COBOL data-domain constraint
        z3.Length(BOUNDARY_0) <= 1,
        # COBOL data-domain constraint
        COLUMN_COUNTER_0 >= 0,
        # COBOL data-domain constraint
        COLUMN_COUNTER_0 < 100,
        # COBOL data-domain constraint
        z3.Length(DEAD_CELL_0) <= 1,
        # COBOL data-domain constraint
        z3.Length(END_OF_FILE_FLAG_0) <= 1,
        # COBOL data-domain constraint
        z3.Length(END_OF_FILE_FLAG_1) <= 1,
        # COBOL data-domain constraint
        GENERATION_0 >= 0,
        # COBOL data-domain constraint
        GENERATION_0 < 1000,
        # COBOL data-domain constraint
        z3.Length(INITIAL_CONDX_RECORD_0) <= 80,
        # COBOL data-domain constraint
        z3.Length(LIVING_CELL_0) <= 1,
        # COBOL data-domain constraint
        MAX_COLUMNS_0 >= 0,
        # COBOL data-domain constraint
        MAX_COLUMNS_0 < 100,
        # COBOL data-domain constraint
        MAX_GEN_0 >= 0,
        # COBOL data-domain constraint
        MAX_GEN_0 < 1000,
        # COBOL data-domain constraint
        MAX_ROWS_0 >= 0,
        # COBOL data-domain constraint
        MAX_ROWS_0 < 100,
        # COBOL data-domain constraint
        NEIGHBOR_COUNTER_0 >= 0,
        # COBOL data-domain constraint
        NEIGHBOR_COUNTER_0 < 10,
        # COBOL data-domain constraint
        NEIGHBOR_X_0 >= 0,
        # COBOL data-domain constraint
        NEIGHBOR_X_0 < 100,
        # COBOL data-domain constraint
        NEIGHBOR_Y_0 >= 0,
        # COBOL data-domain constraint
        NEIGHBOR_Y_0 < 100,
        # COBOL data-domain constraint
        ROW_COUNTER_0 >= 0,
        # COBOL data-domain constraint
        ROW_COUNTER_0 < 100,
        # COBOL data-domain constraint
        X_0 < 10,
        # COBOL data-domain constraint
        Y_0 < 10,
        # COBOL table-subscript constraint
        COLUMN_COUNTER_0 >= 1,
        # COBOL table-subscript constraint
        COLUMN_COUNTER_0 <= 80,
        # COBOL table-subscript constraint
        ROW_COUNTER_0 >= 1,
        # COBOL table-subscript constraint
        ROW_COUNTER_0 <= 40,
        # MS1: Initial VALUE for max-rows
        MAX_ROWS_0 == 40,
        # MS2: Initial VALUE for max-columns
        MAX_COLUMNS_0 == 80,
        # MS3: Initial VALUE for max-gen
        MAX_GEN_0 == 357,
        # MS4: Initial VALUE for living-cell
        LIVING_CELL_0 == "*",
        # MS5: Initial VALUE for dead-cell
        DEAD_CELL_0 == ' ',
        # MS6: Initial VALUE for boundary
        BOUNDARY_0 == "X",
        # MS7: Initial VALUE for generation
        GENERATION_0 == 1,
        # MS8: Initial VALUE for row-counter
        ROW_COUNTER_0 == 1,
        # MS9: Initial VALUE for column-counter
        COLUMN_COUNTER_0 == 1,
        # MS10: Initial VALUE for neighbor-counter
        NEIGHBOR_COUNTER_0 == 0,
        # MS11: MOVE "F" TO end-of-file-flag
        END_OF_FILE_FLAG_1 == 'F',
        # MS12: MOVE initial-condx-record to pg-row ( row-counter )
        PG_ROW_1 == z3.Store(PG_ROW_0, ((ROW_COUNTER_0) - 1), INITIAL_CONDX_RECORD_0),
        # MS13: MOVE previous-generation to next-generation
        NEXT_GENERATION_1 == PREVIOUS_GENERATION_0,
        # MS14: IF condition
        COND_1 == (z3.Or(NEIGHBOR_COUNTER_0 == 2, NEIGHBOR_COUNTER_0 == 3)),
        # MS15: MOVE living-cell TO ng-column ( row-counter , column-counter )
        NG_COLUMN_1 == z3.Store(NG_COLUMN_0, ((((ROW_COUNTER_0) - 1)) * 80 + ((COLUMN_COUNTER_0) - 1)), LIVING_CELL_0),
        # MS16: MOVE dead-cell TO ng-column ( row-counter , column-counter )
        NG_COLUMN_2 == z3.Store(NG_COLUMN_0, ((((ROW_COUNTER_0) - 1)) * 80 + ((COLUMN_COUNTER_0) - 1)), DEAD_CELL_0),
        # MS17: Merge NG_COLUMN after IF block
        NG_COLUMN_3 == z3.If(COND_1, NG_COLUMN_1, NG_COLUMN_2),
        # MS18: MOVE next-generation TO previous-generation
        PREVIOUS_GENERATION_1 == NEXT_GENERATION_1,
        # MS19: IF condition
        COND_2 == (NEIGHBOR_COUNTER_0 == 3),
        # MS20: MOVE living-cell TO ng-column ( row-counter , column-counter )
        NG_COLUMN_4 == z3.Store(NG_COLUMN_3, ((((ROW_COUNTER_0) - 1)) * 80 + ((COLUMN_COUNTER_0) - 1)), LIVING_CELL_0),
        # MS21: MOVE dead-cell TO ng-column ( row-counter , column-counter )
        NG_COLUMN_5 == z3.Store(NG_COLUMN_3, ((((ROW_COUNTER_0) - 1)) * 80 + ((COLUMN_COUNTER_0) - 1)), DEAD_CELL_0),
        # MS22: Merge NG_COLUMN after IF block
        NG_COLUMN_6 == z3.If(COND_2, NG_COLUMN_4, NG_COLUMN_5)
    )

    # =========================================================
    # PART 2: Safety property assertion
    # =========================================================

    _ASSERT_EXPRS = [
        END_OF_FILE_FLAG_1 == 'F',
        z3.Select(PG_ROW_1, ROW_COUNTER_0 - 1) == INITIAL_CONDX_RECORD_0,
        NEXT_GENERATION_1 == PREVIOUS_GENERATION_0,
        PREVIOUS_GENERATION_1 == NEXT_GENERATION_1,
        z3.Or(z3.Not(COND_2), z3.Or(z3.Not(z3.Or(NEIGHBOR_COUNTER_0 == 2, NEIGHBOR_COUNTER_0 == 3)), z3.Select(NG_COLUMN_4, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == LIVING_CELL_0)),
        z3.Or(z3.Not(z3.And(z3.Not(COND_2))), z3.Or(z3.Or(NEIGHBOR_COUNTER_0 == 2, NEIGHBOR_COUNTER_0 == 3), z3.Select(NG_COLUMN_5, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == DEAD_CELL_0)),
        z3.Or(z3.Not(COND_1), z3.Or(z3.Not(NEIGHBOR_COUNTER_0 == 3), z3.Select(NG_COLUMN_1, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == LIVING_CELL_0)),
        z3.Or(z3.Not(z3.And(z3.Not(COND_1))), z3.Select(NG_COLUMN_2, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == DEAD_CELL_0),
    ]

    # Every individual proof obligation: (assertion index, kind, expr).
    #   postcondition  : the assertion itself, with TARGET-NEW bound to
    #                    the effective value after the operation.
    #   guard_mismatch : the IMPLIES antecedent must be equivalent to
    #                    the operation's real execution path condition.
    _CHECKS = [
        (0, 'postcondition', END_OF_FILE_FLAG_1 == 'F'),
        (1, 'postcondition', z3.Select(PG_ROW_1, ROW_COUNTER_0 - 1) == INITIAL_CONDX_RECORD_0),
        (2, 'postcondition', NEXT_GENERATION_1 == PREVIOUS_GENERATION_0),
        (3, 'postcondition', PREVIOUS_GENERATION_1 == NEXT_GENERATION_1),
        (4, 'postcondition', z3.Or(z3.Not(COND_2), z3.Or(z3.Not(z3.Or(NEIGHBOR_COUNTER_0 == 2, NEIGHBOR_COUNTER_0 == 3)), z3.Select(NG_COLUMN_4, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == LIVING_CELL_0))),
        (4, 'guard_mismatch', ((COND_2) == (z3.Or(NEIGHBOR_COUNTER_0 == 2, NEIGHBOR_COUNTER_0 == 3)))),
        (5, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(COND_2))), z3.Or(z3.Or(NEIGHBOR_COUNTER_0 == 2, NEIGHBOR_COUNTER_0 == 3), z3.Select(NG_COLUMN_5, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == DEAD_CELL_0))),
        (6, 'postcondition', z3.Or(z3.Not(COND_1), z3.Or(z3.Not(NEIGHBOR_COUNTER_0 == 3), z3.Select(NG_COLUMN_1, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == LIVING_CELL_0))),
        (6, 'guard_mismatch', ((COND_1) == (NEIGHBOR_COUNTER_0 == 3))),
        (7, 'postcondition', z3.Or(z3.Not(z3.And(z3.Not(COND_1))), z3.Select(NG_COLUMN_2, (ROW_COUNTER_0 - 1) * 80 + (COLUMN_COUNTER_0 - 1)) == DEAD_CELL_0)),
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
    _spec_solver.add(z3.Length(BOUNDARY_0) <= 1)
    _spec_solver.add(COLUMN_COUNTER_0 >= 0)
    _spec_solver.add(COLUMN_COUNTER_0 < 100)
    _spec_solver.add(z3.Length(DEAD_CELL_0) <= 1)
    _spec_solver.add(z3.Length(END_OF_FILE_FLAG_0) <= 1)
    _spec_solver.add(z3.Length(END_OF_FILE_FLAG_1) <= 1)
    _spec_solver.add(GENERATION_0 >= 0)
    _spec_solver.add(GENERATION_0 < 1000)
    _spec_solver.add(z3.Length(INITIAL_CONDX_RECORD_0) <= 80)
    _spec_solver.add(z3.Length(LIVING_CELL_0) <= 1)
    _spec_solver.add(MAX_COLUMNS_0 >= 0)
    _spec_solver.add(MAX_COLUMNS_0 < 100)
    _spec_solver.add(MAX_GEN_0 >= 0)
    _spec_solver.add(MAX_GEN_0 < 1000)
    _spec_solver.add(MAX_ROWS_0 >= 0)
    _spec_solver.add(MAX_ROWS_0 < 100)
    _spec_solver.add(NEIGHBOR_COUNTER_0 >= 0)
    _spec_solver.add(NEIGHBOR_COUNTER_0 < 10)
    _spec_solver.add(NEIGHBOR_X_0 >= 0)
    _spec_solver.add(NEIGHBOR_X_0 < 100)
    _spec_solver.add(NEIGHBOR_Y_0 >= 0)
    _spec_solver.add(NEIGHBOR_Y_0 < 100)
    _spec_solver.add(ROW_COUNTER_0 >= 0)
    _spec_solver.add(ROW_COUNTER_0 < 100)
    _spec_solver.add(X_0 < 10)
    _spec_solver.add(Y_0 < 10)
    _spec_solver.add(COLUMN_COUNTER_0 >= 1)
    _spec_solver.add(COLUMN_COUNTER_0 <= 80)
    _spec_solver.add(ROW_COUNTER_0 >= 1)
    _spec_solver.add(ROW_COUNTER_0 <= 40)

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
        (4, COND_2),
        (5, z3.And(z3.Not(COND_2))),
        (6, COND_1),
        (7, z3.And(z3.Not(COND_1))),
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