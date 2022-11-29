import numpy as np
import os.path
import sys
from tables import *
from utils.logs import *

_x, _xp, _y, _yp, _tau, _dp = range(6)

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
        self.std_x = 0
        self.std_xp = 0
        self.std_y = 0
        self.std_yp = 0
        
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
        h5file.create_array(twiss_group, "emittance_x", bunch.twiss_x[2])
        h5file.create_array(twiss_group, "alpha_y", bunch.twiss_y[0])
        h5file.create_array(twiss_group, "beta_y", bunch.twiss_y[1])
        h5file.create_array(twiss_group, "emittance_y", bunch.twiss_y[2])

        self.get_bunch_diagnostics(bunch)
        
        h5file.create_array(diagnostics_group, "num_particles", bunch.num_particles)
        h5file.create_array(diagnostics_group, "std_x", self.std_x)
        h5file.create_array(diagnostics_group, "std_xp", self.std_xp)
        h5file.create_array(diagnostics_group, "std_y", self.std_y)
        h5file.create_array(diagnostics_group, "std_yp", self.std_yp)
        
        h5file.close()
        

    def get_bunch_diagnostics(self, bunch):
        self.std_x = np.std(bunch.state[_x])
        self.std_xp = np.std(bunch.state[_xp])
        self.std_y = np.std(bunch.state[_y])
        self.std_yp = np.std(bunch.state[_yp])
                            
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
    
    
class Beamline_diagnostics(Diagnostics):
    def __init__(self, filename):
        super().__init__(filename)
        
    def save_element_diagnostics(self, element):
        if os.path.exists(self.filename):
            print_error("%s already exists" % self.filename)
            return
        else:
            h5file = open_file(self.filename, mode="w", title="Beamline Data")
        group = h5file.create_group("/", "beamline", 'Beamline data')
        
        #for k, v in element.element_properties.items():
        #    if isinstance(v, str):
        #        h5file.create_array(group, k, [v])
        #    else:
        #        h5file.create_array(group, k, v)
        
        h5file.close()
        
"""