import numpy as np
import csv
from datetime import datetime as date
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import os

# Lee los archivos CSV para llenar matrices numpy que representan la asignación de presentaciones, 
# la disponibilidad de supervisores y las preferencias de estos.
def load():
    slot_no = 280   # La cantidad de slots es una combinación de salas y horarios disponibles.
    supervisor_no = 40  # Cantidad de supervisores (moderadores y técnicos)
    presentation_no = 124  # Cantidad de presentaciones
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

    # Si no existe el directorio "output" lo crea
    if not os.path.exists('output'):
        os.makedirs('output')

    # Dibuja el gráfico de penalizaciones por iteraciones
    title = (f"Mejora en la Programación de Presentaciones a través de las iteraciones\n"
             f"[Restricciones duras violadas:] {constraints_count[1]} "
             f"[Restricciones blandas violadas:] {constraints_count[2]}\n"
             f"[Puntos de penalización:] {constraints_count[0]}")
    plt.title(title)
    plt.xlabel("nro. de iteraciones")
    plt.ylabel("puntos de penalización")
    plt.axis([0, len(plot_data), 0, max(plot_data)])
    plt.plot(plot_data, "r--")
    plt.grid(True)
    plt.ioff()
    pic = plt.gcf()
    plt.show()

    # Guarda el gráfico resultado
    graph_name = f"graph {timestamp}"
    pic.savefig("output/" + graph_name)  # Guarda el gráfico como archivo

    # Dibuja el horario
    venue_no = 7  # Número de salas
    time_slot_no = 20  # Número de slots por día
    day_slot_no = venue_no * time_slot_no  # Número total de slots por día
    day_no = 2  # Número de días
    slot_no = day_slot_no * day_no  # Número total de slots
    venues = ["Aula Magna", "Sala de Conferencias", "Aula 31", "Aula 57", "Aula 28", "Aula 29", "Aula 30"]
    days = ["Día 1", "Día 2"]

    # Inicializa la tabla de horarios
    schedule = PrettyTable()
    schedule.field_names = ["Día", "Sala",
                            "0800-0830", "0830-0900",
                            "0900-0930", "0930-1000", "1000-1030",
                            "1030-1100", "1100-1130", "1130-1200",
                            "1200-1230", "1230-1300", "1400-1430",
                            "1430-1500", "1500-1530", "1530-1600",
                            "1600-1630", "1630-1700", "1700-1730",
                            "1730-1800", "1800-1830", "1830-1900"]

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
        venue_preference = "No" if supervisor_preference[supervisor][2] else "Sí"

        print(f"[Moderador #{str(supervisor + 1).zfill(2)}] "
              f"[Prefiere hasta {supervisor_preference[supervisor][0]} presentaciones consecutivas] "
              f"[Presentaciones consecutivas: {supervisor_preference[supervisor][3]}] "
              f"[Preferencia de días: {supervisor_preference[supervisor][1]}] "
              f"[Días: {supervisor_preference[supervisor][4]}] "
              f"[Prefiere cambio de sala: {venue_preference}] "
              f"[Cambios de sala: {supervisor_preference[supervisor][5]}]")

    # Escribe los resultados en un archivo CSV con la marca de tiempo
    filename = f"output/result {timestamp}.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        for slot in range(slot_presentation.shape[0]):
            presentation = np.where(slot_presentation[slot] == 1)[0]

            if len(presentation) == 0:  # Si no hay presentación para el slot
                writer.writerow(["null", ""])
            else:
                presentation = presentation[0] + 1  # Obtiene la presentación
                writer.writerow(["P" + str(presentation), ""])  # Escribe la presentación en el archivo CSV