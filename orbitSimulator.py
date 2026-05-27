from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt


def two_body_ode(t, state):
    # unpack state
    x = state[0]
    y = state[1]
    vx = state[2]
    vy = state[3]
    mu = 3.986 * 10**14

    # compute distance from Earth
    r = (x**2 + y**2)**0.5

    # compute acceleration from gravity
    ax = -mu * (x / r**3)
    ay = -mu * (y / r**3)

    # return derivatives
    return [vx, vy, ax, ay]


if __name__ == "__main__":
    speeds = [6500, 7500, 8500, 9500, 10500]
    t_start = 0
    hours = [2, 2, 6, 10, 128]
    t_marker = 2 * 60 * 60  # 2 hours in seconds

    plt.figure(figsize=(6, 6))

    for i in range(len(speeds)):
        if i == 0:
            continue
        state0 = [7_000_000, 0, 0, speeds[i]]

        t_end = hours[i] * 60 * 60

        t_eval = np.linspace(t_start, t_end, 10000)

        y0 = state0
        t_span = (t_start, t_end)

        sol = solve_ivp(two_body_ode,  t_span, y0, t_eval=t_eval, method='RK45')

        print(sol.y.shape)
        print(sol.y[:, 0])
        print(sol.y[:, -1]) 

        x = sol.y[0]
        y = sol.y[1]

        plt.plot(x, y, label=f"vy0 = {speeds[i]} m/s")
        if i == 0:
            plt.plot(x[0], y[0], "o", label="start (t=0)")

        idx = np.argmin(np.abs(sol.t - t_marker))

        plt.scatter(sol.y[0, idx], sol.y[1, idx])                                                                          

    earth_radius = 6.371e6

    theta = np.linspace(0, 2*np.pi, 300)
    earth_x = earth_radius * np.cos(theta)
    earth_y = earth_radius * np.sin(theta) 
    
    plt.plot(earth_x, earth_y, label="Earth surface")

    plt.axis("equal")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    plt.title("Spacecraft trajectory")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.xlim(-1.5e7, 1.5e7)
    plt.ylim(-1.5e7, 1.5e7) 
    plt.show()

