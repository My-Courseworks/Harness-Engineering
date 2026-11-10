"""Test scaffolding for the mutant runs: when CARDCARE_MUTANT names a mutant (probes/mutants/mutants.py), it is applied
as this process starts. Python imports this module only when run_scenario --mutant puts this directory first on
PYTHONPATH for its child processes (the shipped CLI and tick); it is never on the product's path.
"""

import os
import sys

name = os.environ.get("CARDCARE_MUTANT")
if name:
    try:
        from mutants import MUTANTS
        MUTANTS[name]()
        sys.stderr.write(f"[mutant] {name} applied\n")
    except Exception as exc:
        sys.stderr.write(f"[mutant] {name} could not be applied: {type(exc).__name__}: {exc}\n")
