# Claim Boundaries

This repository is deliberately conservative about what each artifact can show.

## Boundary Table

| Layer | What the repo can show | What it cannot show |
|---|---|---|
| Pardon mathematics | Background intuition for symplectic geometry, holomorphic residuals, moduli-space degeneracy, Lagrangian intersections and knot distortion | John Pardon's proofs, virtual fundamental cycle machinery, Fukaya-category constructions or theorem-level curve counts |
| Python toy models | Reproducible numerical behavior on small controlled examples | Physical truth of a full spacetime theory or theorem-level mathematical results |
| SSZ bridge | A validation style: observable routing, formula-domain guardrails, invariant checks and explicit limitations | Endorsement by John Pardon or proof that SSZ follows from Pardon's work |
| Visualizations | Intuition, diagnostics and reproducible outputs from local scripts | Evidence by themselves; every image depends on code and assumptions |
| Tests | Consistency checks for the included toy models and routing rules | External validation of the underlying physics or mathematical research program |
| Local repo scan | A map of public/non-private local physics repositories and useful expansion axes | A full audit of unpublished/private material |

## Practical Rule

Every strong claim in this repository should be traceable to one of four categories:

1. `source-grounded`: stated in a cited source or local documentation file.
2. `code-grounded`: directly produced by a deterministic script in this repository.
3. `test-grounded`: checked by the local unittest suite.
4. `interpretive`: an explicit methodological analogy or research direction, not a proof.

When a claim mixes categories, the weakest category controls the wording.
