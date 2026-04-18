Task D — UnitOp Base Class Refactor
Instructions for Claude Code
Context
This is a chemical engineering process simulator. stream, pump, and heat_exchanger are working with passing tests. compressor, flash_drum, distillation_column, and flowsheet are stubs.
The goal is to introduce a UnitOp abstract base class that pump, heat_exchanger, and the three stubs all inherit from. This removes duplicated boilerplate and enforces a consistent interface across unit ops.
Current repo layout
simulator/
  models.py          # component, stream, and all unit op classes
  components.py      # component_db dict (do not touch)
  nist_scraper.py    # db build script (do not touch)
  test_unit_ops.py   # 4 passing tests (do not touch except as noted)
Target repo layout
simulator/
  models.py          # component, stream only
  base.py            # NEW — UnitOp ABC
  unit_ops.py        # NEW — pump, heat_exchanger, compressor, flash_drum, distillation_column
  components.py      # unchanged
  nist_scraper.py    # unchanged
  test_unit_ops.py   # update imports only
Success criteria
pytest -v must pass all 4 existing tests with zero modifications to test logic. The only allowed test-file change is updating imports (from models import ... may become from unit_ops import ... for the unit op classes). If any test fails, the refactor is wrong.
Do not add new tests. Do not rename any class (keep lowercase pump, heat_exchanger, etc. for now — that's a separate refactor).

1. Create base.py
pythonfrom abc import ABC, abstractmethod
from models import stream


class UnitOp(ABC):
    """Abstract base class for all unit operations."""

    def __init__(self, name, feed):
        self.name = name
        self.feed = feed
        self.outlet_stream = None

    @abstractmethod
    def validate(self):
        """Check input specs. Raise ValueError on invalid inputs."""
        pass

    @abstractmethod
    def calculate(self):
        """Solve the unit op. Must call self.validate() first and populate self.outlet_stream."""
        pass

    def _make_outlet(self, T, P, z=None, flow=None, name_suffix="_out"):
        """Construct the outlet stream with the feed's z and flow as defaults."""
        return stream(
            name=f"{self.name}{name_suffix}",
            flow=flow if flow is not None else self.feed.flow,
            z=z if z is not None else self.feed.z,
            T=T,
            P=P,
        )

    def summary(self):
        """Generic summary. Subclasses should call super().summary() and append specifics."""
        print(f"{type(self).__name__}: {self.name}")
        print(f"  Feed:         {self.feed.name}")
        if self.outlet_stream is not None:
            print(f"  Outlet:       {self.outlet_stream.name}")
2. Create unit_ops.py
Move pump, heat_exchanger, compressor, flash_drum, distillation_column out of models.py and into unit_ops.py. All five must inherit from UnitOp.
2a. pump

Inherit from UnitOp
__init__ signature: (self, name, feed, P_out=None, efficiency=None, power=None) — call super().__init__(name, feed) first
Port validate() and calculate() logic from current models.py unchanged EXCEPT:

Replace manual stream(...) construction in calculate() with self.outlet_stream = self._make_outlet(T=self.feed.T, P=self.P_out)
Replace the first two validate() checks with: if (self.P_out is None) == (self.power is None): raise ValueError("Must specify exactly one of P_out or power")


Rewrite summary() to call super().summary() then print pump-specific lines (efficiency, power in W and kW, P_out)

2b. heat_exchanger

Inherit from UnitOp
__init__ signature: (self, name, feed, efficiency=None, Q=None, T_out=None) — call super().__init__(name, feed) first
Add a validate() method (currently missing). It must check:

(self.T_out is None) == (self.Q is None) → raise ValueError "Must specify exactly one of T_out or Q"
self.feed.phase not in ("l", "g") → raise ValueError "Heat exchanger requires single-phase feed, got '{phase}'"


calculate() must call self.validate() as its first line
Replace manual stream(...) construction with self.outlet_stream = self._make_outlet(T=self.T_out, P=self.feed.P)
Keep the Cp_molar + molar_flow math exactly as it is in current models.py — do NOT change it
Rewrite summary() to call super().summary() then print HX-specific lines
Leave efficiency accepted but unused in the math — it is TODO territory

2c. compressor, flash_drum, distillation_column

All three must inherit from UnitOp
Call super().__init__(name, feed) in their __init__ methods (they all have a feed as their first non-name arg currently)
Keep all their existing __init__ parameters exactly as they are
Add validate() and calculate() methods that raise NotImplementedError("<unit op name> not yet implemented")
These are stubs. The point of making them inherit is interface consistency. Do not attempt to implement them.

3. Update models.py

Remove pump, heat_exchanger, compressor, flash_drum, distillation_column classes entirely
Keep component, stream, and flowsheet classes
Keep the header comments and thermo_model = "PR" line
Delete the if __name__ == "__main__": block at the bottom — it references phase="l" which is no longer a valid stream kwarg, and it belongs in a scratch file anyway

4. Update test_unit_ops.py
Only change: the import line. Currently:
pythonfrom models import stream, heat_exchanger, pump
Becomes:
pythonfrom models import stream
from unit_ops import heat_exchanger, pump
No other changes to the test file.
5. Verify
Run pytest -v from the simulator/ directory. All 4 tests must pass. Do not commit unless they do.

Constraints / things NOT to do

Do not rename any class or method
Do not change any physics or math
Do not add new tests
Do not modify components.py, nist_scraper.py, or component_db
Do not change the stream class signature or internals
Do not add type hints (keeping consistent with existing style)
Do not add docstrings beyond what I've specified in base.py
Do not "clean up" things that aren't in this spec — no scope creep. If you notice something that looks wrong or stylistically off, leave it alone. The point of this refactor is the base class, nothing else.
Do not add a from __future__ import annotations or any new imports beyond what's needed
If anything in this spec is ambiguous, stop and ask rather than guessing