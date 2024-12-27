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

Since Lorentz' force work is zero in the absence of an electric field, conservation of the cinetic energy is guaranteed. The particle is only going to be deflected, but not accelerated or slowed in its motion. This means we need a conservative scheme if possible.

Below are three possible schemes that can be used in the code.

### Euler scheme

Most simple scheme for this equation is Euler's scheme. It is of order 1 and doesn't preserve cinetic energy because it is not reversible.

$$\begin{align}
    v_x^{n+1} = v_x^{n} + dt \frac{qB(x_n,y_n)}{m} v_y^n \\
    v_y^{n+1} = v_y^{n} - dt \frac{qB(x_n,y_n)}{m} v_x^n \\
    x_{n+1} = x_n + dt v_x^n
    y_{n+1} = y_n + dt v_y^n
\end{align}$$

### Central finite differences

$$\begin{align}
    v_x^{n+1} &= v_x^{n-1} + 2dt \frac{qB(x_n,y_n)}{m} v_y^n \\
    v_y^{n+1} &= v_y^{n-1} - 2dt \frac{qB(x_n,y_n)}{m} v_x^n \\
    x_{n+1} &= x_n + dt v_x^n \\
    y_{n+1} &= y_n + dt v_y^n
\end{align}$$

This scheme is of order 1 and requires two integrations steps. The initial solution at time dt is set using one Euler step at the beginning. It is reversible and preserves cinetic energy.

### Verlet's method

Verlet's one-step method in its vector form can be written as follows:

$$\begin{align}
    X_{n+1} &= X_n + dt V_n + \frac{dt^2}{2} A_n \\
    V_{n+1} &= V_n + \frac{dt}{2} (A_n + A_{n+1})
\end{align}$$

where $A_n$ is the acceleration at $x_n$: 

$$ A_n = \frac{qB(x_n, y_n)}{m} \left(\begin{array}{cc} 0 & 1 \\\ -1 & 0 \end{array}\right) V_n = M(x_n, y_n)V_n$$

Thus the iteration step on $V$ can be rewritten as:

$$ \left( I_2 - \frac{dt}{2}M(x_{n+1}, y_{n+1}) \right)V_{n+1} = V_n + \frac{dt}{2} A_n $$

$V_{n+1}$ is then computed by solving the $2 \times 2$ linear system above.

This method is of the same order as the centered difference scheme from the previous paragraph and preserves the cinetic energy as well. These two methods differ by a factor of about $10$ in terms of norm-2 error, meaning we can use a greater $dt$ with Verlet's step and reduce computation cost.

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