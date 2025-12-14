import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric

def geocentric_body_pos_gcrs_m(body: str, t: Time, ephem: str = "builtin") -> np.ndarray:
    body = body.lower()
    with solar_system_ephemeris.set(ephem):
        r_body = get_body_barycentric(body, t)
        r_earth = get_body_barycentric("earth", t)
    r_geo = (r_body - r_earth).xyz.to(u.m).value
    return np.array(r_geo, dtype=float)

def sample_times(start_utc: str, stop_utc: str, step_s: float) -> Time:
    t0 = Time(start_utc, scale="utc")
    t1 = Time(stop_utc, scale="utc")
    dt = step_s * u.s
    n = int(np.floor(((t1 - t0) / dt).to_value(u.dimensionless_unscaled)))
    return t0 + np.arange(n) * dt
