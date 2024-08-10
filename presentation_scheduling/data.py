import numpy as np
import csv
from datetime import datetime as date
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Lee los archivos CSV para llenar matrices numpy que representan la asignación de presentaciones, 
# la disponibilidad de supervisores y las preferencias de estos.
def load():
    slot_no = 300   # La cantidad de slots es una combinación de salas y horarios disponibles.
    supervisor_no = 47  # Cantidad de supervisores (moderadores y técnicos)
    presentation_no = 118  # Cantidad de presentaciones
    preference_no = 3  # Número de preferencias para los supervisores
    
    # Inicializa matrices de asignación y preferencias con ceros
    presentation_supervisor = np.zeros([presentation_no, supervisor_no], dtype=np.int8)
    supervisor_slot = np.zeros([supervisor_no, slot_no], dtype=np.int8)
    supervisor_preference = np.zeros([supervisor_no, 2 * preference_no], dtype=np.int8)

    # Lee el archivo que mapea presentaciones con asignación de moderadores y técnicos.
    with open('input_data/ModsAssign.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)  # Salta la cabecera del archivo CSV

        # Recorre las filas del archivo CSV
        for row in csv_reader:
            i = int(row[0][1:]) - 1  # Índice de presentación (P___) en la matriz

            for col in range(1, 4):
                j = int(row[col][2:]) - 1  # Índice de supervisor (S0__) en la matriz
                presentation_supervisor[i][j] = 1  # Marca la asignación

    # Calcula las presentaciones supervisadas por los mismos examinadores
    presentation_presentation = np.dot(presentation_supervisor, presentation_supervisor.transpose())
    # Presentaciones supervisadas por los mismos examinadores se marcan con 1
    presentation_presentation[presentation_presentation >= 1] = 1
    np.fill_diagonal(presentation_presentation, 0)  # Marca la diagonal con 0 para el cálculo de puntos de penalización

    # Lee la Hard Constrait 04: Disponibilidad de moderadores en determinados horarios.
    with open('input_data/HC04.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')

        # Recorre las filas del archivo CSV
        for row in csv_reader:
            i = int(row[0][2:]) - 1  # Índice de supervisor (S0__) en la matriz
            j = [int(_) - 1 for _ in row[1:]]  # Índices de slots no disponibles
            supervisor_slot[i][j] = 1  # Marca los slots no disponibles

    # Calcula los slots disponibles para las presentaciones
    slot_presentation = np.dot(supervisor_slot.transpose(), presentation_supervisor.transpose())
    slot_presentation[slot_presentation >= 1] = -1  # Slots no disponibles para presentaciones se marcan con -1

    # Lee la Hard Constrait 03: Disponibilidad de salas en determinados horarios.
    with open('input_data/HC03.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')

        # Recorre las filas del archivo CSV
        for row in csv_reader:
            i = [int(_) - 1 for _ in row[1:]]  # Índices de slots no disponibles
            slot_presentation[i, :] = -1  # Marca los slots no disponibles

    # Lee la Soft Constrait 01: Número máximo de presentaciones consecutivas que cada moderador debería tener.
    with open('input_data/SC01.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')

        # Recorre las filas del archivo CSV
        for row in csv_reader:
            i = int(row[0][2:]) - 1  # Índice de supervisor (S0__) en la matriz
            supervisor_preference[i][0] = int(row[1])  # Marca el número máximo de presentaciones consecutivas

    # Lee la Soft Constrait 02: Número máximo de días que un moderador debe asistir a presentaciones.
    with open('input_data/SC02.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')

        # Recorre las filas del archivo CSV
        for row in csv_reader:
            i = int(row[0][2:]) - 1  # Índice de supervisor (S0__) en la matriz
            supervisor_preference[i][1] = int(row[1])  # Marca el número máximo de días

    # Lee la Soft Constrait 03: Predisposición de los moderadores de cambiar de sala entre presentaciones.
    with open('input_data/SC03.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')

        # Recorre las filas del archivo CSV
        for row in csv_reader:
            i = int(row[0][2:]) - 1  # Índice de supervisor (S0__) en la matriz
            supervisor_preference[i][2] = 1 if row[1] == "yes" else 0  # Marca la predisposición a cambiar de sala

    return slot_presentation, presentation_presentation, presentation_supervisor, supervisor_preference


# Escribe los resultados en un archivo de salida .csv
def write(slot_presentation, supervisor_preference, constraints_count, plot_data):
    timestamp = date.now().strftime("[%Y-%m-%d %H-%M-%S]")  # Crea una marca de tiempo para el archivo

    # Dibuja el gráfico de penalizaciones por iteraciones
    title = (f"Improvement of Presentation Scheduling over Iterations\n"
             f"[Hard Constraints Violated:] {constraints_count[1]} "
             f"[Soft Constraints Violated:] {constraints_count[2]}\n"
             f"[Final Penalty Points:] {constraints_count[0]}")
    plt.title(title)
    plt.xlabel("Number of Iterations")
    plt.ylabel("Penalty Points")
    plt.axis([0, len(plot_data), 0, max(plot_data)])
    plt.plot(plot_data, "r--")
    plt.grid(True)
    plt.ioff()
    plt.show()
    graph_name = f"graph {timestamp}"
    plt.savefig(graph_name)  # Guarda el gráfico como archivo

    # Dibuja el horario
    venue_no = 4  # Número de salas
    time_slot_no = 15  # Número de slots por día
    day_slot_no = venue_no * time_slot_no  # Número total de slots por día
    day_no = 5  # Número de días
    slot_no = day_slot_no * day_no  # Número total de slots
    venues = ["Aula Magna", "Sala de Conferencias", "Aula 31", "Aula 57"]
    days = ["Lun", "Mar", "Mie", "Jue", "Vie"]

    # Inicializa la tabla de horarios
    schedule = PrettyTable()
    schedule.field_names = ["Dia", "Sala",
                            "0900-0930", "0930-1000", "1000-1030",
                            "1030-1100", "1100-1130", "1130-1200",
                            "1200-1230", "1230-1300", "1400-1430",
                            "1430-1500", "1500-1530", "1530-1600",
                            "1600-1630", "1630-1700", "1700-1730"]

    venue = 0
    day = 0

    # Rellena la tabla de horarios con la programación de presentaciones
    for first_slot in range(0, slot_no, time_slot_no):
        row = []

        if venue == 0:
            row.append(days[day])
        else:
            row.append("")

        row.append(venues[venue])

        for slot in range(first_slot, first_slot + time_slot_no):
            presentation = np.where(slot_presentation[slot] == 1)[0]

            if len(presentation) == 0:
                row.append("")
            else:
                presentation = presentation[0] + 1
                row.append("P" + str(presentation))

        schedule.add_row(row)
        venue += 1

        if venue == venue_no:
            venue = 0
            day += 1
            schedule.add_row([""] * (2 + time_slot_no))

    print("\n", schedule, "\n")  # Imprime la tabla de horarios

    # Imprime los datos relacionados con los supervisores
    supervisor_no = supervisor_preference.shape[0]

    for supervisor in range(supervisor_no):
        venue_preference = "No" if supervisor_preference[supervisor][2] else "Yes"

        print(f"[Supervisor S{str(supervisor + 1).zfill(3)}] "
              f"[No. of Continuous Presentations: {supervisor_preference[supervisor][3]}] "
              f"[Day Preference: {supervisor_preference[supervisor][1]}] "
              f"[Days: {supervisor_preference[supervisor][4]}] "
              f"[Venue Change Preference: {venue_preference}] "
              f"[Venue Changes: {supervisor_preference[supervisor][5]}]")

    # Escribe los resultados en un archivo CSV con la marca de tiempo
    filename = f"result {timestamp}.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        for slot in range(slot_presentation.shape[0]):
            presentation = np.where(slot_presentation[slot] == 1)[0]

            if len(presentation) == 0:  # Si no hay presentación para el slot
                writer.writerow(["null", ""])
            else:
                presentation = presentation[0] + 1  # Obtiene la presentación
                writer.writerow(["P" + str(presentation), ""])  # Escribe la presentación en el archivo CSV