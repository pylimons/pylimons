import sys
from elements import *

class Beamline(object):
    types = ["drift", "sbend", "rbend", "quadrupole", "sextupole", "octupole", "solenoid", "rfcavity", "marker"]
    
    def __init__(self, name, lattice):
        self.name = name.lower()
        self.lattice = lattice
        self.construct_beamline()
        
    def construct_beamline(self):
        for element in self.lattice:
            elmtype = element.element_properties["type"]
            if elmtype not in self.__class__.types:
                print ("The element {} type is not in the type list".format(elemtype), file=sys.stderr)
                return
            
    def propagate(self, bunch):
        for element in self.lattice:
            element.propagate(bunch)
            
    def print_beamline(self):
        length = 0
        for element in self.lattice:
            length += element.element_properties["length"]
            print ("%5s %10s %6.3f %6.3f %6.3f" % (element.element_properties["name"], element.element_properties["type"], \
                                             element.element_properties["length"], element.element_properties["strength"], length))
        
    def get_num_beamline_elements(self):
        print (len(self.lattice))
            