# Pardon's Mathematics: Deep-Dive Map

This document is a source-grounded orientation map. It is not a proof and not a substitute for Pardon's papers.

## 1. The Fields Medal Citation

The International Mathematical Union cites John Pardon for achievements in symplectic geometry, including new approaches to virtual fundamental cycles, Fukaya categories of certain manifolds and counting holomorphic curves, plus contributions to geometry and topology including group actions on 3-manifolds and knot theory.

That citation identifies several connected research lines rather than one isolated theorem.

## 2. Virtual Fundamental Cycles

Pardon's 2016 Geometry & Topology paper develops an algebraic approach to virtual fundamental cycles on moduli spaces of pseudo-holomorphic curves. The motivation is foundational: moduli spaces used in curve-counting are often not cut out transversely. Naive counting can fail because the solution space is singular, has the wrong dimension, or has boundary/compactness problems.

The key educational idea for this repo:

```text
geometric equation -> solution/moduli space -> degeneracy -> virtual count machinery
```

The `moduli_space_toy.py` script illustrates only the first visual intuition: a solution space can change dimension or become singular as a parameter changes.

## 3. Contact Homology

In his JAMS paper on contact homology and virtual fundamental cycles, Pardon constructs coherent virtual fundamental cycles on compactified moduli spaces of pseudo-holomorphic curves. Contact homology comes from counting curves in the symplectization of a contact manifold.

Educational translation:

```text
contact dynamics -> Reeb orbits -> pseudo-holomorphic curves -> algebraic invariant
```

This repository does not implement contact homology. It only visualizes the background Cauchy-Riemann residual and phase-space geometry.

## 4. Fukaya Categories and Wrapped Fukaya Categories

With Sheel Ganatra and Vivek Shende, Pardon contributed to a modern local-to-global framework for wrapped Fukaya categories, including sectorial descent and microlocal Morse theory. These works connect symplectic/Floer-theoretic data with sheaf-theoretic descriptions and mirror-symmetry computations.

Educational translation:

```text
Lagrangians + intersections + holomorphic polygons -> category
```

The `lagrangian_intersections.py` script is only a first picture of the word "intersections". It is not a Fukaya category.

## 5. Universal Curve Counting and Calabi-Yau Threefolds

Pardon's 2023 work on universally counting curves in Calabi-Yau threefolds relates enumerative invariants and reductions to local curves in contexts connected with the MNOP conjecture.

Educational translation:

```text
many curve-counting theories -> universal invariant -> reduction to local pieces
```

This matters conceptually because it shows a recurring theme: organize hard global geometry by precise local-to-global algebraic structures.

## 6. Hilbert-Smith in Dimension Three

Pardon's 2013 JAMS paper proved the Hilbert-Smith conjecture for three-manifolds: every locally compact group acting faithfully on a connected 3-manifold is a Lie group. The proof rules out faithful actions of p-adic integers using low-dimensional topology.

Educational translation:

```text
topological group action -> manifold constraints -> rigidity result
```

## 7. Knot Distortion

Pardon's Annals paper on knot distortion answered a 1983 question of Gromov by proving nontrivial lower bounds for distortion of torus knots. The repo's `knot_distortion.py` computes a finite sampled distortion ratio for a trefoil-like polygon.

The real theorem is much deeper. The demo only explains what the ratio means.

## 8. Pattern Across The Work

A recurring pattern in Pardon's work is not just solving individual geometric problems, but building frameworks that make unstable geometric objects countable, comparable, or classifiable.

That is the conceptual bridge to this repository:

- preserve structure when simulating dynamics;
- distinguish real geometry from numerical artifact;
- document degeneracies instead of hiding them;
- use tests and visualizations to catch false intuition.
