from penalty_function import penalty
import numpy as np
import genetic_algorithm as ga

# Particle Swarm Optimization (PSO) algorithm for Presentation Scheduling
def pso(num_particles, max_iterations, initial_candidate, penalty_point, presentation_presentation,
        presentation_supervisor, supervisor_preference, slot_presentation):
    
    sc_array = np.array([1, 5, 10])

    # Initialize particle positions and velocities
    particles =  np.array([np.clip(np.random.uniform(0, 1, initial_candidate.shape), 0, 1) for _ in range(num_particles)])
    velocities = np.array([np.random.uniform(-1, 1, initial_candidate.shape) for _ in range(num_particles)])

    # Crea la población inicial
    for i in range(num_particles):
        # Genera un cromosoma aleatorio
        chromosome = ga.generate_chromosome(slot_presentation)
        particles[i] = chromosome  # Asigna el cromosoma a la población
        
        # Calcula los puntos de penalización para el cromosoma
        # penalty_point = penalty(chromosome, presentation_presentation, presentation_supervisor, supervisor_preference)[0]
        # personal_best_penalties[i] = penalty_point # Asigna el punto de penalización al vector
   
    # Initialize personal bests and global best
    particles[0] = initial_candidate
    personal_best_positions = np.copy(particles)
    personal_best_penalties = np.array([np.dot(sc_array, penalty(particle, presentation_presentation, presentation_supervisor, supervisor_preference)) for particle in particles])
    global_best_position = np.copy(initial_candidate)
    global_best_penalty = penalty_point

    w = 0.7 # inertia weight
    c1 = 1.49 # cognitive (particle) weight
    c2 = 1.49  # social (swarm) weight

    plot_data = []
    iteration = 0

    while iteration < max_iterations:
        for i in range(num_particles):
            # Update velocity
            r1, r2 = np.random.uniform(0, 1, initial_candidate.shape), np.random.uniform(0, 1, initial_candidate.shape)
            velocities[i] = w * velocities[i] + \
                            c1 * np.multiply(r1, (personal_best_positions[i] - particles[i])) + \
                            c2 * np.multiply(r2, (global_best_position - particles[i]))

            # Update particle position
            particles[i] = particles[i] + velocities[i]
            particles[i] = np.clip(particles[i], 0, 1)  # Ensure the particle stays within bounds

            # Discretize positions (0 or 1)
            particles[i] = np.where(particles[i] >= 0.5, 1, 0)

            # Calculate penalty for the current particle
            current_penalty = np.dot(sc_array, penalty(particles[i], presentation_presentation, presentation_supervisor, supervisor_preference))

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
            print("[Iteración ", iteration, "] PSO - Penalty Point: ", global_best_penalty, sep="")

        iteration += 1

    return global_best_position, global_best_penalty, plot_data