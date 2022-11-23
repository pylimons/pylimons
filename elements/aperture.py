import sys
import copy
import numpy as np

class Aperture():
    types = ["rectangular", "circular", "elliptical"]
    properties = ["width", "height", "radius", "horizontala_axis", "vertical_axis"]
    
    def __init__(self, aperture):
        if len(aperture) > 1:
            if aperture[0].lower() not in self.__class__.types:
                print ("The apeture type {} is not in the type list".format(aperture[0]), file=sys.stderr)
                return
            else:
                self.aperture_properties = {}
                if aperture[0].lower() == "rectangular":
                    self.aperture_properties["width"] = aperture[1]
                    self.aperture_properties["height"] = aperture[2]
                elif aperture[0].lower() == "circular":
                    self.aperture_properties["radius"] = aperture[1]
                elif aperture[0].lower() == "elliptical":
                    self.aperture_properties["horizontal_axis"] = aperture[1]
                    self.aperture_properties["vertical_axis"] = aperture[2]

class Rectangular_aperture(Aperture):
    def __init__(self, aperture):
        super().__init__(aperture)
        
    def apply_rectangular_aperture(self, particles):
        half_width = self.aperture_properties["width"] / 2
        half_height = self.aperture_properties["height"] / 2
        
        loss_index = []
        
        if (half_width <= 0) or (half_height <= 0):
            print ("The width and height of the rectangular aperture should be greater than zero", file=sys.stderr)
            return
        
        else:
            for i in range(len(particles[1])):
                x = particles[0, i]
                y = particles[2, i]
                if (np.abs(x) > half_width) or (np.abs(y) > half_height):
                    loss_index.append(i)
                    
            new_particles = np.delete(particles, loss_index, axis=1)
            loss = len(loss_index)
            
            return (new_particles, loss)


class Circular_aperture(Aperture):
    def __init__(self, aperture):
        super().__init__(aperture)
        
    def apply_circular_aperture(self, particles):
        r = self.aperture_properties["radius"]
        r2 = r * r
        loss_index = []
        
        if r <= 0:
            print ("The radius of the circular aperture should be greater than zero", file=sys.stderr)
            return
        
        else:
            for i in range(len(particles[1])):
                x = particles[0, i]
                y = particles[2, i]
                rsquare = x*x + y*y
                if (rsquare > r2):
                    loss_index.append(i)
                    
            new_particles = np.delete(particles, loss_index, axis=1)
            loss = len(loss_index)
            
            return (new_particles, loss)


class Elliptical_aperture(Aperture):
    def __init__(self, aperture):
        super().__init__(aperture)
        
    def apply_elliptical_aperture(self, particles):
        a = self.aperture_properties["horizontal_axis"]
        b = self.aperture_properties["vertical_axis"]

        loss_index = []
        
        if (a <= 0) or (b <= 0):
            print ("The horizontal and vertical axes of the elliptical aperture should be greater than zero", file=sys.stderr)
            return
        
        else:
            for i in range(len(particles[1])):
                x = particles[0, i]
                y = particles[2, i]
                rsquare = (x * x) / (a * a) + (y * y) / (b * b)
                if (rsquare > 1):
                    loss_index.append(i)
                    
            new_particles = np.delete(particles, loss_index, axis=1)
            loss = len(loss_index)
            
            return (new_particles, loss)