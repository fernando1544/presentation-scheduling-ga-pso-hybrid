from penalty_function import penalty
import numpy as np

# Genera una población inicial donde todas las restricciones duras han sido resueltas, excepto HC02
def generate_chromosome(slot_presentation):
    chromosome = np.copy(slot_presentation)  # Crea una copia de la presentación de los slots
    slot_no = chromosome.shape[0]  # Número total de slots
    presentation_no = chromosome.shape[1]  # Número total de presentaciones

    # Recorre cada presentación
    for presentation in range(presentation_no):
        while True:
            random_slot = np.random.randint(slot_no)  # Selecciona un slot aleatorio
            # Si el slot está disponible y vacío
            if chromosome[random_slot][presentation] == 0 and np.count_nonzero(chromosome[random_slot] == 1) == 0:
                chromosome[random_slot][presentation] = 1  # Asigna la presentación al slot
                break

    return chromosome  # Devuelve el cromosoma generado

# Selecciona 2 cromosomas basándose en la selección por torneo
def selection(population, penalty_points):
    tournament_size = 2  # Tamaño del torneo

    # Selecciona el primer cromosoma basado en la primera selección por torneo
    t1, t2 = np.random.choice(range(population.shape[0]), tournament_size)
    first = t1 if penalty_points[t1] <= penalty_points[t2] else t2

    # Asegura que los 2 cromosomas seleccionados no sean idénticos
    while True:
        # Selecciona el segundo cromosoma basado en la segunda selección por torneo
        t1, t2 = np.random.choice(range(population.shape[0]), tournament_size)
        second = t1 if penalty_points[t1] <= penalty_points[t2] else t2

        if second != first:
            break

    return population[first], population[second]  # Devuelve los dos cromosomas seleccionados

# Realiza un cruce de 2 puntos
def crossover(first_parent, second_parent):
    first_child = np.copy(first_parent)  # Crea una copia del primer padre
    second_child = np.copy(second_parent)  # Crea una copia del segundo padre
    presentation_no = first_parent.shape[1]  # Número total de presentaciones
    cutpoint1, cutpoint2 = np.random.choice(range(presentation_no), 2)  # Selecciona dos puntos de corte aleatorios

    if cutpoint1 > cutpoint2:
        cutpoint1, cutpoint2 = cutpoint2, cutpoint1  # Asegura que cutpoint1 sea menor que cutpoint2

    # Intercambia las presentaciones entre los dos padres desde cutpoint1 hasta cutpoint2
    first_child[:, cutpoint1:cutpoint2], second_child[:, cutpoint1:cutpoint2] = \
        second_child[:, cutpoint1:cutpoint2], np.copy(first_child[:, cutpoint1:cutpoint2])
    
    # Repara los hijos para corregir posibles violaciones de restricciones
    first_child = repair(first_child, cutpoint1, cutpoint2)
    second_child = repair(second_child, cutpoint1, cutpoint2)
    
    return first_child, second_child  # Devuelve los dos hijos resultantes del cruce

# Repara el cromosoma después del cruce
def repair(chromosome, cutpoint1, cutpoint2):
    slot_no = chromosome.shape[0]  # Número total de slots

    # Recorre cada presentación entre los puntos de corte
    for presentation in range(cutpoint1, cutpoint2):
        slot = np.where(chromosome[:, presentation] == 1)[0][0]  # Encuentra el slot donde está la presentación

        # Si hay más de una presentación programada para un slot
        if np.count_nonzero(chromosome[slot] == 1) > 1:
            chromosome[slot][presentation] = 0  # Desasigna la presentación del slot

            # Asigna la presentación a otro slot aleatorio
            while True:
                random_slot = np.random.randint(slot_no)

                if chromosome[random_slot][presentation] == 0 and np.count_nonzero(chromosome[random_slot] == 1) == 0:
                    chromosome[random_slot][presentation] = 1
                    break

    return chromosome  # Devuelve el cromosoma reparado

# Realiza una mutación por intercambio en el cromosoma después del cruce
def mutation(chromosome):
    presentation_no = chromosome.shape[1]  # Número total de presentaciones
    random_presentation1 = np.random.randint(presentation_no)  # Selecciona una presentación aleatoria
    slot1 = np.where(chromosome[:, random_presentation1] == 1)[0][0]  # Encuentra el slot para la presentación1

    while True:
        random_presentation2 = np.random.randint(presentation_no)  # Selecciona otra presentación aleatoria
        slot2 = np.where(chromosome[:, random_presentation2] == 1)[0][0]  # Encuentra el slot para la presentación2

        # Intercambia las dos presentaciones entre los dos slots si son intercambiables
        if chromosome[slot1][random_presentation2] == 0 and chromosome[slot2][random_presentation1] == 0:
            chromosome[slot1][random_presentation1] = chromosome[slot2][random_presentation2] = 0
            chromosome[slot1][random_presentation2] = chromosome[slot2][random_presentation1] = 1
            break

    return chromosome  # Devuelve el cromosoma mutado

# Algoritmo Genético de Estado Estable - reemplaza 2 cromosomas en la población
def replacement(population, penalty_points, first_child, second_child, first_penalty_point, second_penalty_point):
    # Reemplaza los 2 cromosomas de mayor penalización con los 2 nuevos cromosomas
    population_size = len(population)
    population[population_size - 1], population[population_size - 2] = first_child, second_child
    penalty_points[population_size - 1], penalty_points[population_size - 2] = first_penalty_point, second_penalty_point

    # Ordena la población según los puntos de penalización
    population = population[penalty_points.argsort()]
    penalty_points = penalty_points[penalty_points.argsort()]

    return population, penalty_points  # Devuelve la población y los puntos de penalización ordenados

# Reproduce nuevos cromosomas en la nueva generación
def reproduction(max_generations, population, penalty_points, presentation_presentation,
                 presentation_supervisor, supervisor_preference):
    plot_data = []  # Lista para almacenar los puntos de penalización por iteración

    # Ejecuta el ciclo de generaciones
    for generation in range(max_generations):
        # Selecciona 2 padres
        first_parent, second_parent = selection(population, penalty_points)
        # Realiza el cruce para generar 2 hijos
        first_child, second_child = crossover(first_parent, second_parent)
        # Aplica mutación a los hijos
        first_child = mutation(first_child)
        second_child = mutation(second_child)
        # Calcula los puntos de penalización para los hijos
        first_penalty_point = \
            penalty(first_child, presentation_presentation, presentation_supervisor, supervisor_preference)[0]
        second_penalty_point = \
            penalty(second_child, presentation_presentation, presentation_supervisor, supervisor_preference)[0]
        # Reemplaza los cromosomas de mayor penalización con los hijos nuevos
        population, penalty_points = \
            replacement(population, penalty_points, first_child, second_child,
                        first_penalty_point, second_penalty_point)
        plot_data.append(penalty_points[0])  # Almacena el punto de penalización del mejor cromosoma

        # Imprime el punto de penalización cada 50 iteraciones
        if (generation + 1) % 50 == 0:
            print("[Iteration ", generation + 1, "] Penalty Point: ", penalty_points[0], sep="")

    return population, penalty_points, plot_data  # Devuelve la población, los puntos de penalización y los datos de gráficos