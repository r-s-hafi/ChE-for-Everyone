#UNITS
#FOR NOW
#Pressure: bar
#Temperature: degC
#Flow = kg/hr
#Density = kg/m^3
#Cp = kJ/kmol/K
#z = mass fraction




thermo_model = "PR"



class component:

    def __init__(self, name, mw, Tb, Tc, Pc, omega, antoine, Cp_liq, Cp_vap, density_liq, density_vap, Hvap):

        self.name = name
        self.mw = mw
        self.Tb = Tb
        self.Tc = Tc
        self.Pc = Pc
        self.omega = omega
        self.antoine = antoine
        self.Cp_liq = Cp_liq
        self.Cp_vap = Cp_vap
        self.density_liq = density_liq
        self.density_vap = density_vap
        self.Hvap = Hvap
        

class stream:
    def __init__(self, name, flow, z, T, P):

        self.name = name
        self.flow = flow
        self.z = z
        self.T = T
        self.P = P

        self.validate()
        self.calculate_properties()

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

    def calculate_properties(self):

        from components import component_db
        from thermo import Mixture
        components = list(self.z.keys())
        fracs = list(self.z.values())

        #create mixtute with stream components and fractions, convert bar to Pa
        mix = Mixture(components, fracs, T=self.T, P=self.P * 1e5)
        self.phase = mix.phase
        self.v_frac = mix.V_over_F
        self.density_liq = mix.rhol #kg/m3
        self.density_vap = mix.rhog #kg/m3
        self.Mw = mix.MW #kg/kmol
        self.x = mix.xs #liquid mole fractions
        self.y = mix.ys #vapor mole fractions

        moles = {component: self.z[component] / component_db[component].mw for component in self.z}
        total_moles = sum(moles.values())
        x_moles = {component: moles[component] / total_moles for component in moles}

        if self.phase == "l":
            Cp_molar = sum(x_moles[component] * component_db[component].Cp_liq for component in x_moles)
        elif self.phase == "g":
            Cp_molar = sum(x_moles[component] * component_db[component].Cp_vap for component in x_moles)
        
        molar_flow = self.flow / self.Mw

        self.Cp_molar = Cp_molar
        self.molar_flow = molar_flow

    def summary(self):

        print(f"Stream: {self.name}")
        print(f"  Temperature:  {self.T:.1f} K  ({self.T - 273.15:.1f} °C)")
        print(f"  Pressure:     {self.P:.3f} bar")
        print(f"  Flow:         {self.flow:.2f} kg/hr")
        print()
        print(f"  {'Component':<20} {'Mass Frac':>10}    {'Flow (kg/hr)':>15}")
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

        if self.T_out is not None and self.Q is not None:
            raise ValueError("Cannot specify both T_out and Q for a heat exchanger")
        if self.T_out is None and self.Q is None:
            raise ValueError("Must specify either T_out or Q for a heat exchanger")

        if self.T_out is not None:
            self.Q = self.feed.molar_flow * self.feed.Cp_molar * (self.T_out - self.feed.T)
        elif self.Q is not None:
            self.T_out = self.feed.T + (self.Q / (self.feed.molar_flow * self.feed.Cp_molar))
        
        #phase assumptions here are not necessarily correct, but it is a good place to start
        self.outlet_stream = stream(name=f'{self.name}_out', flow=self.feed.flow, z=self.feed.z, T=self.T_out, P=self.feed.P)

    def summary(self):

        print(f"Heat Exchanger: {self.name}")
        print(f"  Feed: {self.feed.name}")
        print(f"  Outlet Stream: {self.outlet_stream.name}")
        print(f"  Efficiency: {self.efficiency:.2f}")
        print(f"  Q: {self.Q:.2f} kJ/hr")
        print(f"  T_out: {self.T_out:.1f} K  ({self.T_out - 273.15:.1f} °C)")
        print()

class pump:

    def __init__(self, name, feed, P_out=None, efficiency=None, power=None):
        self.name = name
        self.feed = feed
        self.P_out = P_out
        self.efficiency = efficiency
        self.power = power

    def validate(self):
        if self.P_out is None and self.power is None:
            raise ValueError("Must specify either P_out or power for a pump")
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
        
        self.outlet_stream = stream(
            name=f'{self.name}_out',
            flow=self.feed.flow,
            z=self.feed.z,
            T=self.feed.T,
            P=self.P_out,
        )

    def summary(self):

        print(f"Pump: {self.name}")
        print(f"  Feed: {self.feed.name}")
        print(f"  Outlet Stream: {self.outlet_stream.name}")
        print(f"  Efficiency: {self.efficiency:.2f}")
        print(f"  Power: {self.power/1000:.2f} kW")
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
        P=1.5
    )

    hex1 = heat_exchanger(
        name="hex1",
        feed=feed,
        T_out=350,
        efficiency=0.9
    )

    hex1.calculate()
    hex1.summary()

