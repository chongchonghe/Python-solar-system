#!/usr/bin/env python
"""
Fetch planet information from nasa.org and store it in a json file.
"""
import numpy as np
import json
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2018-01-01"     # simulating a solar system starting from this date
names = ['Mercury', 'Venus', 'Earth', 'Mars']
sizes = [0.38, 0.95, 1., 0.53]
nasaids = [1, 2, 3, 4]   # The 1st, 2nd, 3rd (399 and 301), 4th planet in solar system

data = dict(info="Solar planets database, including positions and velocities at the given date",
            date=sim_start_date)
for i in range(len(nasaids)):
    nasaid = nasaids[i]
    obj = Horizons(id=nasaid, location="@sun", epochs=Time(sim_start_date).jd, id_type='id').vectors()
    data[str(nasaid)] = {
        "name": names[i],
        "size": sizes[i],
        "r": [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
        "v": [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]
    }

with open("planets.json", 'w') as f:
    json.dump(data, f, indent=4)
