#!/usr/bin/env python3
"""Exact, dependency-free verification for binary constant-weight A(18,6,6) codes.

The checks certify a supplied finite construction, not global optimality or novelty.
Run: python verify_code.py path/to/code.txt
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
from collections import Counter
from typing import Sequence

def _popcount(value: int) -> int:
    """Compatibility helper for Python versions before int.bit_count()."""
    return value.bit_count() if hasattr(value, 'bit_count') else bin(value).count('1')


def verify(rows: Sequence[str]) -> dict:
    errors: list[str] = []
    if not rows:
        errors.append('The input contains no words.')
    for i, row in enumerate(rows, 1):
        if len(row) != 18:
            errors.append(f'Row {i}: length {len(row)} instead of 18.')
        if set(row) - {'0', '1'}:
            errors.append(f'Row {i}: contains a non-binary character.')
        if row.count('1') != 6:
            errors.append(f'Row {i}: weight {row.count("1")} instead of 6.')
    if len(set(rows)) != len(rows):
        errors.append('Duplicate words are present.')
    result = {
        'word_count': len(rows), 'required_length': 18, 'required_weight': 6,
        'required_minimum_distance': 6, 'target_minimum_word_count': 134,
        'format_errors': errors,
        'valid_code': False, 'meets_134_target': False,
        'scope': 'Finite exact checks only; no assertion of novelty or external review.',
    }
    if any(len(row) != 18 or set(row) - {'0', '1'} for row in rows):
        return result

    # Checker 1: whole-word integer exclusive OR and population counts.
    integers = [int(row, 2) for row in rows]
    xor_hist = Counter()
    xor_bad = []
    for i, j in itertools.combinations(range(len(rows)), 2):
        d = _popcount(integers[i] ^ integers[j])
        xor_hist[d] += 1
        if d < 6:
            xor_bad.append([i + 1, j + 1, d])

    # Checker 2: literal per-coordinate character comparisons, without bit operations.
    character_hist = Counter()
    character_bad = []
    for i in range(len(rows)):
        for j in range(i):
            d = sum(rows[i][k] != rows[j][k] for k in range(18))
            character_hist[d] += 1
            if d < 6:
                character_bad.append([j + 1, i + 1, d])

    # Checker 3: no 4-coordinate subset may appear in two weight-6 supports.
    owner = {}
    repeated_four_subsets = 0
    for i, row in enumerate(rows):
        support = [k for k, c in enumerate(row) if c == '1']
        for q in itertools.combinations(support, 4):
            if q in owner:
                repeated_four_subsets += 1
            else:
                owner[q] = i
    xor_ok = not errors and not xor_bad
    character_ok = not errors and not character_bad
    packing_ok = not errors and not repeated_four_subsets
    agreement = (xor_hist == character_hist and xor_ok == character_ok == packing_ok)
    result.update({
        'pair_count': len(rows) * (len(rows) - 1) // 2,
        'xor_check': {'passes': xor_ok, 'minimum_distance': min(xor_hist, default=None),
                      'distance_histogram': dict(sorted(xor_hist.items())),
                      'violating_pairs_1_based': xor_bad},
        'character_check': {'passes': character_ok,
                            'minimum_distance': min(character_hist, default=None),
                            'distance_histogram': dict(sorted(character_hist.items())),
                            'violating_pairs_1_based': sorted(character_bad)},
        'four_subset_check': {'passes': packing_ok,
                              'repeated_four_subsets': repeated_four_subsets},
        'checkers_agree': agreement,
        'valid_code': bool(xor_ok and character_ok and packing_ok and agreement),
        'meets_134_target': bool(len(rows) >= 134 and xor_ok and character_ok and packing_ok and agreement),
    })
    return result


def verify_file(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    rows = text.splitlines()
    result = verify(rows)
    result['input_file'] = str(path)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    args = parser.parse_args()
    try:
        result = verify_file(args.file)
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f'Cannot read the input: {exc}\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['valid_code'] else 1)
