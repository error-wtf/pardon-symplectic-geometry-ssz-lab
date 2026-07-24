# Observable Routing Matrix

This file is generated from `pardon_math.method_assignment.ROUTES`.
It documents the fail-closed SSZ method assignment used by the Pardon/SSZ bridge.

| Observable | Method | Domain | Guardrail | Claim boundary |
|---|---|---|---|---|
| `clock` | Xi/D direct | timelike local clock comparison | do not reuse this route for null-ray lensing or Shapiro delay | toy bridge to SSZ clock formulas, not a proof of the physical model |
| `frame_dragging` | PPN beta/gamma | rotating-source orbital observable | requires spin/metric data beyond scalar Xi | methodological bridge only |
| `frequency_shift` | Xi/D direct | timelike frequency comparison | closed static products telescope unless dynamics/non-sphericity is present | methodological bridge only |
| `geodesic` | Lagrange/Hamilton geodesic equations | phase-space trajectory | validate invariants before interpreting coordinate plots | toy validation pattern only |
| `gps` | Xi/D direct plus operational frame corrections | timelike clock network | do not collapse real GPS modelling to a single scalar | routing sanity check only |
| `holonomy_dynamic` | dynamic loop diagnostic | time-dependent or non-spherical loop | only deviations with stated dynamics are physically interesting | illustrative diagnostic only |
| `holonomy_static` | static telescoping identity | closed static frequency product | closed product should return 1 in the static toy model | sanity check, not a physical anomaly |
| `lensing` | PPN (1+gamma) | null ray observable | Xi-only is temporal contribution only; spatial curvature completion is required | methodological bridge only |
| `null` | PPN (1+gamma) | generic null observable | must not be evaluated with a timelike-only shortcut | methodological bridge only |
| `orbit` | PPN beta/gamma or Hamiltonian orbit machinery | timelike trajectory | check energy/angular-momentum drift and regime domain | toy validation pattern only |
| `pound_rebka` | Xi/D direct | laboratory gravitational redshift | keep height/weak-field approximation explicit | routing sanity check only |
| `precession` | PPN beta/gamma | timelike orbital correction | do not infer from a static redshift formula alone | methodological bridge only |
| `redshift` | Xi/D direct | timelike frequency ratio | source/observer convention must be stated | derived identity inside the simplified bridge module |
| `shapiro` | PPN (1+gamma) | null delay observable | Xi-only route is incomplete for full delay; spatial curvature contribution is required | methodological bridge only |
| `time_dilation` | Xi/D direct | timelike proper-time comparison | no photon proper-time interpretation | derived identity inside the simplified bridge module |
| `vlbi` | PPN (1+gamma) | null timing/angle observable | requires spatial contribution and measurement geometry | methodological bridge only |
