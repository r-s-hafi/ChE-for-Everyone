class component:
    def __init__(self, name, mw, Tb, Tc, Pc, antoine, Cp_liq, Cp_vap, Hvap):
        self.name = name
        self.mw = mw
        self.Tb = Tb
        self.Tc = Tc
        self.Pc = Pc
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

class heat_exchanger:
    def __init__(self, name, feed, efficiency, Q=None, T_out=None):
        self.name = name
        self.feed = feed
        self.Q = Q
        self.T_out = T_out
        self.efficiency = efficiency

class pump:
    def __init__(self, name, feed, P_out, efficiency):
        self.name = name
        self.feed = feed
        self.P_out = P_out
        self.efficiency = efficiency

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



