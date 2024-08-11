from penalty_function import penalty
import numpy as np

# Particle Swarm Optimization (PSO) algorithm for Presentation Scheduling
def pso(num_particles, max_iterations, initial_candidate, penalty_point, presentation_presentation,
        presentation_supervisor, supervisor_preference):
    
    # Initialize particle positions and velocities
    particles = np.array([np.copy(initial_candidate) for _ in range(num_particles)])
    velocities = np.random.uniform(-1, 1, particles.shape)

    # Initialize personal bests and global best
    personal_best_positions = np.copy(particles)
    personal_best_penalties = np.full(num_particles, penalty_point)
    global_best_position = np.copy(initial_candidate)
    global_best_penalty = penalty_point

    w = 0.5  # inertia weight
    c1 = 1.5 # cognitive (particle) weight
    c2 = 0.5  # social (swarm) weight

    plot_data = []
    iteration = 0

    while iteration < max_iterations:
        for i in range(num_particles):
            # Update velocity
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = w * velocities[i] + \
                            c1 * r1 * (personal_best_positions[i] - particles[i]) + \
                            c2 * r2 * (global_best_position - particles[i])

            # Update particle position
            particles[i] = particles[i] + velocities[i]
            particles[i] = np.clip(particles[i], 0, 1)  # Ensure the particle stays within bounds

            # Discretize positions (0 or 1)
            particles[i] = np.where(particles[i] >= 0.5, 1, 0)

            # Calculate penalty for the current particle
            current_penalty = penalty(particles[i], presentation_presentation, presentation_supervisor, supervisor_preference)[0]

            # Update personal best
            if current_penalty < personal_best_penalties[i]:
                personal_best_positions[i] = np.copy(particles[i])
                personal_best_penalties[i] = current_penalty

            # Update global best
            if current_penalty < global_best_penalty:
                global_best_position = np.copy(particles[i])
                global_best_penalty = current_penalty

        # Log the best penalty at each iteration
        plot_data.append(global_best_penalty)

        # Print status every 50 iterations
        if iteration % 50 == 0:
            print("[Iteracion ", iteration, "] PSO - Best Penalty Point: ", global_best_penalty, sep="")

        iteration += 1

    return global_best_position, global_best_penalty, plot_data