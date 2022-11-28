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
        self.state = np.zeros((self.dimension, self.num_particles))
        
    def update_num_particles(self):
        self.num_particles = self.state.shape[1]
    
    def update_state(self, new_state):
        self.state = new_state
        self.update_num_particles()
        self.update_emittance()
    
    def get_emittance(self):
        return (self.twiss_x[2], self.twiss_y[2])
    
    def update_emittance(self):
        #print (self.twiss_x[2])
        sigma_x  = np.mean(self.state[_x,:]**2)
        sigma_xp = np.mean(self.state[_xp,:]**2)
        sigma_xxp = np.mean(self.state[_x] * self.state[_xp])
        sigma_y  = np.mean(self.state[_y,:]**2)
        sigma_yp = np.mean(self.state[_yp,:]**2)
        sigma_yyp = np.mean(self.state[_y] * self.state[_yp])
        
        emittance_x = np.sqrt(sigma_x*sigma_xp - sigma_xxp * sigma_xxp)
        emittance_y = np.sqrt(sigma_y*sigma_yp - sigma_yyp * sigma_yyp)

        self.twiss_x[2] = emittance_x
        self.twiss_y[2] = emittance_y
        #print (self.twiss_x[2], emittance_x, '\n')
    
    def get_twiss_paramters(self):
        return (self.twiss_x, self.twiss_y)
    
    def propagate_twiss_parameters(self, twiss, mat):
        new_twiss = [0, 0, twiss[2]]
        alpha0 = twiss[0]
        beta0 = twiss[1]
        gamma0 = (1 + alpha0 * alpha0) / beta0
        
        new_twiss[1] = beta0 * mat[_x,_x]**2 + alpha0 * (-2 * mat[_x,_x] * mat[_x,_xp]) + gamma0 * mat[_x,_xp]**2
        new_twiss[0] = beta0 * (-mat[_x,_x] * mat[_xp,_x]) + alpha0 * (mat[_x,_x] * mat[_xp,_xp] + mat[_x,_xp] * mat[_xp,_x]) + gamma0 * (-mat[_x,_xp] * mat[_xp,_xp])
        
        return (new_twiss)
    
    def update_twiss_paramters(self, transfer_map):
        map_x = transfer_map[_x:_y, _x:_y]
        map_y = transfer_map[_y:_tau, _y:_tau]

        self.twiss_x = self.propagate_twiss_parameters(self.twiss_x, map_x)
        self.twiss_y = self.propagate_twiss_parameters(self.twiss_y, map_y)
        
    def generate_transverse_matched_beam_distribution(self):

        cov_mat = np.zeros((self.dimension, self.dimension))
        
        cov_mat[_x:_y,_x:_y] = _get_2D_covariance_matrix(self.twiss_x, self.dimension)
        cov_mat[_y:_tau,_y:_tau] = _get_2D_covariance_matrix(self.twiss_y, self.dimension)
            
        mean = np.zeros((4,), 'd') #[np.sqrt(cov_mat[_x,_x]), np.sqrt(cov_mat[_xp,_xp]), np.sqrt(cov_mat[_y,_y]), np.sqrt(cov_mat[_yp,_yp])]
        
        part = np.random.multivariate_normal(mean, cov_mat, self.num_particles).T
        
        self.state[_x,:] = part[_x,:]
        self.state[_xp,:] = part[_xp,:]
        self.state[_y,:] = part[_y,:]
        self.state[_yp,:] = part[_yp,:]
        
        self.update_emittance()
        
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
        
        
        