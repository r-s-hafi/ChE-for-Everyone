class component:
    def __init__(self, name, mw, Tb, Tc, Pc, omega, antoine, Cp_liq, Cp_vap, Hvap):
        self.name = name
        self.mw = mw
        self.Tb = Tb
        self.Tc = Tc
        self.Pc = Pc
        self.omega = omega
        self.antoine = antoine
        self.Cp_liq = Cp_liq
        self.Cp_vap = Cp_vap
        self.Hvap = Hvap

class stream:
    def __init__(self, name, flow, z, T, P, phase=None, v_frac=None):
        self.name = name
        self.flow = flow
        self.z = z
        self.T = T
        self.P = P
        self.phase = phase
        self.v_frac = v_frac
    def validate(self):
        if abs(sum(self.z.values()) - 1) > 1e-6:
            raise ValueError(f"Component {self.name} has a sum of z values that is not 1")
        if any(z < 0 for z in self.z.values()):
            raise ValueError(f"Component {self.name} has a negative z value")
        if self.T is not None and self.T < 0:
            raise ValueError(f"Stream temperature cannot be negative")
        if self.P is not None and self.P < 0:
            raise ValueError(f"Stream pressure cannot be negative")
        if self.flow is not None and self.flow < 0:
            raise ValueError(f"Stream flow cannot be negative")
    def summary(self):
        print(f"Stream: {self.name}")
        print(f"  Temperature:  {self.T:.1f} K  ({self.T - 273.15:.1f} °C)")
        print(f"  Pressure:     {self.P:.3f} bar")
        print(f"  Flow:         {self.flow:.2f} kmol/hr")
        print()
        print(f"  {'Component':<20} {'Mol Frac':>10}    {'Flow (kmol/hr)':>15}")
        print(f"  {'-'*20} {'-'*10}    {'-'*15}")
        for comp, frac in self.z.items():
            comp_flow = self.flow * frac
            print(f"  {comp:<20} {frac:>10.4f}    {comp_flow:>15.3f}")

class heat_exchanger:
    def __init__(self, name, feed, efficiency, Q=None, T_out=None):
        self.name = name
        self.feed = feed
        self.efficiency = efficiency
        self.Q = Q
        self.T_out = T_out
        self.outlet_stream = None
    def calculate(self):
        from components import component_db
        if self.T_out is not None and self.Q is not None:
            raise ValueError("Cannot specify both T_out and Q for a heat exchanger")
        if self.T_out is None and self.Q is None:
            raise ValueError("Must specify either T_out or Q for a heat exchanger")
        if self.feed.phase == "liquid":
            Cp_mix = sum(self.feed.z[comp] * component_db[comp].Cp_liq for comp in self.feed.z)
        if self.feed.phase == "vapor":
            Cp_mix = sum(self.feed.z[comp] * component_db[comp].Cp_vap for comp in self.feed.z)
        if self.T_out is not None:
            self.Q = self.feed.flow * Cp_mix * (self.T_out - self.feed.T)
        elif self.Q is not None:
            self.T_out = self.feed.T + (self.Q / (self.feed.flow * Cp_mix))
        
        #phase assumptions here are not necessarily correct, but it is a good place to start
        self.outlet_stream = stream(name=f'{self.name}_out', flow=self.feed.flow, z=self.feed.z, T=self.T_out, P=self.feed.P, phase=self.feed.phase, v_frac=self.feed.v_frac)
    def summary(self):
        print(f"Heat Exchanger: {self.name}")
        print(f"  Feed: {self.feed.name}")
        print(f"  Outlet Stream: {self.outlet_stream.name}")
        print(f"  Efficiency: {self.efficiency:.2f}")
        print(f"  Q: {self.Q:.2f} kJ/hr")
        print(f"  T_out: {self.T_out:.1f} K  ({self.T_out - 273.15:.1f} °C)")
        print()

class pump:
    def __init__(self, name, feed, P_out, efficiency):
        self.name = name
        self.feed = feed
        self.P_out = P_out
        self.efficiency = efficiency
        self.outlet_stream = None
    def validate(self):
        if self.P_out is not None and self.feed.P is not None and self.P_out < self.feed.P:
            raise ValueError("Outlet pressure cannot be less than inlet pressure")
    def calculate(self):
        #phase assumptions here are not necessarily correct, but it is a good place to start
        #calculate power? keep simple for now
        self.outlet_stream = stream(name=f'{self.name}_out', flow=self.feed.flow, z=self.feed.z, T=self.feed.T, P=self.P_out, phase=self.feed.phase, v_frac=self.feed.v_frac)
    def summary(self):
        print(f"Pump: {self.name}")
        print(f"  Feed: {self.feed.name}")
        print(f"  Outlet Stream: {self.outlet_stream.name}")
        print(f"  Efficiency: {self.efficiency:.2f}")
        print(f"  P_out: {self.P_out:.3f} bar")
        print()

class compressor:
    def __init__(self, name, feed, P_out, efficiency):
        self.name = name
        self.feed = feed
        self.P_out = P_out
        self.efficiency = efficiency

class flash_drum:
    def __init__(self, name, feed, P, T):
        self.name = name
        self.feed = feed
        self.P = P
        self.T = T

class distillation_column:
    def __init__(self, name, feed, light_key, heavy_key, recovery_lk, recovery_hk, P):
        self.name = name
        self.feed = feed
        self.light_key = light_key
        self.heavy_key = heavy_key
        self.recovery_lk = recovery_lk
        self.recovery_hk = recovery_hk
        self.P = P

class flowsheet:
    def __init__(self, name, streams, units):
        self.name = name
        self.streams = streams
        self.units = units


if __name__ == "__main__":
    feed = stream(
        name="feed",
        flow=100,
        z={"benzene": 0.6, "toluene": 0.4},
        T=300,
        P=1.5,
        phase="liquid"
    )

    hex1 = heat_exchanger(
        name="hex1",
        feed=feed,
        T_out=350,
        efficiency=0.9
    )

    hex1.calculate()
    hex1.summary()

