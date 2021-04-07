# Global Transformation library

A library to define and compute synchronous rewriting systems.

A rewriting system can be defined over the following structures :
- Graphs defined in `data/Graph`
- Generalized maps defined in `data/Gmap`
- Sequences defined in `data/Sequence`
- Labelized structures with `data/Sheaf`
- Sets of alternatives with `data/Open`

To install the required modules :
```pip install -r requirements.txt```

The tests in `test` can be run with the following arguments
- `--show`    : show each step of computation
- `--showall` : show also each intermediary step

For the plots in `test\plot` see details in `test\plot\README.md`
