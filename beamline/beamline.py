import sys
from elements import *
from utils.diagnostics import *
from utils.logs import *

class Beamline(object):
    types = ["drift", "sbend", "rbend", "quadrupole", "sextupole", "octupole", "solenoid", "rfcavity", "marker"]
    
    def __init__(self, name, lattice, diag=False):
        self.name = name.lower()
        self.lattice = lattice
        self.sliced_lattice = []
        self.construct_beamline()
        self.diag = diag
        self.num_beamline_elements = len(self.lattice)
        
        if self.diag:
            self.beamline_diagnostics = Beamline_diagnostics("beamline.h5")
        
    def construct_beamline(self):
        for element in self.lattice:
            elmtype = element.element_properties["type"]
            if elmtype not in self.__class__.types:
                print_error("The element {} type is not in the type list".format(elemtype))
                return
            
    def propagate_beamline(self, bunch):
        if self.diag:
            self.beamline_diagnostics.save_bunch_diagnostics(bunch)
        index = 0
        length = 0
        for element in self.lattice:
            element.propagate(bunch)
            element_name = element.element_properties["name"]
            element_type = element.element_properties["type"]
            element_length = element.element_properties["length"]
            length += element_length
            
            emit_x, emit_y = bunch.get_emittance()
            
            print ("%10d %10s %10s %10.5f %10.5f %10d/%10d %10.5f %10.5f" % (index, element_name, element_type, element_length, \
                                                   length, bunch.get_num_particles(), bunch.get_original_num_particles(), \
                                                                             emit_x*1e6, emit_y*1e6))
            index += 1
            
            if self.diag:
                self.beamline_diagnostics.save_bunch_diagnostics(bunch)
            
    def propagate_sliced_beamline(self, bunch):
        for element in self.sliced_lattice:
            element.propagate(bunch)
            
    def print_beamline(self):
        length = 0
        for element in self.lattice:
            length += element.element_properties["length"]
            print ("%5s %10s %6.3f %6.3f %6.3f" % (element.element_properties["name"], element.element_properties["type"], \
                                             element.element_properties["length"], element.element_properties["strength"], length))
            
    def print_sliced_beamline(self):
        length = 0
        for element in self.sliced_lattice:
            length += element.element_properties["length"]
            print ("%5s %10s %6.3f %6.3f %6.3f" % (element.element_properties["name"], element.element_properties["type"], \
                                             element.element_properties["length"], element.element_properties["strength"], length))
        
    def get_num_beamline_elements(self):
        return (self.num_beamline_elements)
    
    def get_num_sliced_beamline_elements(self):
        print (len(self.sliced_lattice))
        
    def slice_beamline(self, slicen):
        for element in self.lattice:
            new_element_list = element.slice_element(slicen)
            for new_element in new_element_list:
                self.sliced_lattice.append(new_element)
            