import sys
import numpy as np
from .element import Element

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Sbend(Element):
    def __init__(self, name, elmtype="sbend", length=0, angle=0, **kwargs):
        super().__init__(name=name, elmtype=elmtype, length=length, **kwargs)
        self.element_properties['strength'] = angle
        self.element_properties['angle'] = angle
        self.element_properties['phi'] = angle * np.pi / 180
        
    def get_transfer_matrix(self, dim=4):
        L = self.element_properties["length"]
        phi = self.element_properties['phi']
        rho = L / phi
        
        mat = np.zeros([dim, dim], dtype=float)
        
        cosphi = np.cos(phi)
        sinphi = np.sin(phi)

        alpha = 0
        cosphi2 = np.cos(phi-alpha)
        sinphi2 = np.sin(phi-2*alpha)

        cosphi3 = np.cos(alpha)
        sinphi3 = np.sin(phi-2*alpha)

        
        mat[_x, _x] = mat[_xp, _xp] = cosphi2/cosphi3
        mat[_x, _xp] = rho * sinphi
        mat[_xp, _x] = - sinphi2 / rho /cosphi3**2
        
        mat[_y, _y] = mat[_yp, _yp] = 1
        mat[_y, _yp] = L
            
        #TODO
        #if dim == 6:
        #    mat[4, 4] = mat[5,5] = 1
        #    mat[4, 5] = self.length / (beta0 * gamma0)**2
        
        return mat



        # L = self.element_properties["length"]
        # phi = self.element_properties['phi']
        # rho = L / phi
        
        # mat = np.zeros([dim, dim], dtype=float)
        
        # cosphi = np.cos(phi)
        # sinphi = np.sin(phi)
        
        # mat[_x, _x] = mat[_xp, _xp] = cosphi
        # mat[_x, _xp] = rho * sinphi
        # mat[_xp, _x] = - sinphi / rho
        
        # mat[_y, _y] = mat[_yp, _yp] = 1
        # mat[_y, _yp] = L
            
        # #TODO
        # #if dim == 6:
        # #    mat[4, 4] = mat[5,5] = 1
        # #    mat[4, 5] = self.length / (beta0 * gamma0)**2
        
        # return mat

    def s_get_transfer_matrix(self, dim=4):
        L = self.element_properties["length"]
        phi = self.element_properties['phi']
        rho = L / phi
        
        mat1 = np.zeros([dim, dim], dtype=float)
        mat2 = np.zeros([dim, dim], dtype=float)

        cosphi = np.cos(phi)
        sinphi = np.sin(phi)
        
        mat1[_x, _x] = mat1[_xp, _xp] = 1
        mat1[_x, _xp] = rho * sinphi
        # mat1[_xp, _x] = - sinphi / rho
        
        mat1[_y, _y] = mat1[_yp, _yp] = 1
        mat1[_y, _yp] = L

        mat2[_x,_x] = mat2[_xp, _xp] = 1
        mat2[_xp, _x] = np.tan(phi/2)/rho

        mat2[_y, _y] = mat2[_yp, _yp] = 1
        mat2[_y, _yp] = L
        
        
        # mat2[_x,_x] = mat2[_xp, _xp] =1
        # mat2[_x, _xp] = np.sin(phi/2)*rho

        # mat2[_y, _y] = mat2[_yp, _yp] = 1
        # mat2[_y, _yp] = L

        mat = mat2 @ mat1 @ mat2
        #mat = mat2 @ mat

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

    def s_propagate(self, bunch):
        reference_particle = bunch.particle
        particles = bunch.state
        
        reference_particle.update_s(self.element_properties["length"])
        
        transfer_map = self.s_get_transfer_matrix(particles.shape[0])
        
        bunch.update_state(transfer_map @ particles)
        
        if bunch.state.shape != particles.shape:
            print ("something is wrong in propgation", file=sys.stderr)
            
        if self.element_properties["aperture"] == 0:
            pass
        else:
            self.apply_aperture(bunch)
                        