import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import GCRS, ITRS, CartesianRepresentation, SkyCoord

def gcrs_to_itrs_vec(t: Time, r_gcrs_m: np.ndarray) -> np.ndarray:
    rep = CartesianRepresentation(r_gcrs_m * u.m)
    c = SkyCoord(rep, frame=GCRS(obstime=t))
    itrs = c.transform_to(ITRS(obstime=t)).cartesian
    return np.array([itrs.x.to_value(u.m), itrs.y.to_value(u.m), itrs.z.to_value(u.m)], dtype=float)
