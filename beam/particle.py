import sys
import numpy as np
from utils import physical_constants as pconstants
from utils.logs import *

class Particle():
    def __init__(self, species, energy, charge=1):
        self.species = species
        self.energy = energy

        if self.species.lower() == 'electron':
            self.charge = -1
            self.mass = pconstants.m_e
        elif self.species.lower() == 'proton':
            self.charge = 1
            self.mass = pconstants.m_p
        else:
            print_error('Unknown species {}'.format(self.species))

        self.s = 0
        #self.gamma = 0
        #self.beta = 0
        #self.momentum = 0
        
        self.update_energy(energy)

    def get_charge(self):
        return self.charge
    
    def get_rest_mass(self):
        return self.mass
        
    def update_gamma(self):
        self.gamma = 1 + self.energy / self.mass
    
    def get_gamma(self):
        return self.gamma
        
    def update_beta(self):
        gamma = self.get_gamma()
        self.beta = np.sqrt(gamma * gamma - 1) / gamma     
    
    def get_beta(self):
        return self.beta
        
    def update_momentum(self):
        self.momentum = np.sqrt(self.energy * self.energy - self.mass * self.mass)
        
    def get_momentum(self):
        return self.momentum
    
    def update_energy(self, energy):
        self.energy = energy
        self.update_gamma()
        self.update_beta()
        self.update_momentum()
        
    def get_energy(self):
        return self.energy
        
    def reset_s(self):
        self.s = 0
    
    def update_s(self, length):
        self.s += length
        
    def get_s(self):
        return self.s
    
    def print_particle_properties(self):
        print ("particle species  :", self.species)
        print ("particle charge   :", self.charge)
        print ("particle mass     :", self.mass, "MeV/c^2")
        print ("particle energy   :", self.energy, "MeV")
        print ("particle momentum :", self.momentum, "MeV/c") 
        print ("particle gamma    :", self.gamma)
        print ("particle beta     :", self.beta)
