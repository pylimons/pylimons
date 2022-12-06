import sys
import numpy as np
from .element import Element
from utils import physical_constants as pconstants
from utils.logs import *

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Rfcavity(Element):
    def __init__(self, name, elmtype="rfcavity", length=0, strength=0, phase=0, freq=0, **kwargs):
        super().__init__(name=name, elmtype=elmtype, length=length, strength=strength, **kwargs)
        self.element_properties["gradient"] = strength
        self.element_properties["phase"] = phase * np.pi / 180
        self.element_properties["frequency"] = freq
        
    """
    def get_transfer_matrix(self, bunch, dim=4):
        L = self.element_properties["length"]
        gradient = self.element_properties["gradient"]
        phase = self.element_properties["phase"]
        f = self.element_properties["frequency"]
        
        k = 2 * np.pi * f / pconstants.c
        alpha = np.abs(bunch.particle.get_charge()) * gradient / bunch.particle.get_momentum()
        
        omega1 = k * np.sqrt(alpha * np.cos(phase) / (2 * np.pi))
        print (alpha, omega1)
        
        cos_omegal = np.cos(omega1 * L)
        sin_omegal = np.sin(omega1 * L)
        
        # transfer matrix
        mat = np.zeros([dim, dim], dtype=float)

        mat[_x, _x] = mat[_y, _y] = mat[_xp, _xp] = mat[_yp, _yp] = np.cos(omega1 * L)
        mat[_x, _xp] = mat[_y, _yp] = np.sin(omega1 * L) / omega1
        mat[_xp, _x] = mat[_yp, _y] = - omega1 * np.sin(omega1 * L)
        
        #TODO
        #if dim == 6:
        #    mat[4, 4] = mat[5,5] = 1
        #    mat[4, 5] = self.length / (beta0 * gamma0)**2
        
        return mat
    """
                            
    def get_transfer_matrix(self, bunch, dim=4):
        L = self.element_properties["length"]
        gradient = self.element_properties["gradient"]
        phase = self.element_properties["phase"]
        
        cos_phase = np.cos(phase)
        
        rest_mass = bunch.particle.get_rest_mass()
        initial_energy = bunch.particle.get_energy()
        gamma_i = bunch.particle.get_gamma()
        
        final_energy = initial_energy + np.abs(bunch.particle.charge) * gradient * cos_phase
        bunch.particle.update_energy(final_energy)
        gamma_f = bunch.particle.get_gamma()
        
        #print (initial_energy, final_energy)
        #print (gamma_i, gamma_f)
        #print (1 + initial_energy / rest_mass, 1 + final_energy / rest_mass)
        
        alpha = 1 / (8 * np.cos(phase)) * np.log(gamma_f / gamma_i)
        gamma_prime = (gamma_f - gamma_i) / (L * cos_phase)
        
        cos_alpha = np.cos(alpha)
        sin_alpha = np.sin(alpha)
        
        # transfer matrix
        mat = np.zeros([dim, dim], dtype=float)

        mat[_x, _x]   = mat[_y, _y]   = cos_alpha - np.sqrt(2) * cos_phase * sin_alpha
        mat[_x, _xp]  = mat[_y, _yp]  = np.sqrt(8) * (gamma_i / gamma_prime) * cos_phase * sin_alpha
        mat[_xp, _x]  = mat[_yp, _y]  = - (gamma_prime / gamma_f) * (cos_phase / np.sqrt(2) + 1 / (np.sqrt(8) * cos_phase)) * sin_alpha
        mat[_xp, _xp] = mat[_yp, _yp] = (gamma_i / gamma_f) * (cos_alpha + np.sqrt(2) * cos_phase * sin_alpha)
        
        #TODO
        #if dim == 6:
        #    mat[4, 4] = mat[5,5] = 1
        #    mat[4, 5] = self.length / (beta0 * gamma0)**2
        
        return mat
        
    def propagate(self, bunch):
        reference_particle = bunch.particle
        particles = bunch.state
        
        reference_particle.update_s(self.element_properties["length"])
        
        transfer_map = self.get_transfer_matrix(bunch, particles.shape[0])
        
        bunch.update_state(transfer_map @ particles)
        
        if bunch.state.shape != particles.shape:
            print_error("something is wrong in propgation")
            
        if self.element_properties["aperture"] == 0:
            pass
        else:
            self.apply_aperture(bunch)
            
        bunch.update_twiss_parameters(transfer_map)
            