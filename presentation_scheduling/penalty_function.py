import numpy as np
from numba import njit

# Calcula la penalty basada en las soft y las hard constraints
@njit(cache=True)  # Decora la funcion para que sea compilada en lugar de interpretada, hace la ejecucion hasta 2-3 veces mas rapida
def penalty(slot_presentation, presentation_presentation, presentation_supervisor, supervisor_preference):
    penalty_point = 0
    hc_count = 0
    sc_count = 0
    presentation_no = slot_presentation.shape[1]
    supervisor_no = supervisor_preference.shape[0]
    venue_no = 4
    time_slot_no = 15
    day_slot_no = venue_no * time_slot_no
    day_no = 5
    presentation_presentation = np.copy(presentation_presentation)
    supervisor_preference[:, 3:6].fill(0)

    # HC02: Nadie del staff puede ir a mas de 1 presentacion a la vez
    for presentation in range(presentation_no):
        slot = np.where(slot_presentation[:, presentation] == 1)[0][0]
        min_concurrent_slot = (slot % time_slot_no) + (slot // day_slot_no) * day_slot_no
        max_concurrent_slot = min_concurrent_slot + day_slot_no

        for concurrent_slot in range(min_concurrent_slot, max_concurrent_slot, time_slot_no):
            concurrent_presentation = np.where(slot_presentation[concurrent_slot] == 1)[0]

            if len(concurrent_presentation) != 0:
                concurrent_presentation = concurrent_presentation[0]

                if presentation_presentation[presentation][concurrent_presentation] == 1:
                    presentation_presentation[presentation][concurrent_presentation] = -1
                    presentation_presentation[concurrent_presentation][presentation] = -1
                    penalty_point += 1000
                    hc_count += 1

    # 5(dias) × 15(slots de tiempo) matriz que guarda los lugares para cada presentacion
    day_time_slot = np.zeros((day_no, time_slot_no + 1), dtype=np.int8)  # extra last column to handle last time slot

    for supervisor in range(supervisor_no):
        supervised_presentations = np.where(presentation_supervisor[:, supervisor] == 1)[0]
        day_time_slot.fill(0)

        for supervised_presentation in supervised_presentations:
            supervised_slot = np.where(slot_presentation[:, supervised_presentation] == 1)[0][0]
            supervised_day = supervised_slot // day_slot_no
            supervised_time_slot = supervised_slot % time_slot_no
            supervised_venue = (supervised_slot // time_slot_no) % venue_no + 1  # add 1 to avoid conflict with 0
            day_time_slot[supervised_day][supervised_time_slot] = supervised_venue

        consecutive_preference = supervisor_preference[supervisor][0]  # SC01: consecutive presentations
        day_count = 0
        venue_changes = 0

        for day in range(day_no):
            is_consecutive = False
            is_this_day = False
            consecutive_count = 0
            previous_venue = 0

            for time_slot in range(time_slot_no + 1):
                if day_time_slot[day][time_slot] != 0:
                    venue = day_time_slot[day][time_slot]

                    # Si la presentacion actual es consecutiva a la anterior
                    # Se ignora este check de presentaciones consecutivas
                    if is_consecutive and venue != previous_venue:
                        venue_changes += 1

                    is_consecutive = True
                    is_this_day = True
                    consecutive_count += 1
                    previous_venue = venue
                else:
                    # Calcula los penalties para un grupo de presentaciones consecutivas
                    if is_consecutive:
                        if consecutive_count < consecutive_preference:  # Incentiva a que haya presentaciones consecutivas
                            penalty_point += (consecutive_preference - consecutive_count) * 1
                            supervisor_preference[supervisor][3] += 1
                        elif consecutive_count > consecutive_preference:  # Preferencia para que exceda maximo consecutivo 
                            penalty_point += (consecutive_count - consecutive_preference) * 10
                            supervisor_preference[supervisor][3] += 1
                            sc_count += 1

                    is_consecutive = False

            if is_this_day:  # Una presentacion toma lugar en ese dia
                day_count += 1

        days_preference = supervisor_preference[supervisor][1]  # SC02: Numero de dias
        supervisor_preference[supervisor][4] = day_count

        if day_count > days_preference:
            penalty_point += (day_count - days_preference) * 10
            sc_count += 1

        venue_preference = supervisor_preference[supervisor][2]  # SC03: Cambio de lugar del evento
        supervisor_preference[supervisor][5] = venue_changes

        if venue_preference == 1 and venue_changes > 0:  # Supervisor no quiere cambiar el lugar del evento
            penalty_point += venue_changes * 10
            sc_count += 1

    return penalty_point, hc_count, sc_count
