#!/usr/bin/env python
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta

class Object:                   # define the objects: the Sun, Earth, Mercury, etc
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r    = np.array(r, dtype=float)
        self.v    = np.array(v, dtype=float)
        self.xs = []
        self.ys = []
        self.plot = plt.scatter(r[0], r[1], color=color, s=rad**2, edgecolors=None, zorder=10)
        self.line, = plt.plot([], [], color=color, linewidth=1.4)

class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = plt.text(.03, .94, 'Date: ', color='w', transform=plt.gca().transAxes, fontsize='x-large')
    def add_planet(self, planet):
        self.planets.append(planet)
    def evolve(self): # evolve the trajectories
        dt = 1
        self.time += timedelta(dt)
        plots = []
        lines = []
        for i, p in enumerate(self.planets):
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)  # in units of AU/day^2
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            plots.append(p.plot)
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
            lines.append(p.line)
        if len(p.xs) > 10000:
            raise SystemExit("Stopping after a long run to prevent memory overflow")
        self.timestamp.set_text('Date: {}'.format(self.time.isoformat()))
        return plots + lines + [self.timestamp]

def main(save=False):
    matplotlib.use('Agg' if save else 'TkAgg')
    plt.style.use('dark_background')
    fig = plt.figure(figsize=[6, 6])
    ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
    ax.set_aspect('equal')
    ax.axis('off')
    with open("planets.json", 'r') as f:
        planets = json.load(f)
    ss = SolarSystem(Object("Sun", 28, 'red', [0, 0, 0], [0, 0, 0]))
    ss.time = datetime.strptime(planets["date"], '%Y-%m-%d').date()
    colors = [plt.get_cmap('Paired')(i) for i in [0, 6, 3, 11]]
    texty = [.47, .73, 1, 1.5]
    for i, nasaid in enumerate([1, 2, 3, 4]): # The 1st, 2nd, 3rd, and 4th planet in solar system
        planet = planets[str(nasaid)]
        ss.add_planet(Object(nasaid, 20 * planet["size"], colors[i], planet["r"], planet["v"]))
        ax.text(0, - (texty[i] + 0.1), planet["name"], color=colors[i], zorder=1000, ha='center', fontsize='large')
    def animate(i):
        return ss.evolve()
    sim_duration = 2 * 365                # (int) simulation duration in days
    ani = animation.FuncAnimation(fig, animate, repeat=False, frames=sim_duration, blit=True, interval=20,)
    if save:
        ani.save('solar_system_150dpi.mp4', fps=60, dpi=150)
    else:
        plt.show()

main(save=False)                # Real-time animation
# main(save=True)                 # Save as a gif. Use it when no graphics is available.