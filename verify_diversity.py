#!/usr/bin/env python3
"""Verify the finite code family and its distance-profile inequivalence certificate.
Uses only Python's standard library. Does not certify novelty or the 134-word target.
"""
from pathlib import Path
import hashlib
import json
import sys
from verify_code import verify_file

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def main() -> None:
    root = Path(__file__).resolve().parent
    directory = (root / 'incumbent_diversity').resolve()
    certificate = json.loads((directory / 'CERTIFICATE.json').read_text(encoding='utf-8'))
    seen = set()
    for entry in certificate['entries']:
        path = (directory / entry['file']).resolve()
        require(path.parent == directory, 'Certificate contains an out-of-directory path.')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], f'Hash mismatch: {path.name}')
        audit = verify_file(path)
        require(audit['valid_code'] and audit.get('checkers_agree', False) and audit['word_count'] == 133,
                f'Invalid construction: {path.name}')
        histogram = {str(k): v for k, v in audit['xor_check']['distance_histogram'].items()}
        require(histogram == entry['distance_histogram'], f'Distance-profile mismatch: {path.name}')
        key = tuple(sorted(histogram.items()))
        require(key not in seen, f'Repeated distance profile: {path.name}')
        seen.add(key)
    require(len(seen) == certificate['number_of_pairwise_inequivalent_codes'], 'Code-family count mismatch.')
    print(f'PASS: {len(seen)} exactly valid, pairwise distance-profile-distinguished 133-word codes.')
    print('This certificate does not establish a 134-word construction, a new size record, or global literature novelty.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
