from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
mu = 3.986 * 10**14
earth_radius = 6.371e6
theta = np.linspace(0, 2*np.pi, 300)
    

def two_body_ode(t, state):
    # unpack state
    x = state[0]
    y = state[1]
    vx = state[2]
    vy = state[3]
    

    # compute distance from Earth
    r = (x**2 + y**2)**0.5

    # compute acceleration from gravity
    ax = -mu * (x / r**3)
    ay = -mu * (y / r**3)

    # return derivatives
    return [vx, vy, ax, ay]

def apply_burn(state, delta_v):
    # state = [x, y, vx, vy]
    # delta_v = [dvx, dvy]
    # return the updated state
    return [state[0], state[1], state[2] + delta_v[0], state[3] + delta_v[1]]

            
if __name__ == "__main__":

    # Week 1-4 Test
    speeds = [(mu/7_000_000)**0.5, 7500, 8500, 9500, 10500, (2**0.5)*(mu/7_000_000)**0.5] # 
    t_start = 0
    burns = [1, 1, 3, 5, 64, 100] # 
    hours = [4, 4, 12, 20, 256, 400] # 
    t_marker = 2 * 60 * 60  # 2 hours in seconds
    delta_vs = [[0, 100], [0, -100], [100, 0], [-100, 0], [100, 100], [-100, -100], [-100, 100], [100, -100]]

    for delta_v in delta_vs:
        fig, axes = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
        axes = axes.flatten()    
        for i in range(len(speeds)):
            ax = axes[i]

            state0 = [7_000_000, 0, 0, speeds[i]]

            t_burn = burns[i] * 60 * 60

            t_end = hours[i] * 60 * 60

            # how long

            t_eval_burn = np.linspace(t_start, t_burn, 10000)

            t_eval_end = np.linspace(t_burn, t_end, 10000)

            y0 = state0

            t_span_burn = (t_start, t_burn)
            t_span_end = (t_burn, t_end)

            sol1 = solve_ivp(two_body_ode,  t_span_burn, y0, t_eval=t_eval_burn, method='DOP853', rtol=1e-6) # last arg makes the solver more accurate

            state1 = sol1.y[:, -1]

            state2 = apply_burn(state1, delta_v=delta_v)

            sol2 = solve_ivp(two_body_ode, t_span_end, state2, t_eval=t_eval_end, method='DOP853', rtol=1e-6)

            
            ax.plot(sol1.y[0], sol1.y[1], label="Before burn")
            ax.plot(sol2.y[0], sol2.y[1], label="After burn")

            burn_x = sol1.y[0, -1]
            burn_y = sol1.y[1, -1]

            ax.scatter(burn_x, burn_y, s=80, label="Burn location")

            if i == 0:
                ax.scatter(sol1.y[0, 0], sol1.y[1, 0], s=80, label="start (t=0)")
            
            ax.plot(
            earth_radius * np.cos(theta),
            earth_radius * np.sin(theta),
            label="Earth surface"
            )

            ax.set_aspect("equal")
            ax.set_title(f"Initial vy = {speeds[i]} m/s")
            ax.grid(True)

        fig.suptitle(f"Burn Δv = {delta_v} m/s", fontsize=14)
        plt.show()                                           

    
    

