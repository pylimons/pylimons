import sys
import numpy as np
from .element import Element
from .utils.logs import *

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Quadrupole(Element):
    def __init__(self, name, elmtype="quadrupole", length=0, strength=0, **kwargs):
        super().__init__(name=name, elmtype=elmtype, length=length, strength=strength, **kwargs)
        self.element_properties["k1"] = strength
        
    def get_transfer_matrix(self, dim=4):
        L = self.element_properties["length"]
        k1 = self.element_properties["k1"]
        
        mat = np.zeros([dim, dim], dtype=float)
        
        absk1 = np.abs(k1)

        sqrk1 = np.sqrt(absk1)
        sqrk1L = sqrk1 * L
        
        cosk1L = np.cos(sqrk1L)
        sink1L = np.sin(sqrk1L)
        coshk1L = np.cosh(sqrk1L)
        sinhk1L = np.sinh(sqrk1L)
        
        focus_mat = np.zeros([2,2], dtype=float)
        defocus_mat = np.zeros([2,2], dtype=float)
        
        focus_mat[0, 0] = focus_mat[1, 1] = cosk1L
        focus_mat[0, 1] = sink1L / sqrk1
        focus_mat[1, 0] = - sqrk1 * sink1L
        
        defocus_mat[0, 0] = defocus_mat[1, 1] = coshk1L
        defocus_mat[0, 1] = sinhk1L / sqrk1
        defocus_mat[1, 0] = sqrk1 * sinhk1L
        
        if k1 > 0:
            mat[_x:_y, _x:_y] = focus_mat
            mat[_y:_tau, _y:_tau] = defocus_mat
        elif k1 < 0:
            mat[_x:_y, _x:_y] = defocus_mat
            mat[_y:_tau, _y:_tau] = focus_mat
        
        #TODO
        #if dim == 6:
        #    mat[4, 4] = mat[5,5] = 1
        #    mat[4, 5] = self.length / (beta0 * gamma0)**2
        
        return mat
        
    def propagate(self, bunch):
        reference_particle = bunch.particle
        particles = bunch.state
        
        reference_particle.update_s(self.element_properties["length"])
        
        transfer_map = self.get_transfer_matrix(particles.shape[0])
        
        bunch.update_state(transfer_map @ particles)
        
        if bunch.state.shape != particles.shape:
            print_error("something is wrong in propgation")
            
        if self.element_properties["aperture"] == 0:
            pass
        else:
            self.apply_aperture(bunch)
            
        bunch.update_twiss_paramters(transfer_map)
            