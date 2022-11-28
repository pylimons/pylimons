import sys
import numpy as np
from .element import Element

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Drift(Element):
    def __init__(self, name, elmtype="drift", length=0, **kwargs):
        super().__init__(name=name, elmtype=elmtype, length=length, **kwargs)
        
    def get_transfer_matrix(self, dim=4):
        L = self.element_properties["length"]
        mat = np.zeros([dim, dim], dtype=float)
        mat[_x, _x] = mat[_xp, _xp] = mat[_y, _y] = mat[_yp, _yp] = 1
        mat[_x, _xp] = mat[_y, _yp] = L
        
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
            print ("something is wrong in propgation", file=sys.stderr)
            
        if self.element_properties["aperture"] == 0:
            pass
        else:
            self.apply_aperture(bunch)
            
        bunch.update_twiss_paramters(transfer_map)
        