import numpy as np
import os.path
import sys
from tables import *
from utils.logs import *

_x, _xp, _y, _yp, _tau, _dp = range(6)


def get_bunch_diagnostics(bunch):
    std_x = np.std(bunch.state[_x])
    std_xp = np.std(bunch.state[_xp])
    std_y = np.std(bunch.state[_y])
    std_yp = np.std(bunch.state[_yp])
    
    return (std_x, std_xp, std_y, std_yp)


"""
def _get_dtype(data):
    fields = []
    for (key, value) in data.items():
        # make strings go to the next 64 character boundary
        # pytables requires an 8 character boundary
        if isinstance(value, str):
            value += ' ' * (64 - (len(value) % 64))

        if isinstance(value, dict):
            fields.append((key, get_dtype(value)))
        else:
            value = np.array(value)
            fields.append((key, '%s%s' % (value.shape, value.dtype)))
    return np.dtype(fields)


def _recurse_row(row, base, data):
    for k, v in data.items():
        new = base + k
        if isinstance(v, dict):
            _recurse_row(row, new + '/', v)
        else:
            row[new] = v


def _add_row(table, data):
    row = table.row
    for k, v in data.items():
        if isinstance(v, dict):
            _recurse_row(row, k + '/', v)
        else:
            row[k] = v
    row.append()
    table.flush()
"""
    

class Diagnostics():
    def __init__(self, filename):
        self.filename = filename
    
    def save_logs(self):
        pass

    
class Particle_diagnostics(Diagnostics):
    def __init__(self, filename):
        super().__init__(filename)
        
    def save_particle_diagnostics(self, particle):
        if os.path.exists(self.filename):
            print_error("%s already exists" % self.filename)
            return
        else:
            h5file = open_file(self.filename, mode="w", title="Particle Data")
            
        group = h5file.create_group("/", "particle", 'particle data')

        h5file.create_array(group, "species", [particle.species])
        h5file.create_array(group, "charge", particle.charge)
        h5file.create_array(group, "mass", particle.mass)
        h5file.create_array(group, "energy", particle.energy)
        h5file.create_array(group, "momentum", particle.momentum)
        h5file.create_array(group, "gamma", particle.gamma)
        h5file.create_array(group, "beta", particle.beta)
        
        h5file.close()


class Bunch_diagnostics(Diagnostics):
    def __init__(self, filename):
        super().__init__(filename)
        
    def save_bunch_diagnostics(self, bunch):
        if os.path.exists(self.filename):
            print_error("%s already exists" % self.filename)
            return
        else:
            h5file = open_file(self.filename, mode="w", title="Bunch Data")
        twiss_group = h5file.create_group("/", "twiss", 'Twiss data')
        diagnostics_group = h5file.create_group("/", "diagnostics", "Bunch diagnostics data")
        
        h5file.create_array("/", "particles", bunch.state)
        
        h5file.create_array(twiss_group, "alpha_x", bunch.twiss_x[0])
        h5file.create_array(twiss_group, "beta_x", bunch.twiss_x[1])
        h5file.create_array(twiss_group, "emit_x", bunch.twiss_x[2])
        h5file.create_array(twiss_group, "alpha_y", bunch.twiss_y[0])
        h5file.create_array(twiss_group, "beta_y", bunch.twiss_y[1])
        h5file.create_array(twiss_group, "emit_y", bunch.twiss_y[2])

        std_x, std_xp, std_y, std_yp = get_bunch_diagnostics(bunch)
        
        h5file.create_array(diagnostics_group, "num_particles", bunch.num_particles)
        h5file.create_array(diagnostics_group, "std_x", std_x)
        h5file.create_array(diagnostics_group, "std_xp", std_xp)
        h5file.create_array(diagnostics_group, "std_y", std_y)
        h5file.create_array(diagnostics_group, "std_yp", std_yp)
        
        h5file.close()

    
