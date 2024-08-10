import data as dt
from penalty_function import penalty
import genetic_algorithm as ga
import numpy as np
from timeit import default_timer as timer
from pso import pso  # Ensure this imports the function or class you implemented earlier

# Hybrid system using genetic algorithm and particle swarm optimization
def hybrid_system():
    # Load data and functions
    slot_presentation, presentation_presentation, presentation_supervisor, supervisor_preference = dt.load()

    # Initialize matrices
    slot_no = slot_presentation.shape[0]
    presentation_no = slot_presentation.shape[1]
    population_size = 10
    population = np.empty([population_size, slot_no, presentation_no], dtype=np.int8)
    penalty_points = np.empty(population_size, dtype=int)

    # Create initial population
    for i in range(population_size):
        chromosome = ga.generate_chromosome(slot_presentation)
        population[i] = chromosome
        penalty_point = penalty(chromosome, presentation_presentation, presentation_supervisor, supervisor_preference)[0]
        penalty_points[i] = penalty_point

    # Sort initial population based on penalty points
    population = population[penalty_points.argsort()]
    penalty_points = penalty_points[penalty_points.argsort()]

    # Run genetic algorithm for 600 generations
    ga_max_generations = 600
    population, penalty_points, ga_plot_data = \
        ga.reproduction(ga_max_generations, population, penalty_points, presentation_presentation,
                        presentation_supervisor, supervisor_preference)

    # Run particle swarm optimization after running genetic algorithm
    best_candidate, best_penalty_point, pso_plot_data = pso(
        num_particles=population_size,
        iterations=5000,
        initial_candidates=population,
        penalty_point=penalty_points,
        presentation_presentation=presentation_presentation,
        presentation_supervisor=presentation_supervisor,
        supervisor_preference=supervisor_preference
    )

    # Write result data
    constraint_counts = penalty(best_candidate, presentation_presentation, presentation_supervisor, supervisor_preference)
    plot_data = np.concatenate([ga_plot_data, pso_plot_data])
    dt.write(best_candidate, supervisor_preference, constraint_counts, plot_data)


start = timer()
hybrid_system()
print("\nExecution Time of Hybrid System:", round(timer() - start, 2), "seconds")
