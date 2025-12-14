import numpy as np
import matplotlib.pyplot as plt
from ephemerides import sample_times
from tidal_strain import compute_timeseries
from tqdm import tqdm

def main():
    times = sample_times("2025-01-01T00:00:00", "2025-04-01T00:00:00", 600.0)
    bodies = ["Moon", "Sun", "Venus", "Jupiter", "Mars"]
    detectors = ["H1", "L1", "V1", "K1", "I1"]
    for det in tqdm(detectors, desc="Detectors", unit="detector"):
        ts = compute_timeseries(det, bodies, times)
        t = [s.t.to_datetime() for s in ts]
        darm = [s.eps_darm for s in ts]
        carm = [s.eps_carm for s in ts]

        plt.figure(figsize=(11,4))
        plt.plot(t, darm, label="DARM")
        plt.plot(t, carm, label="CARM")
        plt.title(f"{det} tidal strain")
        plt.xlabel("UTC")
        plt.ylabel("Strain")
        plt.legend()
        plt.tight_layout()
        plt.savefig('figures/' + f"tidal_{det}.png")
        plt.close()

if __name__ == "__main__":
    main()
