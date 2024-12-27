import numpy as np

###  Differential equation parameters ###

q = -1.60217663 * 10**(-19) # electron charge
m =  9.1093837 * 10**(-31) # electron mass

def B_const(*args):
    return 1.0 * 10**(-3) # constant 1mT magnetic field

def B_step(x, y):
    if x <= -0.5 or x >= 0.5:
        return B_const()
    else:
        return 0.0

def B_lin(x, y):
    return B_const() * x # linear magnetic field

def B_sq(x, y):
    return B_const() * x**2 # parabolic magnetic field

def B_cube(x, y):
    return B_const() * x**3 # x**3 magnetic field

def B_abs(x, y):
    return abs(B_const() * x) # symetrical linear magnetic field

def omega(x, y, B):
    return q * B(x, y) / m

def M(x, y, B):
    return omega(x, y, B) * np.array([[0, 1.0], [-1.0, 0]])

def a(p, B):
    # Acceleration of the particle
    # dv/dt = M * v
    return M(p.x, p.y, B).dot([p.vx, p.vy])