"""Test scaffolding for the lost-result probe (g61-lost-tool-result): when CARDCARE_CRASH_AFTER names a function of
cardcare.world, the process exits as if killed right after that function returns, that is after its database effect
and before the framework records the tool's result. Python imports this module only when run_scenario puts this
directory first on PYTHONPATH for a `crash_session` step; it is never on the product's path.
"""

import os
import sys

name = os.environ.get("CARDCARE_CRASH_AFTER")
if name:
    try:
        import cardcare.world as world
        original = getattr(world, name)
    except (ImportError, AttributeError) as exc:  # older code without the function: the step runs without a crash
        print(f"[crash hook] nothing to patch: {exc}", file=sys.stderr)
    else:
        def crash_after(*args, **kwargs):
            result = original(*args, **kwargs)
            sys.stderr.write(f"[crash hook] {name} done; exiting before its result is recorded\n")
            sys.stderr.flush()
            os._exit(137)
        setattr(world, name, crash_after)
