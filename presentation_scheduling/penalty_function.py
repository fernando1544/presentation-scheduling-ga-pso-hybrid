import numpy as np
from numba import njit

# Calcula los puntos de penalización basados en restricciones duras y suaves
@njit(cache=True)  # Decora la función para ser compilada en lugar de interpretada, acelerando la ejecución del código de 2 a 3 veces
def penalty(slot_presentation, presentation_presentation, presentation_supervisor, supervisor_preference):
    penalty_point = 0  # Inicializa el punto de penalización total
    hc_count = 0  # Contador de violaciones de restricciones duras
    sc_count = 0  # Contador de violaciones de restricciones suaves
    presentation_no = slot_presentation.shape[1]  # Número total de presentaciones
    supervisor_no = supervisor_preference.shape[0]  # Número total de supervisores
    venue_no = 4  # Número total de lugares
    time_slot_no = 15  # Número total de intervalos de tiempo
    day_slot_no = venue_no * time_slot_no  # Número total de intervalos de tiempo por día
    day_no = 5  # Número total de días
    presentation_presentation = np.copy(presentation_presentation)  # Copia para manipulación segura
    supervisor_preference[:, 3:6].fill(0)  # Inicializa las preferencias de los supervisores (columnas 3 a 5)

    # HC02: ningún personal puede asistir a más de 1 presentación simultáneamente
    for presentation in range(presentation_no):
        # Encuentra el slot de la presentación actual
        slot = np.where(slot_presentation[:, presentation] == 1)[0][0]
        min_concurrent_slot = (slot % time_slot_no) + (slot // day_slot_no) * day_slot_no
        max_concurrent_slot = min_concurrent_slot + day_slot_no

        # Verifica los slots concurrentes
        for concurrent_slot in range(min_concurrent_slot, max_concurrent_slot, time_slot_no):
            concurrent_presentation = np.where(slot_presentation[concurrent_slot] == 1)[0]

            if len(concurrent_presentation) != 0:
                concurrent_presentation = concurrent_presentation[0]

                if presentation_presentation[presentation][concurrent_presentation] == 1:
                    presentation_presentation[presentation][concurrent_presentation] = -1
                    presentation_presentation[concurrent_presentation][presentation] = -1
                    penalty_point += 1000  # Penalización alta por restricción dura
                    hc_count += 1

    # Matriz 5x15 que almacena el lugar para cada presentación
    day_time_slot = np.zeros((day_no, time_slot_no + 1), dtype=np.int8)  # Columna extra para manejar el último intervalo

    # Verifica las preferencias de los supervisores
    for supervisor in range(supervisor_no):  # Bucle más costoso en tiempo
        supervised_presentations = np.where(presentation_supervisor[:, supervisor] == 1)[0]
        day_time_slot.fill(0)

        # Rellena la matriz con las presentaciones supervisadas
        for supervised_presentation in supervised_presentations:
            supervised_slot = np.where(slot_presentation[:, supervised_presentation] == 1)[0][0]
            supervised_day = supervised_slot // day_slot_no
            supervised_time_slot = supervised_slot % time_slot_no
            supervised_venue = (supervised_slot // time_slot_no) % venue_no + 1  # Añade 1 para evitar conflicto con 0
            day_time_slot[supervised_day][supervised_time_slot] = supervised_venue

        consecutive_preference = supervisor_preference[supervisor][0]  # SC01: presentaciones consecutivas
        day_count = 0
        venue_changes = 0

        # Recorre los días y los intervalos de tiempo para evaluar las preferencias
        for day in range(day_no):
            is_consecutive = False
            is_this_day = False
            consecutive_count = 0
            previous_venue = 0

            for time_slot in range(time_slot_no + 1):
                if day_time_slot[day][time_slot] != 0:
                    venue = day_time_slot[day][time_slot]

                    # Verifica si la presentación actual es consecutiva con la anterior
                    if is_consecutive and venue != previous_venue:
                        venue_changes += 1

                    is_consecutive = True
                    is_this_day = True
                    consecutive_count += 1
                    previous_venue = venue
                else:
                    # Calcula la penalización para un grupo de presentaciones consecutivas
                    if is_consecutive:
                        if consecutive_count < consecutive_preference:  # Fomenta presentaciones consecutivas
                            penalty_point += (consecutive_preference - consecutive_count) * 1
                            supervisor_preference[supervisor][3] += 1
                        elif consecutive_count > consecutive_preference:  # Excede la preferencia máxima de consecutivas
                            penalty_point += (consecutive_count - consecutive_preference) * 10
                            supervisor_preference[supervisor][3] += 1
                            sc_count += 1

                    is_consecutive = False

            if is_this_day:  # Se lleva a cabo una presentación en este día
                day_count += 1

        days_preference = supervisor_preference[supervisor][1]  # SC02: número de días
        supervisor_preference[supervisor][4] = day_count

        if day_count > days_preference:
            penalty_point += (day_count - days_preference) * 10
            sc_count += 1

        venue_preference = supervisor_preference[supervisor][2]  # SC03: cambio de lugar
        supervisor_preference[supervisor][5] = venue_changes

        if venue_preference == 1 and venue_changes > 0:  # El supervisor no quiere cambiar de lugar
            penalty_point += venue_changes * 10
            sc_count += 1

    return penalty_point, hc_count, sc_count