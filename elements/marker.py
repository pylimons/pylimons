import sys
import numpy as np
from .element import Element

_x, _xp, _y, _yp, _tau, _dp = range(6)

class Marker(Element):
    def __init__(self, name, elmtype="marker"):
        super().__init__(name, elmtype)
        
    def propagate(self, bunch):
        return bunch
        