import numpy as np

# Define the force function (example: harmonic oscillator)
def force(x):
    k = 1.0  # Spring constant
    return -k * x

# Initialize parameters
dt = 0.01  # Time step
num_steps = 1000  # Number of steps
x = np.zeros(num_steps)  # Position array
v = np.zeros(num_steps)  # Velocity array
x[0] = 1.0  # Initial position
v[0] = 0.0  # Initial velocity

# Verlet integration
for i in range(1, num_steps):
    if i == 1:
        # First step using Euler method to get second position
        x[i] = x[i-1] + v[i-1] * dt + 0.5 * force(x[i-1]) * dt**2
    else:
        # Verlet integration
        x[i] = 2 * x[i-1] - x[i-2] + force(x[i-1]) * dt**2
        v[i-1] = (x[i] - x[i-2]) / (2 * dt)  # Update velocity

# Final velocity update
v[-1] = (x[-1] - x[-2]) / dt

# Example plot
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

plt.plot(np.arange(num_steps) * dt, x)
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Verlet Integration')
plt.show()