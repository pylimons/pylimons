from beam import Bunch

twiss_x = [-1.5, 10, 10e-6]
twiss_y = [1.5, 10, 10e-6]
seednum = 5
bunch = Bunch('electron', 10, 4, 10000, twiss_x, twiss_y, seednum)
print(seednum)

particles = bunch.generate_transverse_matched_beam_distribution()


bunch.print_bunch_properties()