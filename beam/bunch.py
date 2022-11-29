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
    def __init__(self, species, energy, dimension, num_particles, twiss_x, twiss_y, seednum):
        self.dimension = dimension
        self.num_particles = num_particles
        self.seednum  = seednum
  
        if (self.dimension != 4) and (self.dimension != 6):
            print (self.dimension)
            print ("Dimension should be either 4 or 6", file=sys.stderr)
        self.twiss_x = twiss_x
        self.twiss_y = twiss_y
        self.particle = Particle(species, energy)
        self.state = np.zeros((self.dimension, self.num_particles))
        
    def update_num_particles(self):
        self.num_particles = self.state.shape[1]
    
    def update_state(self, new_state):
        self.state = new_state
        self.update_num_particles()
        #self.get_emiitance()
        #self.update_twiss_parameters()
    
    def get_emittance(self):
        return (self.twiss_x[2], self.twiss_y[2])
        pass
    
    def update_emittance(self):
        
        pass
    
    def get_twiss_paramters(self):
        return (self.twiss_x, self.twiss_y)
    
    def update_twiss_paramters(self):
        
        pass
    
    def generate_transverse_matched_beam_distribution(self):
        self.seednum  = seednum
        print('seed num:',seednum)
        if seednum == 0:
            seednum = np.randum  
        cov_mat = np.zeros((self.dimension, self.dimension))
        
        cov_mat[_x:_y,_x:_y] = _get_2D_covariance_matrix(self.twiss_x, self.dimension)
        cov_mat[_y:_tau,_y:_tau] = _get_2D_covariance_matrix(self.twiss_y, self.dimension)
            
        mean = np.zeros((4,), 'd') #[np.sqrt(cov_mat[_x,_x]), np.sqrt(cov_mat[_xp,_xp]), np.sqrt(cov_mat[_y,_y]), np.sqrt(cov_mat[_yp,_yp])]
        
        np.random.seed(seednum)
        part = np.random.multivariate_normal(mean, cov_mat, self.num_particles).T
        
        self.state[_x,:] = part[_x,:]
        self.state[_xp,:] = part[_xp,:]
        self.state[_y,:] = part[_y,:]
        self.state[_yp,:] = part[_yp,:]
        print(part[1,:])
        return self.state
    
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
        
        self.state[_x,:] = part[_x,:]
        self.state[_xp,:] = part[_xp,:]
        self.state[_y,:] = part[_y,:]
        self.state[_yp,:] = part[_yp,:]
        
        return self.state
    
    def print_bunch_properties(self):
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
        print ("particle s                :", self.particle.s)
        
        
        