import numpy as np
import astropy.units as u
from astropy.constants import GM_sun

G_SURFACE = 9.80665 * (u.m / u.s**2)
SHIDA_L2 = 0.0847

MU_SUN = GM_sun.to(u.m**3 / u.s**2)

GM_KM3_S2 = {
    "Mercury": 22031.868551,
    "Venus": 324858.592000,
    "Earth": 398600.435507,
    "Moon": 4902.800118,
    "Mars": 42828.375816,
    "Jupiter": 126712764.100000,
    "Saturn": 37940584.841800,
    "Uranus": 5794556.400000,
    "Neptune": 6836527.100580,
    "Pluto": 975.500000,
}

MU = {k: (v * 1e9) * (u.m**3 / u.s**2) for k, v in GM_KM3_S2.items()}
MU["Sun"] = MU_SUN
