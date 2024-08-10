import data as dt
from penalty_function import penalty
import genetic_algorithm as ga
import numpy as np
from timeit import default_timer as timer
from pso import pso

# Sistema híbrido que utiliza algoritmos genéticos y optimización por enjambre de partículas
def hybrid_system():
    # Carga los datos y las funciones necesarias
    slot_presentation, presentation_presentation, presentation_supervisor, supervisor_preference = dt.load()

    # Inicializa matrices y parámetros
    slot_no = slot_presentation.shape[0]  # Número total de slots
    presentation_no = slot_presentation.shape[1]  # Número total de presentaciones
    population_size = 10  # Tamaño de la población para el algoritmo genético
    population = np.empty([population_size, slot_no, presentation_no], dtype=np.int8)  # Matriz para almacenar la población
    penalty_points = np.empty(population_size, dtype=int)  # Vector para almacenar los puntos de penalización

    # Crea la población inicial
    for i in range(population_size):
        # Genera un cromosoma aleatorio
        chromosome = ga.generate_chromosome(slot_presentation)
        population[i] = chromosome  # Asigna el cromosoma a la población
        
        # Calcula los puntos de penalización para el cromosoma
        penalty_point = penalty(chromosome, presentation_presentation, presentation_supervisor, supervisor_preference)[0]
        penalty_points[i] = penalty_point # Asigna el punto de penalización al vector

    # Ordena la población inicial basada en los puntos de penalización
    population = population[penalty_points.argsort()]  # Ordena la población según los puntos de penalización
    penalty_points = penalty_points[penalty_points.argsort()]  # Ordena los puntos de penalización

    # Número máximo de generaciones para el algoritmo genético
    ga_max_generations = 100
    population, penalty_points, ga_plot_data = \
        ga.reproduction(ga_max_generations, population, penalty_points, presentation_presentation,
                        presentation_supervisor, supervisor_preference)

    # Ejecuta la optimización por enjambre de partículas después del algoritmo genético
    best_candidate, best_penalty_point, pso_plot_data = pso(
        num_particles=population_size,
        iterations=5000,
        initial_candidates=population,
        penalty_point=penalty_points,
        presentation_presentation=presentation_presentation,
        presentation_supervisor=presentation_supervisor,
        supervisor_preference=supervisor_preference
    )

     # Escribe los resultados
    # Combina los datos de gráficos del algoritmo genético
    constraint_counts = penalty(best_candidate, presentation_presentation, presentation_supervisor, supervisor_preference)
    plot_data = np.concatenate([ga_plot_data, pso_plot_data])
    
    dt.write(best_candidate, supervisor_preference, constraint_counts, plot_data) # Guarda los resultados

# Inicia el temporizador, ejecuta el sistema híbrido y calcula el tiempo de ejecución
start = timer()
hybrid_system()
print("\nTiempo de ejecución del sistema hibrido GA PSO:", round(timer() - start, 2), "segundos")
