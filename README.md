# Global Transformation library

A library to define and compute synchronous rewriting systems as global transformations (GT)[1].
This projects implements the computation algorithm designed in [2].

A rewriting system can be defined over the following structures :
- Graphs defined in `data/Graph`
- Generalized maps defined in `data/Gmap`
- Sequences defined in `data/Sequence`
- Labelized structures with `data/Sheaf`
- Sets of alternatives with `data/Open`

To install the required modules :
```pip install -r requirements.txt```

The tests in `test` can be run with the following arguments :
- `--show`    : show each step of computation
- `--showall` : show also each intermediary step

Rewriting systems can be run and plotted for visual output in `test\plot`.
Python files in 'test\plot' outputs the following computations:
- graph_tmr: implementation of triangle mesh refinement (TMR) over graphs [1].
- gmap_tmr: 3D implementation of TMR over generalized maps.
- graph_sierpinsky: modification of the TMR over graphs to compute sierpinksy graphs.
- open_sierpinsky: application of monadic formalism presented in [3] to random subdivision.
- open_rivers: use of previous features for fractal river generation ([3], [4]).

All theses plots can be run step-by-step by running `jupyter` in `test\plot\jupyter`.
Details of configuration can be found `test\plot\README.md`.

References:
[1] Thesis chapter1
[2] Thesis chapter3
[3] Thesis chapter4
[4] A fractal model of rivers... 
