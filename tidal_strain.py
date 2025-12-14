import numpy as np
import astropy.units as u
from astropy.time import Time
from dataclasses import dataclass

from constants import MU, SHIDA_L2, G_SURFACE
from detectors import get_detector
from ephemerides import geocentric_body_pos_gcrs_m
from earth_rotation import gcrs_to_itrs_vec

@dataclass(frozen=True)
class StrainSample:
    t: Time
    eps_x: float
    eps_y: float
    eps_darm: float
    eps_carm: float

def tidal_tensor(mu_m3_s2: float, r_ecef_m: np.ndarray) -> np.ndarray:
    r = np.linalg.norm(r_ecef_m)
    n = r_ecef_m / r
    return (mu_m3_s2 / r**3) * (3.0 * np.outer(n, n) - np.eye(3))

def eps_along(u_hat: np.ndarray, E: np.ndarray) -> float:
    q = float(u_hat @ E @ u_hat)
    return float((SHIDA_L2 / G_SURFACE.to_value(u.m/u.s**2)) * q)

def compute_timeseries(detector_name: str, bodies: list[str], times: Time, ephem: str = "builtin"):
    det = get_detector(detector_name)
    ux, uy = det.ux_ecef, det.uy_ecef
    out = []
    for t in times:
        epsx = epsy = 0.0
        for b in bodies:
            mu = MU[b].to_value(u.m**3/u.s**2)
            r_gcrs = geocentric_body_pos_gcrs_m(b, t, ephem=ephem)
            r_ecef = gcrs_to_itrs_vec(t, r_gcrs)
            E = tidal_tensor(mu, r_ecef)
            epsx += eps_along(ux, E)
            epsy += eps_along(uy, E)
        out.append(StrainSample(t, epsx, epsy, epsx-epsy, 0.5*(epsx+epsy)))
    return out
