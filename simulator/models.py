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

class flowsheet:
    def __init__(self, name, streams, units):
        self.name = name
        self.streams = streams
        self.units = units


