# Finite inequivalence certificate

## Statement

The 292 files C001.txt through C292.txt provide 292 pairwise non-isometric binary codes. Each code has length 18, cardinality 133, constant weight 6, and minimum Hamming distance 6.

## Verification of the witnesses

For each file, the checker verifies the SHA-256 digest, 133 distinct rows, 18 binary characters per row, six ones per row, and all 8,778 unordered pairs. It checks pair distances by two implementations and separately verifies that no four-coordinate subset belongs to two codeword supports. The supplied certificate gives the resulting pair-distance histogram.

## Inequivalence proof

For a code C, let H_C(d) be the number of unordered pairs of distinct words in C at Hamming distance d. Any bijection preserving Hamming distance induces a bijection on unordered pairs and therefore preserves every H_C(d). All 292 histograms in CERTIFICATE.json are distinct. Thus no two of these codes are isometric. Coordinate permutations and row reorderings are particular cases covered by this argument.

## What this does not establish

This statement does not supply 134 words or improve the known-size benchmark. C001 is the supplied published Christopher D. Rosin code. The other 291 files are proved inequivalent to C001; this does not establish that those equivalence classes were previously unknown anywhere in the literature. No external specialist review or global classification is claimed.
