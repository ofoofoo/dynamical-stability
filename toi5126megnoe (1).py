import rebound
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import os
import pdb
import random
import csv
from os.path import dirname, join as pjoin
import scipy.io as sio
from scipy.io import readsav
from astropy.io import fits
from astropy.table import Table
import seaborn as sns

# SET-UP
# Units: G = 1 Solar mass, AU, years/(2*pi)

G = 6.67408*10**(-11)   # gravitational constant 
Mearth = 5.9722*10**24  # kg
Rearth = 6.371*10**6  # meters
Msun = 1.98911*10**30 # kg
Rsun = 6.95*10**8 # meters
Mjup = 1.898*10**27  # kg
Rjup = 7.1492*10**7 # meters
year = 365.25*24*60*60  # years in seconds
AU = (G*Msun*(year**2)/(4.*np.pi**2))**(1./3.)  # meters

# System Parameters:
m_star = 1.22 # Solar masses

def megnoe(par):
    m1, m2, M1, M2, omega1, omega2 = par # unpack parameters
    m_star = 1.22
    sim = rebound.Simulation()
    sim.integrator = "whfast"
    sim.ri_whfast.safe_mode = 0
    delta_t = (1/20)*5.46/365.25  # years
    sim.dt = delta_t*2*np.pi
    sim.add(m = m_star) # star
    sim.add(m = m1, a = (m_star*(5.46/(365.25))**2)**(1/3), M=M1, omega=omega1, e = np.random.rayleigh(scale = 0.05)) #b
    sim.add(m = m2, a = (m_star*(17.9/(365.25))**2)**(1/3), M=M2, omega=omega2, e = np.random.rayleigh(scale = 0.05)) #c
    sim.move_to_com()
    sim.init_megno()
    sim.exit_max_distance = 5.
    try: #49007.5291
        sim.integrate(49007.5291*2.*np.pi, exact_finish_time=0) # integrate for 500 years, integrating to the nearest
    #timestep for each output to keep the timestep constant and preserve WHFast's symplectic nature
        megno = sim.calculate_megno() 
        return (megno, m1, m2)
    except rebound.Escape as error:
        return (10, m1, m2) # At least one particle got ejected, returning large MEGNO.

e1arr = np.linspace(0, 0.4, 20)
e2arr = np.linspace(0, 0.4, 20)

megnoearr = []
for i in range(20):
  for j in range(20):
    r2 = np.random.normal(4.43, 0.115)
    m2 = (1.74*(r2)**1.58)*(Mearth/Msun) 
    r1 = np.random.normal(4.897, 0.1)
    m1 = (1.74*(r1)**1.58)*(Mearth/Msun)
    for k in range(1):
      M1 = random.uniform(0, 2*np.pi)
      M2 = random.uniform(0, 2*np.pi)
      omega1 = random.uniform(0, 2*np.pi)
      omega2 = random.uniform(0, 2*np.pi)
      megno = megnoe((m1, m2, M1, M2, omega1, omega2))
      #print(megno)
      megnoearr.append(megno)
print(megnoearr)

