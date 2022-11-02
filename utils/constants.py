import scipy.constants as const

class PhysicalConstants(object):
    def __init__(self):
        self.c = const.c                                # speed of light
        self.h = const.h                                # planck constant
        self.mu_0 = const.mu_0                          # permeability in free space
        self.epsilon_0 = const.epsilon_0                # permittivity in free space
        self.e = const.e                                # electron charge
        self.eV = const.eV                              # electron volt in Joules

        self.m_e = const.physical_constants['electron mass energy equivalent in MeV'][0]
        self.electron_mass = const.physical_constants['electron mass energy equivalent in MeV'][0]
        self.m_p = const.physical_constants['proton mass energy equivalent in MeV'][0]
        self.proton_mass = const.physical_constants['proton mass energy equivalent in MeV'][0]
        self.m_n = const.physical_constants['neutron mass energy equivalent in MeV'][0]
        self.neutron_mass = const.physical_constants['neutron mass energy equivalent in MeV'][0]
        self.r_e = const.physical_constants['classical electron radius'][0]
        
        self.electron_charge = -1
        self.proton_charge = 1

        
class MathConstants(object):
    def __init__(self):
        self.pi = const.pi
        self.deg2rad = self.pi / 180
        self.rad2deg = 180 / self.pi