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

    speeds = [(mu/7_000_000)**0.5]
    t_start = 0
    t_end = 4 * 60 * 60
    t_burn = 2 * 60 * 60
    t_marker = 2 * 60 * 60
    t_eval_burn = np.linspace(t_start, t_burn, 5000)
    t_eval_end = np.linspace(t_burn, t_end, 5000)
    t_eval = np.linspace(t_start, t_end, 5000)
    t_span = (t_start, t_end)

    target_state0 = [7_000_000, 0, 0, speeds[0]]
    chaser_state0 = [7_000_000, -500_000, 500, speeds[0]]

    target_sol = solve_ivp(two_body_ode, t_span, target_state0, t_eval=t_eval, dense_output=True, method='DOP853', rtol=1e-6)
    chaser_sol = solve_ivp(two_body_ode, (t_start, t_burn), chaser_state0, t_eval=t_eval_burn, dense_output=True, method='DOP853', rtol=1e-6)

    target_marker_state = target_sol.sol(t_burn)
    chaser_before_burn_state = chaser_sol.y[:, -1]

    chaser_after_burn_state = apply_burn(chaser_before_burn_state, [500, 0])

    chaser_sol2 = solve_ivp(two_body_ode, (t_burn, t_end), chaser_after_burn_state, t_eval=t_eval_end, dense_output=True, method='DOP853', rtol=1e-6)

    target_before = target_sol.sol(t_eval_burn)
    target_after = target_sol.sol(t_eval_end)

    dx_before = chaser_sol.y[0] - target_before[0]
    dy_before = chaser_sol.y[1] - target_before[1]
    distance_before = np.sqrt(dx_before**2 + dy_before**2)

    dx_after = chaser_sol2.y[0] - target_after[0]
    dy_after = chaser_sol2.y[1] - target_after[1]
    distance_after = np.sqrt(dx_after**2 + dy_after**2)

    plt.figure(figsize=(8, 5))

    plt.plot(t_eval_burn, distance_before, label="Before burn")
    plt.plot(t_eval_end, distance_after, label="After burn")
    plt.axvline(t_burn, color="black", linestyle="--", linewidth=1, label="Burn time")

    plt.xlabel("time (s)")
    plt.ylabel("distance between spacecraft (m)")
    plt.title("Chaser-Target Distance Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(7, 7))

    plt.plot(target_sol.y[0], target_sol.y[1], label="Target")
    plt.plot(chaser_sol.y[0], chaser_sol.y[1], label="Chaser before burn")
    plt.plot(chaser_sol2.y[0], chaser_sol2.y[1], label="Chaser after burn")
    plt.scatter(target_marker_state[0], target_marker_state[1], s=90, marker="o", label="Target at 2 hours")
    plt.scatter(chaser_before_burn_state[0], chaser_before_burn_state[1], s=90, marker="x", label="Chaser at 2 hours")

    plt.plot(
        earth_radius * np.cos(theta),
        earth_radius * np.sin(theta),
        label="Earth surface"
    )

    plt.axis("equal")
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    plt.title("Chaser and Target Trajectories")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.show()                                           

    
    

