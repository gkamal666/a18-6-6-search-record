# Verified family: 292 inequivalent 133-word codes

This is a finite construction-family certificate, **not a 134-word solution or a new size record**. Every supplied code has 133 distinct 18-bit words, each of weight 6, with minimum pairwise Hamming distance 6.

C001 is the supplied published Christopher D. Rosin code. The other 291 representatives are proved inequivalent to C001 and to each other by distinct pair-distance profiles. Global literature novelty and external specialist validation have not been established.

## Verify

Run from this directory with Python 3.10 or later:

```sh
python verify_diversity.py
```

The checker uses only the standard library. It verifies the file hashes and every construction using integer, literal-character, and four-subset checks. It then verifies that all 292 pair-distance histograms are different.

The proof is in `incumbent_diversity/PROOF.md`; the individual witnesses and their distance profiles are in `incumbent_diversity/CERTIFICATE.json` and C001.txt through C292.txt.

The broader search target remains at least 134 words. No such construction was found in the completed continuation. Source attribution and the full search logs are retained in the separate research-continuation package.

Published baseline source:

```text
https://aeb.win.tue.nl/codes/Andw.html
https://aeb.win.tue.nl/codes/cwc/d6/a18.6.6.133
```
