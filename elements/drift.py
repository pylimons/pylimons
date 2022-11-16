import sys
import numpy as np
from .element import Element

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Drift(Element):
    def __init__(self, name, elmtype="drift", length=0):
        super().__init__(name, elmtype, length)
        
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
        
    def propagate(self, particles):
        transfer_map = self.get_transfer_matrix(particles.shape[0])
        
        new_particles = transfer_map @ particles
        
        if new_particles.shape != particles.shape:
            print ("something is wrong in propgation", file=sys.stderr)
            
        return new_particles
        