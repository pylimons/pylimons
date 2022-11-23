import sys
import copy
import numpy as np

class Element(object):
    types = ["drift", "sbend", "rbend", "quadrupole", "sextupole", "octupole", "solenoid", "rfcavity", "marker"]
    properties = ["name", "type", "length", "strength", "angle", "phi", "k1", "ks", "aperture"]
    aperture_types = ["rectangular", "circular", "elliptical"]
    
    def __init__(self, name, elmtype, length=0, strength=0, aperture=[]):
        if elmtype.lower() not in self.__class__.types:
            print (elmtype.lower())
            print ("The element type is not in the type list", file=sys.stderr)
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

    def set_aperture_property(self, **param):
        for k, v in param.items():
            if k.lower() in self.__class__.aperture_properties:
                self.aperture_attributes[k.lower()] = v
            else:
                print ("Not a proper aperture property", file=sys.stderr)

    def get_aperture_property(self, prop):
        if prop.lower() in self.__class__.aperture_properties:
            print ("The aprture's {} is {}".format(prop.lower(), self.aperture_attributes[prop.lower()]))
        else:
            print ("The property {} is not defined".format(prop.lower()))

    def print_properties(self):
        print ("element name     :", self.element_properties["name"])
        print ("element type     :", self.element_properties["type"])
        print ("element length   :", self.element_properties["length"])
        print ("element strength :", self.element_properties["strength"])
        print ("element aperture :", self.element_properties["aperture"])
        
    def element_copy(self, new_element_name):
        new_element = copy.deepcopy(self)
        new_element.element_properties["name"] = new_element_name.lower()
        return new_element
    
    def propagate(self, bunch):
        pass
        