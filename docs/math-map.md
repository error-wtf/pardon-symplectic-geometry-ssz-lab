# Mathematical Map

## Symplectic Geometry

A symplectic manifold is an even-dimensional space equipped with a closed, non-degenerate two-form. In the plane the standard form is:

```text
omega = dq wedge dp
```

Hamiltonian flows preserve this form. In two dimensions that implies area preservation.

## Holomorphic and Pseudo-Holomorphic Curves

For a complex map `u(s,t)=x(s,t)+i y(s,t)`, the Cauchy-Riemann equations are:

```text
x_s = y_t
x_t = -y_s
```

Pseudo-holomorphic curves generalize this idea to almost-complex and symplectic settings.

## Virtual Fundamental Cycles

Curve-counting often needs to count solutions living in singular or non-transverse moduli spaces. Virtual fundamental cycle machinery supplies a way to define counts where naive geometry breaks.

## Fukaya Categories

Fukaya categories organize Lagrangian submanifolds, intersection points, and holomorphic curve counts into categorical invariants. This repo only illustrates the first visual intuition: intersections.

## Knot Distortion

For a knot `K`, distortion compares intrinsic distance along the knot to direct Euclidean distance:

```text
distortion(K) = sup intrinsic_distance_K(x,y) / euclidean_distance(x,y)
```

Pardon's undergraduate work solved a major Gromov problem in this area. The code here only computes finite polygonal samples.
