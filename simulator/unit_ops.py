from base import UnitOp


class pump(UnitOp):

    def __init__(self, name, feed, P_out=None, efficiency=None, power=None):
        super().__init__(name, feed)
        self.P_out = P_out
        self.efficiency = efficiency
        self.power = power

    def validate(self):
        if (self.P_out is None) == (self.power is None):
            raise ValueError("Must specify exactly one of P_out or power")
        if self.feed.phase == "g":
            raise ValueError("Pump cannot be used for vapor phase")
        if self.feed.phase != "l":
            raise ValueError("Pump can only be used for liquid phase")
        if self.P_out is not None and self.P_out < self.feed.P:
            raise ValueError("Outlet pressure cannot be less than inlet pressure")
        if self.power is not None and self.power < 0:
            raise ValueError("Power cannot be negative")
        if self.efficiency is not None and (self.efficiency < 0 or self.efficiency > 1):
            raise ValueError("Efficiency must be between 0 and 1")

    def calculate(self):
        self.validate()
        #assume 80% efficiency if user does not specify efficiency
        if self.efficiency is None:
            self.efficiency = 0.8

        mass_flow = self.feed.flow / 3600 #kg/s
        density = self.feed.density_liq #kg/m3

        if self.P_out is not None: #p_out is specified
            dP = (self.P_out - self.feed.P) * 1e5 #Pa
            W_ideal = mass_flow * dP / density #W
            self.power = W_ideal / self.efficiency #W
        else: #power is specified
            W_ideal = self.power * self.efficiency #W
            dP = W_ideal * density / mass_flow #Pa
            self.P_out = self.feed.P + (dP / 1e5) #bar

        self.outlet_stream = self._make_outlet(T=self.feed.T, P=self.P_out)

    def summary(self):
        super().summary()
        print(f"  Efficiency: {self.efficiency:.2f}")
        print(f"  Power: {self.power:.2f} W  ({self.power/1000:.2f} kW)")
        print(f"  P_out: {self.P_out:.3f} bar")
        print()


class heat_exchanger(UnitOp):

    def __init__(self, name, feed, efficiency=None, Q=None, T_out=None):
        super().__init__(name, feed)
        self.efficiency = efficiency
        self.Q = Q
        self.T_out = T_out

    def validate(self):
        if (self.T_out is None) == (self.Q is None):
            raise ValueError("Must specify exactly one of T_out or Q")
        if self.feed.phase not in ("l", "g"):
            raise ValueError(f"Heat exchanger requires single-phase feed, got '{self.feed.phase}'")

    def calculate(self):
        self.validate()

        if self.T_out is not None:
            self.Q = self.feed.molar_flow * self.feed.Cp_molar * (self.T_out - self.feed.T)
        elif self.Q is not None:
            self.T_out = self.feed.T + (self.Q / (self.feed.molar_flow * self.feed.Cp_molar))

        #phase assumptions here are not necessarily correct, but it is a good place to start
        self.outlet_stream = self._make_outlet(T=self.T_out, P=self.feed.P)

    def summary(self):
        super().summary()
        print(f"  Efficiency: {self.efficiency:.2f}")
        print(f"  Q: {self.Q:.2f} kJ/hr")
        print(f"  T_out: {self.T_out:.1f} K  ({self.T_out - 273.15:.1f} °C)")
        print()


class compressor(UnitOp):

    def __init__(self, name, feed, P_out, efficiency):
        super().__init__(name, feed)
        self.P_out = P_out
        self.efficiency = efficiency

    def validate(self):
        raise NotImplementedError("compressor not yet implemented")

    def calculate(self):
        raise NotImplementedError("compressor not yet implemented")


class flash_drum(UnitOp):

    def __init__(self, name, feed, P, T):
        super().__init__(name, feed)
        self.P = P
        self.T = T

    def validate(self):
        raise NotImplementedError("flash_drum not yet implemented")

    def calculate(self):
        raise NotImplementedError("flash_drum not yet implemented")


class distillation_column(UnitOp):

    def __init__(self, name, feed, light_key, heavy_key, recovery_lk, recovery_hk, P):
        super().__init__(name, feed)
        self.light_key = light_key
        self.heavy_key = heavy_key
        self.recovery_lk = recovery_lk
        self.recovery_hk = recovery_hk
        self.P = P

    def validate(self):
        raise NotImplementedError("distillation_column not yet implemented")

    def calculate(self):
        raise NotImplementedError("distillation_column not yet implemented")
