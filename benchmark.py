from lorentz import *

def exact(V0, tmax, dt):
    # V0 : initial speed along x axis
    # exact solution to the differential equation
    # with constant magnetic field
    # (circle with center (0, V0/omega) and radius V0/omega)
    # tmax : simulation real time duration
    # dt : time step

    time = np.arange(0, tmax, dt)
    om = omega(0, 0, B_const)
    trajectory = [Particle((0, 0), (V0, 0))]
    t = dt
    while t < tmax:
        x = V0 / om * np.sin(om * t)
        y = V0 / om * (np.cos(om * t) - 1)
        vx = V0 * np.cos(om * t)
        vy = V0 * np.sin(om * t)
        trajectory.append(Particle((x, y), (vx, vy)))
        t += dt

    return trajectory

def error(traj_1, traj_2):
    def dist(p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**.5
    return sum([dist(p1, p2) for p1, p2 in zip(traj_1, traj_2)])


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib import cm

    v0 = 10**8 # near speed of light initial speed
    d = 5 # travel distance of the particle
    tmax = d/v0 # simulation real time duration
    p0 = Particle((0, 0), (v0, 0)) # initial condition (horizontal speed)


    dts = [5e-9, 1e-9, 5e-10, 1e-10, 5e-11, 1e-11, 5e-12, 1e-12]
    c_dist = []
    v_dist = []
    for dt in dts:
        centered = simulation(p0, tmax, centered_scheme, dt, B_const)
        verlet = simulation(p0, tmax, verlet_scheme, dt, B_const)
        reference = exact(v0, tmax, dt)
        c_dist.append(error(centered, reference))
        v_dist.append(error(verlet, reference))
    
    plt.plot(dts, c_dist, label="Centered scheme")
    plt.plot(dts, v_dist, label="Verlet scheme")
    plt.xscale('log')
    plt.yscale('log')
    plt.gca().invert_xaxis()  # Reverse the x-axis
    plt.title('Convergence of Centered and Verlet Schemes')
    plt.xlabel('Time Step (s)')  # Add x-axis label
    plt.ylabel('Norm-2 Error')  # Add y-axis label
    plt.legend()
    plt.savefig("convergence")