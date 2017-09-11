
All credits should go to Jonathan Salwan and Adrien Guinet. I am just using their amazing work.

The "pimp my triton" title is an idea of pancake (I think).

```
.
├── examples
│   ├── arybo : unobfuscated binary generation example
│   │   ├── deobf.py : script used for symbolic emulation / deobfuscation / binary generation
│   │   ├── obf.out  : the original "obfuscated" binary
│   │   └── run.c    : bootstrap to the deobfuscated blob
│   ├── constraints : constraint resolution examples
│   │   ├── build_cstr.py : building your own constraints
│   │   └── getpathconstraint.py : using getPathConstraint / getBranchConstraints APIs
│   ├── opaque_predicates: not shown, but usefull (from triton repo)
│   │   └── proving_opaque_predicates.py
│   ├── simple_emulation : a simple emulation script using triton
│   │   └── emulation.py
│   └── triton_simplification : simplification examples using triton (from triton repo)
│       └── simplification.py
├── pics:
│   ├── ast.png
│   └── triton_v03_architecture.png
├── pimp_my_triton.md
├── pimp_my_triton.pdf
└── sample: 
    └── baby-re
```

`r2pm -i pimp` should be updated soon (PR sent today). In the meantime check the original repo.
