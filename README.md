# LorentzTrajectory

This code is a simple simulator for a particle moving in a magnetic field. It can solve the mechanical PDE using central finite difference or Verlet's method. A benchmark of the two methods can be generated with benchmark.py

## Usage

You will need numpy and matplotlib to run the code, it is all Python. To generate the particle trajectories, use:

    python3 plot.py

To generate the the convergence plot for the two integration schemes, use:

    python3 benchmark.py

## Equations

A particle of charge $q$ is launched at speed $\vec{V_0}$ (included in plane $Oxy$) from point $(0, 0)$ at time $t=0$. The magnetic field in the area is orthogonal to the trajectories's plane, and directed towards us : $\vec{B} = B(x, y) \vec{u_z}$. The force that drives the particle's movement is Lorentz' force : 

$$\vec{F_{Lorentz}} = q\vec{v} \wedge \vec{B} $$


Newton's third law yields the following system of ODEs:

$$ \begin{align}
    \partial_t v_x &= \frac{qB(x,y)}{m} v_y \\
    \partial_t v_y &= -\frac{qB(x,y)}{m} v_x \\
    \partial_t x &= v_x \\
    \partial_t y &= v_y
    \end{align} $$

### Euler scheme

Most simple scheme for this equation is Euler's scheme. It is of order 1 but unfortunately it doesn't preserve cinetic energy because it is not reversible.

$$ \begin{align}
    v_x^{n+1} = v_x^{n} + dt \frac{qB(x_n,y_n)}{m} v_y^n 
    v_y^{n+1} = v_y^{n} - dt \frac{qB(x_n,y_n)}{m} v_x^n 
\end{align}
$$
## Results

Below are the plots of the particle's trajectory for different forms of magnetic field.

![constant](./figures/constant_field.png)
![v-shape](./figures/v-shape_field.png)
![linear](./figures/linear_field.png)
![parabolic](./figures/parabolic_field.png)
![step](./figures/step_field.png)

## Methods

Two numerical methods are implemented here: a two-step central finite difference scheme and Verlet's method. Both are consistent and stable (I think Verlet's method is unconditionnally stable in our case). They are order one methods, see below their convergence graphs:

![convergence](./convergence.png)