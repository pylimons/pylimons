import sys
import copy
import numpy as np

class Element(object):
    types = ["drift", "sbend", "rbend", "quadrupole", "sextupole", "octupole", "solenoid", "rfcavity", "marker"]
    properties = ["name", "type", "length", "strength", "angle", "phi", "k1", "ks", "aperture"]
    aperture_types = ["rectangular", "circular", "elliptical"]
    
    def __init__(self, name, elmtype, length=0, strength=0, aperture=[]):
        if elmtype.lower() not in self.__class__.types:
            print ("The element {} type is not in the type list".format(elmtype.lower()), file=sys.stderr)
            return

        self.element_properties = {}
        if len(aperture) > 1:
            if aperture[0].lower() not in self.__class__.aperture_types:
                print ("The aperture type is not properly defined")
            else:
                self.element_properties["aperture"] = aperture
        else:
            self.element_properties["aperture"] = "Not defined"

        self.element_properties["name"] = name.lower()
        self.element_properties["type"] = elmtype.lower()
        self.element_properties["length"] = length
        self.element_properties["strength"] = strength
        
    def set_element_property(self, **param):
        for k, v in param.items():
            if k.lower() == "type":
                print ("type cannot be changed", file=sys.stderr)
            elif k.lower() in self.__class__.properties:
                self.element_properties[k.lower()] = v
            else:
                print ("Not a proper property", file=sys.stderr)
                
    def get_element_property(self, prop):
        if prop.lower() in self.__class__.properties:
            print ("The element's {} is {}".format(prop.lower(), self.element_properties[prop.lower()]))
        else:
            print ("The property {} is not defined".format(prop.lower()))

    def set_aperture_properties(self, param):
        if param[0].lower() in self.__class__.aperture_types:
            self.element_properties["aperture"] = param
        else:
            print ("Not a proper aperture attributes", file=sys.stderr)

    def get_aperture_properties(self):
        if self.element_properties["aperture"] == "Not defined":
            return 0
        else:
            return self.element_properties["aperture"]
        #if prop.lower() in self.__class__.aperture_properties:
        #    print ("The aprture's {} is {}".format(prop.lower(), self.aperture_attributes[prop.lower()]))
        #else:
        #    print ("The property {} is not defined".format(prop.lower()))
        #    return 0

    def print_element_properties(self):
        print ("element name     :", self.element_properties["name"])
        print ("element type     :", self.element_properties["type"])
        print ("element length   :", self.element_properties["length"])
        print ("element strength :", self.element_properties["strength"])
        print ("element aperture :", self.element_properties["aperture"])
        
    def propagate(self, bunch):
        pass
    
    def apply_aperture(self, bunch):
        particles = bunch.state
        aperture_type = self.element_properties["aperture"][0].lower()
        if aperture_type == "rectangular":
            from elements.aperture import Rectangular_aperture
            height = self.element_properties["aperture"][1]
            width = self.element_properties["aperture"][2]
            aperture = Rectangular_aperture([aperture_type, height, width])
            new_particle_state, loss = aperture.apply_rectangular_aperture(particles)
            bunch.update_state(new_particle_state)
        elif aperture_type == "circular":
            from elements.aperture import Circular_aperture
            r = self.element_properties["aperture"][1]
            aperture = Circular_aperture([aperture_type, r])
            new_particle_state, loss = aperture.apply_circular_aperture(particles)
            bunch.update_state(new_particle_state)
        elif aperture_type == "elliptical":
            from elements.aperture import Elliptical_aperture
            ax = self.element_properties["aperture"][1]
            bx = self.element_properties["aperture"][2]
            aperture = Elliptical_aperture([aperture_type, ax, bx])
            new_particle_state, loss = aperture.apply_elliptical_aperture(particles)
            bunch.update_state(new_particle_state)
            
    def element_copy(self, new_element_name):
        new_element = copy.deepcopy(self)
        new_element.element_properties["name"] = new_element_name.lower()
        return new_element
    
    def slice_element(self, slicen):
        new_length = self.element_properties["length"] / slicen
        element_name = self.element_properties["name"]
        element_type = self.element_properties["type"]
        element_strength = self.element_properties["strength"]
        if element_type == "sbend":
            new_strength = element_strength / slicen
        else:
            new_strength = element_strength
        element_list = []
        for i in range(0, slicen):
            new_element_name = element_name + ("_%d" % i)
            new_element = self.element_copy(new_element_name)
            new_element.set_element_property(length = new_length)
            new_element.set_element_property(strength = new_strength)
            element_list.append(new_element)
            
        return (element_list)
        
            