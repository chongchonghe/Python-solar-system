#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from astroquery.jplhorizons import Horizons

sim_start_date = "2019-01-01"     # simulating a solar system starting from this date
sim_duration = 2 * 365                # (int) simulation duration in days
m_earth = 5.9722e24 / 1.98847e30  # Mass of Earth relative to mass of the sun
m_moon = 7.3477e22 / 1.98847e30

class Object:

    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r    = np.array(r, dtype=np.float)
        self.v    = np.array(v, dtype=np.float)
        self.xs = []
        self.ys = []
        self.plot = ax.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
        self.line, = ax.plot([], [], color=color, linewidth=1.4)

class SolarSystem:

    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')
        
    def add_planet(self, planet):
        self.planets.append(planet)

    def evolve(self):
        dt = 1.0
        self.time += dt
        plots = []
        lines = []
        for i2, p in enumerate(self.planets):
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)  # in units of AU/day^2
            if p.name == 399:         # Force from the Moon to Earth
                dr = p.r - self.planets[3].r  # trick here, assuming moon is the 4th object
                acc += -2.959e-4 * m_moon * dr / np.sum(dr**2)**(3./2)
            if p.name == 301:         # Force from earth to the Moon
                dr = p.r - self.planets[2].r
                acc += -2.959e-4 * m_earth * dr / np.sum(dr**2)**(3./2)
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            plots.append(p.plot)
            if i2 != 3:          # ignore trajectory lines of the Moon
                p.line.set_xdata(p.xs)
                p.line.set_ydata(p.ys)
                lines.append(p.line)
        if len(p.xs) > 10000:
            raise SystemExit("Stopping after a long run to prevent memory overflow")
        self.timestamp.set_text('Date: ' + Time(self.time, format='jd', out_subfmt='date').iso)
        return plots + lines + [self.timestamp]

plt.style.use('dark_background')
fig = plt.figure(figsize=[6, 6])
ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
ax.set_aspect('equal')
ax.axis('off')
ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd
colors = ['gray', 'orange', 'blue', 'yellow', 'chocolate']
sizes = [0.38, 0.95, 1., 0.27, 0.53]
names = ['Mercury', 'Venus', 'Earth-Moon', 'Earth-Moon', 'Mars']
for i, nasaid in enumerate([1, 2, 399, 301, 4]):
    obj = Horizons(id=nasaid, location="@sun", epochs=ss.time, id_type='id').vectors()
    ss.add_planet(Object(nasaid, 20 * sizes[i], colors[i], 
                         [np.double(obj[xi]) for xi in ['x', 'y', 'z']], 
                         [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
    ax.text(0, - ([.47, .73, 1, 1.02, 1.5][i] + 0.1),
            names[2] if i in [2, 3] else names[i], color=colors[i], zorder=1000,
            ha='center', fontsize='large')
def animate(i):
    return ss.evolve()
ani = animation.FuncAnimation(fig, animate, repeat=False, # init_func=init,
                              frames=sim_duration, blit=True, interval=20,)
plt.show()
# ani.save('solar_system_6in_200dpi.mp4', fps=40, dpi=200)
