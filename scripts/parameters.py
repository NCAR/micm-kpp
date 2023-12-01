"""
conversion factors
"""
percent = 0.01
ppmv = 1.0e-6
ppbv = 1.0e-9

"""
physical constants
"""
N_Avogadro = 6.02214076e23

"""
typical concentrations by volume
"""
# dry air
c_N2 = 0.78
c_O2 = 0.21
c_Ar = 0.9 * percent
c_Ne = 0.002 * percent
c_He = 0.0005 * percent

# greenhouse gases
c_H2O = 4 * percent
c_CO2 = 400 * ppmv
c_CH4 = 2 * ppmv
c_N2O = 300 * ppbv
c_O3  = 40 * ppbv

# pollutants
# CO
# SO2
# H2SO4
# NO
# NO2
# HNO3
# O3
# VOCs
c_NOx = 10 * ppbv
