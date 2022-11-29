import sys
import numpy as np
from .element import Element

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Marker(Element):
    def __init__(self, name, elmtype="marker", **kwargs):
        super().__init__(name, elmtype, **kwargs)
        
    def propagate(self, bunch):
        if self.element_properties["aperture"] == 0:
            pass
        else:
            self.apply_aperture(bunch)
        
        print (bunch.twiss_x, bunch.twiss_y)
        
        return bunch
        