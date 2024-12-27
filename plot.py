import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm

from lorentz import *

def plot_trajectory(trajectory, B):

    p0 = trajectory[0]
    v0 = (p0.vx**2 + p0.vy**2)**.5
    x = np.array([p.x for p in trajectory])
    y = np.array([p.y for p in trajectory])

    x_width = max(x) - min(x)
    y_width = max(y) - min(y)
    xspan = np.arange(min(x)-0.1*x_width,max(x)+0.1*x_width,step=(x_width)/500)
    yspan = np.arange(min(y)-0.1*y_width,max(y)+0.1*y_width,step=(y_width)/500)
    extent = (min(xspan), max(xspan), min(yspan), max(yspan))


    fig, ax = plt.subplots()

    # Plot trajectory
    ax.plot(x, y, color='black')
    ax.arrow(p0.x, p0.y, 0.7*xspan[-1]*p0.vx/v0, 0.7*yspan[-1]*p0.vy/v0, length_includes_head=True, head_width=0.03, color="gold", label="V0")
    ax.text(p0.x + 1.05*(0.7*xspan[-1]*p0.vx/v0), p0.y + 1.05*(0.7*yspan[-1]*p0.vy/v0), r"$\overrightarrow{V_0}$", fontsize = 14, verticalalignment='center', color="black")
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    plt.locator_params(nbins=3) # Set number of ticks

    # Magnetic field colormap
    magfi_array = np.array([[B(x, y)*1000 for x in xspan] for y in yspan]) # Mag field in mT
    im = ax.imshow(magfi_array, extent=extent, cmap=cm.RdYlBu, aspect='auto')

    # Magnetic field colorbar
    shrink = 1 if y_width > x_width else y_width/x_width # Adjust colorbar size to data
    cbar = fig.colorbar(im, ax=ax, location = 'right', orientation='vertical', shrink=shrink, format="%3.1f")
    cbar.ax.set_ylabel('Magnetic field magnitude (mT)', ha = 'center', va='bottom', rotation=270)
    
    ax.set_aspect('equal', adjustable='box')  # Set equal scaling and adjust the box to fit the data
    return fig, ax

if __name__ == "__main__":

    ### Simulation input ###

    v0 = 10**8 # near speed of light initial speed
    d = 10 # travel distance of the particle
    tmax = d/v0 # simulation real time duration
    p0 = Particle((0, 0), (v0, 0)) # initial condition (horizontal speed)

    ### Constant magnetic field ###

    trajectory = simulation(p0, tmax, scheme=verlet_scheme, dt=10**-9, B=B_const)
    fig, ax = plot_trajectory(trajectory, B_const)
    ax.set_title("Particle trajectory in constant magnetic field")
    fig.savefig("constant_field")

    ### Step magnetic field ###

    trajectory = simulation(p0, tmax*0.8, scheme=verlet_scheme, dt = 10**-11, B=B_step)
    fig, ax = plot_trajectory(trajectory, B_step)
    ax.set_title("Particle trajectory in step magnetic field")
    fig.savefig("step_field")

    ### Linear magnetic field ###

    trajectory = simulation(p0, tmax*0.6, scheme=verlet_scheme, dt = 10**-9, B=B_lin)
    fig, ax = plot_trajectory(trajectory, B_lin)
    ax.set_title("Particle trajectory in linear magnetic field")
    fig.savefig("linear_field")

    ### V-shape magnetic field ###

    trajectory = simulation(p0, tmax, scheme=verlet_scheme, dt=10**-10, B=B_abs)
    fig, ax = plot_trajectory(trajectory, B_abs)
    ax.set_title("Particle trajectory in V-shape magnetic field")
    fig.savefig("v-shape_field")

    ### Parabolic magnetic field ###

    trajectory = simulation(p0, tmax, scheme=verlet_scheme, dt=10**-9, B=B_sq)
    fig, ax = plot_trajectory(trajectory, B_sq)
    ax.set_title("Particle trajectory in parabolic magnetic field")
    fig.savefig("parabolic_field")
