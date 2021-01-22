# Simulating the solar system with under 100 lines of code in Python

This is a Python program I wrote attempting to simulate a quite
realistic solar system with minimal lines of code.

![solar_system_6in_150dpi](https://user-images.githubusercontent.com/24463821/90344480-44543f00-dfe8-11ea-9b99-a640c0f26136.gif)

## Modules required

numpy, matplotlib, datetime

Optional: astroquery (to retrieve planets data from nasa.org and generate initial condition)

## How to run
With the required modules installed, simply run the program, e.g. in UNIX command line, with
```bash
python solar_system.py
```
Modify `sim_duration` in the beginning of the code to change the duration of the simulation.

To make a different initial condition, modify and run get_initial_condition.py.

## References

[JPL HORIZONS on-line solar system database][https://docs.astropy.org/en/stable/coordinates/solarsystem.html]
