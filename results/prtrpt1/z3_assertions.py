#!/usr/bin/env python3
import time
import z3


def run_smt_verification():
    solver = z3.Solver()
    print('[Z3 Runtime] Initializing symbolic verification matrix...', flush=True)

    # PRTRPT1 symbolic inputs. The COPY-expanded status fields and level-88
    # conditions are absent from parsed.json, so they are explicit inputs here.
    WS_REPORT_GOOD, WS_MEMBER_GOOD, WS_MEMBER_OKAY = z3.Bools(
        'WS_REPORT_GOOD WS_MEMBER_GOOD WS_MEMBER_OKAY'
    )
    WS_REPORT_STATUS_0, WS_MEMBER_STATUS_0 = z3.Strings(
        'WS_REPORT_STATUS_0 WS_MEMBER_STATUS_0'
    )

    ABN_PARAGRAPH_0, ABN_PARAGRAPH_1, ABN_PARAGRAPH_2, ABN_PARAGRAPH_3 = z3.Strings(
        'ABN_PARAGRAPH_0 ABN_PARAGRAPH_1 ABN_PARAGRAPH_2 ABN_PARAGRAPH_3'
    )
    ABN_CODE_0, ABN_CODE_1, ABN_CODE_2, ABN_CODE_3 = z3.Strings(
        'ABN_CODE_0 ABN_CODE_1 ABN_CODE_2 ABN_CODE_3'
    )
    MEMBER_ID_0, MEMBER_NAME_0, MEMBER_GENDER_0 = z3.Strings(
        'MEMBER_ID_0 MEMBER_NAME_0 MEMBER_GENDER_0'
    )
    PRN_MEMBER_ID_0, PRN_MEMBER_ID_1 = z3.Strings('PRN_MEMBER_ID_0 PRN_MEMBER_ID_1')
    PRN_MEMBER_NAME_0, PRN_MEMBER_NAME_1 = z3.Strings('PRN_MEMBER_NAME_0 PRN_MEMBER_NAME_1')
    PRN_MEMBER_TYPE_0, PRN_MEMBER_TYPE_1 = z3.Strings('PRN_MEMBER_TYPE_0 PRN_MEMBER_TYPE_1')
    PRN_MEMBER_GENDER_0, PRN_MEMBER_GENDER_1 = z3.Strings('PRN_MEMBER_GENDER_0 PRN_MEMBER_GENDER_1')

    MEMBER_TYPE_0, LINE_COUNT_0, LINE_COUNT_1, LINE_COUNT_2, LINE_COUNT_3 = z3.Ints(
        'MEMBER_TYPE_0 LINE_COUNT_0 LINE_COUNT_1 LINE_COUNT_2 LINE_COUNT_3'
    )
    PAGE_COUNT_0, PAGE_COUNT_1, PAGE_COUNT_2 = z3.Ints(
        'PAGE_COUNT_0 PAGE_COUNT_1 PAGE_COUNT_2'
    )
    PRN_PAGE_NUM_0, PRN_PAGE_NUM_1 = z3.Ints('PRN_PAGE_NUM_0 PRN_PAGE_NUM_1')

    NEW_PAGE_REQUIRED = z3.And(LINE_COUNT_1 >= 40, LINE_COUNT_1 <= 99)

    COBOL_PROGRAM = z3.And(
        z3.Length(WS_REPORT_STATUS_0) <= 2,
        z3.Length(WS_MEMBER_STATUS_0) <= 2,
        z3.Length(ABN_PARAGRAPH_0) <= 4,
        z3.Length(ABN_CODE_0) <= 2,
        z3.Length(MEMBER_ID_0) <= 5,
        z3.Length(MEMBER_NAME_0) <= 20,
        z3.Length(MEMBER_GENDER_0) <= 1,
        MEMBER_TYPE_0 >= 0, MEMBER_TYPE_0 < 10,
        LINE_COUNT_0 >= 0, LINE_COUNT_0 < 100,
        PAGE_COUNT_0 >= 0, PAGE_COUNT_0 < 100,

        # 1010-Open-Report WHEN OTHER
        ABN_PARAGRAPH_1 == z3.If(z3.Not(WS_REPORT_GOOD), z3.StringVal('1010'), ABN_PARAGRAPH_0),
        ABN_CODE_1 == z3.If(z3.Not(WS_REPORT_GOOD), WS_REPORT_STATUS_0, ABN_CODE_0),

        # 1020-Open-Member-File WHEN OTHER
        ABN_PARAGRAPH_2 == z3.If(z3.Not(WS_MEMBER_GOOD), z3.StringVal('1020'), ABN_PARAGRAPH_1),
        ABN_CODE_2 == z3.If(z3.Not(WS_MEMBER_GOOD), WS_MEMBER_STATUS_0, ABN_CODE_1),

        # 6100-Print-Page-Headings
        LINE_COUNT_1 == 3,
        PAGE_COUNT_1 == PAGE_COUNT_0 + 1,

        # 5000-Read-Member-File WHEN OTHER
        ABN_PARAGRAPH_3 == z3.If(z3.Not(WS_MEMBER_OKAY), z3.StringVal('5000'), ABN_PARAGRAPH_2),
        ABN_CODE_3 == z3.If(z3.Not(WS_MEMBER_OKAY), WS_MEMBER_STATUS_0, ABN_CODE_2),

        # 6200-Print-Report-Body
        PRN_PAGE_NUM_1 == z3.If(NEW_PAGE_REQUIRED, PAGE_COUNT_1, PRN_PAGE_NUM_0),
        LINE_COUNT_2 == z3.If(NEW_PAGE_REQUIRED, 3, LINE_COUNT_1),
        PAGE_COUNT_2 == z3.If(NEW_PAGE_REQUIRED, PAGE_COUNT_1 + 1, PAGE_COUNT_1),
        PRN_MEMBER_ID_1 == MEMBER_ID_0,
        PRN_MEMBER_NAME_1 == MEMBER_NAME_0,
        PRN_MEMBER_TYPE_1 == z3.IntToStr(MEMBER_TYPE_0),
        PRN_MEMBER_GENDER_1 == MEMBER_GENDER_0,
        LINE_COUNT_3 == LINE_COUNT_2 + 1
    )

    # BR7 and BR8 are intentionally mutated to TRUE, so assertions 6 and 7
    # are unconditional even though the source operations are WHEN OTHER.
    _ASSERT_EXPRS = [
        z3.Or(WS_REPORT_GOOD, ABN_PARAGRAPH_1 == z3.StringVal('1010')),
        z3.Or(WS_REPORT_GOOD, ABN_CODE_1 == WS_REPORT_STATUS_0),
        z3.Or(WS_MEMBER_GOOD, ABN_PARAGRAPH_2 == z3.StringVal('1020')),
        z3.Or(WS_MEMBER_GOOD, ABN_CODE_2 == WS_MEMBER_STATUS_0),
        LINE_COUNT_1 == 3,
        PAGE_COUNT_1 == PAGE_COUNT_0 + 1,
        ABN_PARAGRAPH_3 == z3.StringVal('5000'),
        ABN_CODE_3 == WS_MEMBER_STATUS_0,
        z3.Or(z3.Not(NEW_PAGE_REQUIRED), PRN_PAGE_NUM_1 == PAGE_COUNT_1),
        z3.Or(z3.Not(NEW_PAGE_REQUIRED), LINE_COUNT_2 == 3),
        z3.Or(z3.Not(NEW_PAGE_REQUIRED), PAGE_COUNT_2 == PAGE_COUNT_1 + 1),
        PRN_MEMBER_ID_1 == MEMBER_ID_0,
        PRN_MEMBER_NAME_1 == MEMBER_NAME_0,
        PRN_MEMBER_TYPE_1 == z3.IntToStr(MEMBER_TYPE_0),
        PRN_MEMBER_GENDER_1 == MEMBER_GENDER_0,
        LINE_COUNT_3 == LINE_COUNT_2 + 1,
    ]

    _CHECKS = [(i, 'postcondition', expr) for i, expr in enumerate(_ASSERT_EXPRS)]
    _CHECKS.extend([
        (6, 'guard_mismatch', z3.BoolVal(False) == z3.Not(WS_MEMBER_OKAY)),
        (7, 'guard_mismatch', z3.BoolVal(False) == z3.Not(WS_MEMBER_OKAY)),
    ])
    ASSERTION = z3.And([entry[2] for entry in _CHECKS])

    _spec_solver = z3.Solver()
    _spec_tags = []
    for i, expr in enumerate(_ASSERT_EXPRS):
        tag = z3.Bool(f'_spec_{i}')
        _spec_solver.assert_and_track(expr, tag)
        _spec_tags.append(tag)
    print('[Z3 Runtime] 1/3 Starting assertion consistency check...', flush=True)
    started = time.perf_counter()
    spec_status = _spec_solver.check()
    print(f'[Z3 Runtime] 1/3 Assertion consistency finished: {spec_status} ({time.perf_counter() - started:.2f}s)', flush=True)
    if spec_status == z3.unsat:
        core = {str(t) for t in _spec_solver.unsat_core()}
        bad = [i for i, t in enumerate(_spec_tags) if str(t) in core]
        print('SPEC_CONTRADICTION: assertion indices', bad)
        print('CONTRADICTORY_ASSERTION_INDICES:', bad)
        return {'status': 'invalid_spec', 'model': None, 'contradictory_assertion_indices': bad}

    reachability = [
        (0, z3.Not(WS_REPORT_GOOD)), (1, z3.Not(WS_REPORT_GOOD)),
        (2, z3.Not(WS_MEMBER_GOOD)), (3, z3.Not(WS_MEMBER_GOOD)),
        (6, z3.Not(WS_MEMBER_OKAY)), (7, z3.Not(WS_MEMBER_OKAY)),
        (8, NEW_PAGE_REQUIRED), (9, NEW_PAGE_REQUIRED), (10, NEW_PAGE_REQUIRED),
    ]
    vacuous = []
    print(f'[Z3 Runtime] 2/3 Starting {len(reachability)} reachability check(s)...', flush=True)
    for pos, (idx, path) in enumerate(reachability, start=1):
        rs = z3.Solver(); rs.add(COBOL_PROGRAM, path)
        started = time.perf_counter(); reach_status = rs.check()
        print(f'[Z3 Runtime] 2/3 Reachability {pos}/{len(reachability)} for assertion {idx}: {reach_status} ({time.perf_counter() - started:.2f}s)', flush=True)
        if reach_status == z3.unsat:
            vacuous.append(idx)
            print(f'WARNING: assertion {idx} targets an unreachable operation (vacuous)', flush=True)

    solver.add(COBOL_PROGRAM, z3.Not(ASSERTION))
    print('[Z3 Runtime] 3/3 Starting final verification...', flush=True)
    started = time.perf_counter(); status = solver.check()
    print(f'[Z3 Runtime] 3/3 Final verification finished: {status} ({time.perf_counter() - started:.2f}s)', flush=True)
    if status == z3.unsat:
        print('VERIFIED: The program satisfies the assertion.')
        return {'status': 'verified', 'model': None, 'vacuous_assertion_indices': sorted(set(vacuous))}
    if status == z3.sat:
        print('COUNTEREXAMPLE: ASSERTION VIOLATION DETECTED:')
        model = solver.model(); print(model)
        failed, failed_checks = [], {}
        for idx, kind, expr in _CHECKS:
            if z3.is_false(model.eval(expr, model_completion=True)):
                print(f'FAILED_CHECK: assertion {idx} {kind}')
                failed_checks.setdefault(str(idx), []).append(kind)
                if idx not in failed: failed.append(idx)
        print('FAILED_ASSERTION_INDICES:', sorted(failed))
        return {
            'status': 'failed', 'model': str(model),
            'failed_assertion_indices': sorted(failed),
            'failed_checks': failed_checks,
            'contradictory_assertion_indices': [],
            'vacuous_assertion_indices': sorted(set(vacuous)),
        }
    print('UNKNOWN:', solver.reason_unknown())
    return {'status': 'unknown', 'model': None}


if __name__ == '__main__':
    run_smt_verification()