class Beamline_diagnostics(Diagnostics):
    def __init__(self, filename):
        super().__init__(filename)
    
    def create_arrays(self):
        h5file = open_file(self.filename, mode="w", title="Beamline Data")
        beamline_group = h5file.create_group("/", "beamline", 'Beamline data')
        twiss_group = h5file.create_group("/", "twiss", 'Twiss data')
        diagnostics_group = h5file.create_group("/", "diagnostics", "Bunch diagnostics data")
        
        s = Float64Atom()
        h5file.create_earray(beamline_group, "s", s, shape=(0,))
        
        alpha_x = Float64Atom()
        beta_x = Float64Atom()
        emit_x = Float64Atom()
        alpha_y = Float64Atom()
        beta_y = Float64Atom()
        emit_y = Float64Atom()
            
        h5file.create_earray(twiss_group, "alpha_x", alpha_x, shape=(0,))
        h5file.create_earray(twiss_group, "beta_x", beta_x, shape=(0,))
        h5file.create_earray(twiss_group, "emit_x", emit_x, shape=(0,))
        h5file.create_earray(twiss_group, "alpha_y", alpha_y, shape=(0,))
        h5file.create_earray(twiss_group, "beta_y", beta_y, shape=(0,))
        h5file.create_earray(twiss_group, "emit_y", emit_y, shape=(0,))
        
        num_particles = Int32Atom()
        std_x = Float64Atom()
        std_xp = Float64Atom()
        std_y = Float64Atom()
        std_yp = Float64Atom()
            
        h5file.create_earray(diagnostics_group, "num_particles", num_particles, shape=(0,))
        h5file.create_earray(diagnostics_group, "std_x", std_x, shape=(0,))
        h5file.create_earray(diagnostics_group, "std_xp", std_xp, shape=(0,))
        h5file.create_earray(diagnostics_group, "std_y", std_y, shape=(0,))
        h5file.create_earray(diagnostics_group, "std_yp", std_yp, shape=(0,))

        h5file.close()
        
        return (h5file)
    
    def save_bunch_diagnostics(self, bunch):
        if not os.path.exists(self.filename):
            self.create_arrays()
        
        h5file = open_file(self.filename, mode="a")

        h5file.root.beamline.s.append(np.array([bunch.particle.s]))
        
        h5file.root.twiss.alpha_x.append(np.array([bunch.twiss_x[0]]))
        h5file.root.twiss.beta_x.append(np.array([bunch.twiss_x[1]]))
        h5file.root.twiss.emit_x.append(np.array([bunch.twiss_x[2]]))
        h5file.root.twiss.alpha_y.append(np.array([bunch.twiss_y[0]]))
        h5file.root.twiss.beta_y.append(np.array([bunch.twiss_y[1]]))
        h5file.root.twiss.emit_y.append(np.array([bunch.twiss_y[2]]))
        
        std_x, std_xp, std_y, std_yp = get_bunch_diagnostics(bunch)
        
        h5file.root.diagnostics.num_particles.append(np.array([bunch.num_particles]))
        h5file.root.diagnostics.std_x.append(np.array([std_x]))
        h5file.root.diagnostics.std_xp.append(np.array([std_xp]))
        h5file.root.diagnostics.std_y.append(np.array([std_y]))
        h5file.root.diagnostics.std_yp.append(np.array([std_yp]))
                
        h5file.close()        


"""
class Element_diagnostics(Diagnostics):
    def __init__(self, filename):
        super().__init__(filename)
        
    def save_element_diagnostics(self, element):
        if os.path.exists(self.filename):
            print_error("%s already exists" % self.filename)
            return
        else:
            h5file = open_file(self.filename, mode="w", title="Element Data")
        group = h5file.create_group("/", "element", 'Element data')
        
        element_dtype = _get_dtype(element.element_properties)
        table = h5file.create_table(group, "element", element_dtype)
        _add_row(table, element.element_properties)
        
        #h5file.create_table(group, "element", element.element_properties)
        
        #for k, v in element.element_properties.items():
        #    if isinstance(v, str):
        #        h5file.create_array(group, k, [v])
        #    else:
        #        h5file.create_array(group, k, v)
        
        h5file.close()
"""
