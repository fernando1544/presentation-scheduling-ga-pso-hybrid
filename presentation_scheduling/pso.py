from penalty_function import penalty
import numpy as np
from numba import njit

# Neighbourhood structures remain the same as before

@njit(cache=True)
def update_velocity(velocity, personal_best, global_best, candidate, w, c1, c2):
    r1, r2 = np.random.random(), np.random.random()
    cognitive = c1 * r1 * (personal_best - candidate)
    social = c2 * r2 * (global_best - candidate)
    new_velocity = w * velocity + cognitive + social
    return new_velocity

@njit
def update_position(candidate, velocity):
    # Update the candidate positions using the velocity
    candidate = candidate + velocity

    # Ensure position values are within a valid range [0, 1]
    candidate = np.clip(candidate, 0, 1)

    # Convert floating-point values to integer (0 or 1) using rounding and type casting
    candidate = np.round(candidate).astype(np.int8)

    return candidate

def pso(num_particles, iterations, initial_candidates, penalty_point, presentation_presentation,
        presentation_supervisor, supervisor_preference):
    w = 0.8  # Inertia weight
    c1 = 1.0  # Cognitive parameter
    c2 = 1.5  # Social parameter

    velocities = [np.zeros_like(initial_candidates[0]) for _ in range(num_particles)]
    personal_bests = initial_candidates.copy()
    personal_best_penalty = penalty_point.copy()

    global_best = initial_candidates[np.argmin(penalty_point)]
    global_best_penalty = min(penalty_point)

    plot_data = []

    for iteration in range(iterations):
        for i in range(num_particles):
            velocities[i] = update_velocity(velocities[i], personal_bests[i], global_best, initial_candidates[i], w, c1, c2)
            initial_candidates[i] = update_position(initial_candidates[i], velocities[i])

            new_penalty_point = penalty(initial_candidates[i], presentation_presentation, presentation_supervisor, supervisor_preference)[0]

            if new_penalty_point < personal_best_penalty[i]:
                personal_bests[i] = initial_candidates[i]
                personal_best_penalty[i] = new_penalty_point

            if new_penalty_point < global_best_penalty:
                global_best = initial_candidates[i]
                global_best_penalty = new_penalty_point

        plot_data.append(global_best_penalty)

        if iteration % 50 == 0:
            print("[Iteration ", iteration, "] PSO - Penalty Point: ", global_best_penalty, sep="")

    return global_best, global_best_penalty, plot_data
