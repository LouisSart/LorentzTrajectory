from physics import *
import numpy as np

### Numerical schemes ###

class Particle:
    def __init__(self, X, V):
        self.x, self.y = X
        self.vx, self.vy = V


def euler(p, pp, dt, B):
    # explicit euler iteration
    # p : particle's state at t
    # pp : particle's state at t - dt (unused)
    # dt : time step
    # B : magnetic field function
    
    vx = p.vx + 2 * omega(p.x, p.y, B) * dt * p.vy
    vy = p.vy - 2 * omega(p.x, p.y, B) * dt * p.vx

    x = p.x + dt * vx
    y = p.y + dt * vy

    return Particle((x, y), (vx, vy))

def centered_scheme(p, pp, dt, B):
    # two-step scheme using centered finite differences
    # p : particle's state at t
    # pp : particle's state at t - 1
    # dt : time step
    # B : magnetic field function

    if pp is None:
        return euler(p, pp, dt, B)
    else:
        vx = pp.vx + 2 * omega(p.x, p.y, B) * dt * p.vy
        vy = pp.vy - 2 * omega(p.x, p.y, B) * dt * p.vx

        x = p.x + dt * p.vx
        y = p.y + dt * p.vy

        return Particle((x, y), (vx, vy))

def verlet_scheme(p, pp, dt, B):
    # One-step Verlet scheme
    # Preserves energy, is reversible
    # p : particle's state at t
    # pp : particle state at t - dt (unused)
    # dt : time step
    # B : magnetic field function
    
    ax, ay = a(p, B) # acceleration at t
    x = p.x + dt * p.vx + (dt**2 / 2) * ax # x position at t + dt
    y = p.y + dt * p.vy + (dt**2 / 2) * ay # y position at t + dt
    
    A = (np.eye(2) - (dt/2) * M(x, y, B))
    b = np.array([p.vx + (dt/2) * ax, p.vy + (dt/2) * ay])
    V = np.linalg.solve(A, b) # velocity at t + dt
    
    return Particle((x, y), tuple(V))

def simulation(p0, tmax, scheme=centered_scheme, dt=10**-10, B=B_const):
    # run simulation of the particle's movement
    # up to t = tmax
    # p0, p1 : particle states at t=0 and t=dt

    p1 = scheme(p0, None, dt, B)
    trajectory = [p0, p1]
    t = dt
    while (t < tmax):
        p, pp = trajectory[-1], trajectory[-2]
        trajectory.append(scheme(p, pp, dt, B))
        t += dt
    
    return trajectory