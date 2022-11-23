import sys
import numpy as np
from .element import Element

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Solenoid(Element):
    def __init__(self, name, elmtype="drift", length=0, strength=0, **kwargs):
        super().__init__(name=name, elmtype=elmtype, length=length, strength=strength, **kwargs)
        self.element_properties["ks"] = strength
        
    def get_transfer_matrix(self, dim=4):
        L = self.element_properties["length"]
        ks = self.element_properties["ks"]
        
        mat = np.zeros([dim, dim], dtype=float)
        
        ksL = ks * L
        
        cosksL = np.cos(ksL)
        sin2ksL = np.sin(2 * ksL)
        
        mat[_x, _x] = mat[_xp, _xp] = mat[_y, _y] = mat[_yp, _yp] = cosksL * cosksL
        mat[_x, _xp] = mat[_y, _yp] = sin2ksL / (2 * ks)
        mat[_xp, _x] = mat[_yp, _y] = - sin2ksL * ks / 2
        mat[_x, _y] = mat[_xp, _yp] = sin2ksL / 2
        mat[_y, _x] = mat[_yp, _xp] = - sin2ksL / 2
        mat[_x, _yp] = sin2ksL * sin2ksL / ks
        mat[_yp, _x] = sin2ksL * sin2ksL * ks
        mat[_xp, _y] = - sin2ksL * sin2ksL * ks
        mat[_y, _xp] = - sin2ksL / ks
        
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
            