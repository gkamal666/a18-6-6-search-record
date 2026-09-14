# Reproducibility

Run `python3 verify_diversity.py` from this directory (Python 3.10+). It checks all 292 files, every word's length, weight and pairwise distance, the supplied hashes, and the distinct pair-distance profiles. The finite result is 292 valid pairwise inequivalent 133-word codes of length 18, weight 6 and minimum distance 6. The 134-word target was not met; `data/prior_invalid134.txt` is deliberately rejected by `verify_code.py`.

The search logs and solver records describe time-limited explorations and are not exhaustive impossibility proofs. C001 is attributed to Christopher D. Rosin via Brouwer's maintained table; no worldwide novelty or external review is claimed.
