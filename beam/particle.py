import sys
import numpy as np
from utils import physical_constants as pconstants

class Particle():
    def __init__(self, species, energy):
        self.species = species
        self.energy = energy

        if self.species.lower() == 'electron':
            self.charge = -1
            self.mass = pconstants.m_e
        elif self.species.lower() == 'proton':
            self.charge = 1
            self.mass = pconstants.m_p
        else:
            print('Unknown species {}'.format(self.species), file=sys.stderr)

        self.gamma = self.get_gamma()
        self.beta = self.get_beta()
        self.momentum = self.get_momentum()

    def get_gamma(self):
        gamma = 1 + self.energy / self.mass
        return gamma
        
    def get_beta(self):
        gamma = self.get_gamma()
        beta = np.sqrt(gamma * gamma - 1) / gamma     
        return beta
    
    def get_energy(self):
        return self.energy
        
    def get_momentum(self):
        momentum = np.sqrt(self.energy * self.energy - self.mass * self.mass)
        return momentum
    
    def update_energy(self, energy):
        self.energy = energy
        self.gamma = self.get_gamma()
        self.beta = self.get_beta()
        self.momentum = self.get_momentum()
    
    def print_properties(self):
        print ("particle species  :", self.species)
        print ("particle charge   :", self.charge)
        print ("particle mass     :", self.mass, "MeV/c^2")
        print ("particle energy   :", self.energy, "MeV")
        print ("particle momentum :", self.momentum, "MeV/c") 
        print ("particle gamma    :", self.gamma)
        print ("particle beta     :", self.beta)
