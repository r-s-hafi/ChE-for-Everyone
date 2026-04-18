from abc import ABC, abstractmethod
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
