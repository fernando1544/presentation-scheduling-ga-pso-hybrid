from penalty_function import penalty
import numpy as np
import genetic_algorithm as ga

# Algoritmo del PSO
def pso(num_particles, max_iterations, initial_candidate, penalty_point, presentation_presentation,
        presentation_supervisor, supervisor_preference, slot_presentation):
    
    sc_array = np.array([1, 5, 10])

    # Inicializamos las posiciones de las particulas y las velocidades
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
   
    particles[0] = initial_candidate

    # Inicializamos las mejores posiciones del individuo y globales
    personal_best_positions = np.copy(particles)
    personal_best_penalties = np.array([np.dot(sc_array, penalty(particle, presentation_presentation, presentation_supervisor, supervisor_preference)) for particle in particles])
    global_best_position = np.copy(initial_candidate)
    global_best_penalty = penalty_point

    w = 0.7 # Inercia
    c1 = 1.49 # Coeficiente cognitivo
    c2 = 1.49  # Coeficiente social

    plot_data = []
    iteration = 0

    while iteration < max_iterations:
        for i in range(num_particles):
            # Actualizamos las velocidades
            r1, r2 = np.random.uniform(0, 1, initial_candidate.shape), np.random.uniform(0, 1, initial_candidate.shape)
            velocities[i] = w * velocities[i] + \
                            c1 * np.multiply(r1, (personal_best_positions[i] - particles[i])) + \
                            c2 * np.multiply(r2, (global_best_position - particles[i]))

            # Actualizamos la posición de la particula
            particles[i] = particles[i] + velocities[i]
            particles[i] = np.clip(particles[i], 0, 1)  # Nos aseguramos de que las particulas se mantengan entre los limites

            # Discretizamos la posicion (0 o 1)
            particles[i] = np.where(particles[i] >= 0.5, 1, 0)

            # Calculamos la penalty para la particula
            current_penalty = np.dot(sc_array, penalty(particles[i], presentation_presentation, presentation_supervisor, supervisor_preference))

            # Actualizamos el personal best
            if current_penalty < personal_best_penalties[i]:
                personal_best_positions[i] = np.copy(particles[i])
                personal_best_penalties[i] = current_penalty

            # Y el global...
            if current_penalty < global_best_penalty:
                global_best_position = np.copy(particles[i])
                global_best_penalty = current_penalty

        # Logueamos las best penalties
        plot_data.append(global_best_penalty)

        # Printeamos cada 50 iteraciones
        if iteration % 50 == 0:
            print("[Iteración ", iteration, "] PSO - Penalty Point: ", global_best_penalty, sep="")

        iteration += 1

    return global_best_position, global_best_penalty, plot_data