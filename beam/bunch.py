import sys
import numpy as np
from .particle import Particle

_x, _xp, _y, _yp, _tau, _dp = range(6)

def _get_2D_covariance_matrix(twiss, dim):
    a, b, e = twiss
    c = (1 + a * a) / b
    
    cov_mat = np.zeros((2, 2))
    
    cov_mat[0,0] = e * b
    cov_mat[0,1] = cov_mat[1,0] = - e * a
    cov_mat[1,1] = e * c
    
    return (cov_mat)
         
class Bunch():
    def __init__(self, species, energy, dimension, num_particles, twiss_x, twiss_y):
        self.dimension = dimension
        self.num_particles = num_particles
        if (self.dimension != 4) and (self.dimension != 6):
            print (self.dimension)
            print ("Dimension should be either 4 or 6", file=sys.stderr)
        self.twiss_x = twiss_x
        self.twiss_y = twiss_y
        self.particle = Particle(species, energy)
        self.coordinates = np.zeros((self.dimension, self.num_particles))
    
    def generate_transverse_matched_beam_distribution(self):
        #ax, bx, ex = self.twiss_x
        #ay, by, ey = self.twiss_y
        
        #cx = (1 + ax * ax) / bx
        #cy = (1 + ay * ay) / by
        
        cov_mat = np.zeros((self.dimension, self.dimension))
        
        cov_mat[0:2,0:2] = _get_2D_covariance_matrix(self.twiss_x, self.dimension)
        cov_mat[2:4,2:4] = _get_2D_covariance_matrix(self.twiss_y, self.dimension)
        
        #cov_mat[0,0] = ex * bx
        #cov_mat[0,1] = cov_mat[1,0] = - ex * ax
        #cov_mat[1,1] = ex * cx
        
        #cov_mat[2,2] = ey * by
        #cov_mat[2,3] = cov_mat[3,2] = - ey * ay
        #cov_mat[3,3] = ey * cy
    
        mean = [np.sqrt(cov_mat[0,0]), np.sqrt(cov_mat[1,1]), np.sqrt(cov_mat[2,2]), np.sqrt(cov_mat[3,3])]
        
        part = np.random.multivariate_normal(mean, cov_mat, self.num_particles).T
        
        self.coordinates[_x,:] = part[_x,:]
        self.coordinates[_xp,:] = part[_xp,:]
        self.coordinates[_y,:] = part[_y,:]
        self.coordinates[_yp,:] = part[_yp,:]
        
        return self.coordinates
    
    #TODO
    def generate_6D_matched_beam_distribution(self):
        ax, bx, ex = self.twiss_x
        ay, by, ey = self.twiss_y
        
        cx = (1 + ax * ax) / bx
        cy = (1 + ay * ay) / by
        
        cov_mat = np.zeros((self.dimension, self.dimension))
        
        cov_mat[0,0] = ex * bx
        cov_mat[0,1] = cov_mat[1,0] = - ex * ax
        cov_mat[1,1] = ex * cx
        
        cov_mat[2,2] = ey * by
        cov_mat[2,3] = cov_mat[3,2] = - ey * ay
        cov_mat[3,3] = ey * cy
    
        mean = [np.sqrt(cov_mat[0,0]), np.sqrt(cov_mat[1,1]), np.sqrt(cov_mat[2,2]), np.sqrt(cov_mat[3,3])]
        
        part = np.random.multivariate_normal(mean, cov_mat, self.num_particles).T
        
        self.coordinates[_x,:] = part[_x,:]
        self.coordinates[_xp,:] = part[_xp,:]
        self.coordinates[_y,:] = part[_y,:]
        self.coordinates[_yp,:] = part[_yp,:]
        
        return self.coordinates
    
    def print_properties(self):
        print ("number of macro particles :", self.num_particles)
        print ("beta_x                    :", self.twiss_x[1], "m")
        print ("alpha_x                   :", self.twiss_x[0], "m^(1/2)")
        print ("emittance_x               :", self.twiss_x[2], "mm-mrad")
        print ("beta_y                    :", self.twiss_y[1], "m")
        print ("alpha_y                   :", self.twiss_y[0], "m^(1/2)")
        print ("emittance_y               :", self.twiss_y[2], "mm-mrad")
        print ("")
        print ("particle species          :", self.particle.species)
        print ("particle charge           :", self.particle.charge)
        print ("particle mass             :", self.particle.mass, "MeV/c^2")
        print ("particle energy           :", self.particle.energy, "MeV")
        print ("particle momentum         :", self.particle.momentum, "MeV/c") 
        print ("particle gamma            :", self.particle.gamma)
        print ("particle beta             :", self.particle.beta)
        
        
        