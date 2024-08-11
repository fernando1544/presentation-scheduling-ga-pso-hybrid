# presentation-scheduling-ga-pso-hybrid
This repo is intended to solve Presentation Scheduling problem using a hybrid GA and PSO algorithm.

<img src="https://user-images.githubusercontent.com/70183535/190873516-80c3ce3f-310f-48bc-9a89-cd00ac7fbd6b.png" alt="logo-utn" width="300"/>
# Optimización de programación de presentaciones mediante Algoritmos Genéticos y Enjambre de Partículas
Proyecto para el curso "Algoritmos Genéticos y Optimización Heurística" perteneciente a la carrera de posgrado Especialización en Ingeniería en Sistemas de Información en la UTN FRCU.

# Docentes
* Dra. Ing. López de Luise, Daniela.
* Mg. Ing. Pascal, Andrés.
# Equipo
* Gómez Albornoz, Fernando.
* Pereyra Rausch, Fernando Nahuel.
* Thea, Lucía Inés.

# Descripción del Problema
El problema de programación de presentaciones, análogo al famoso Problema de Horarios Universitarios (UCTP), implica asignar un conjunto de presentaciones y recursos, incluidos oradores, supervisores y lugares, a diferentes franjas horarias considerando diversas restricciones. Los supervisores tienen diferentes preferencias, como elegir asistir a un cierto número de presentaciones consecutivas, elegir el número de días para completar todas las presentaciones y decidir si desean cambiar de lugar mientras asisten a presentaciones consecutivas. El problema se define según los siguientes grupos:

* Presentaciones
* Franjas horarias (Horarios y Lugares)
* Supervisores
* Preferencias

Cada presentación es presentada por un orador y supervisada por tres supervisores. Hay k supervisores disponibles. Existen dos tipos de restricciones: restricciones duras y restricciones blandas. Las restricciones duras no se pueden violar para evitar generar un horario inviable, mientras que las restricciones blandas pueden violarse, sin embargo, el número de violaciones debe minimizarse.

# Algoritmos utilizados
## Optimización por enjambre de partículas (PSO)
<img src="https://github.com/user-attachments/assets/13e0195f-a4b3-41f6-a422-4d15cb1e5d19" alt="image" width="300"/>
Es un algoritmo de optimización inspirado en el comportamiento social de los enjambres de animales, como los pájaros o los peces. En este algoritmo, cada solución posible al problema se representa como una partícula que se mueve en un espacio de búsqueda multidimensional. Las partículas se atraen entre sí y hacia las mejores posiciones que han encontrado, buscando así la mejor solución global.

## Algorítmo Genético
Texto

# Datos
En este repositorio, hay n = 118 presentaciones, m = 300 franjas horarias y k = 47 supervisores. Hay 4 sedes: (Nombres). Cada día hay 15 turnos de 30 minutos cada uno. Se programan 300 slots de lunes a viernes.
Tenga en cuenta que cada franja horaria es una combinación de una sede y una franja horaria.

## Restricciones
### Estrictas
HC01: Todas las presentaciones deben programarse y cada presentación sólo puede programarse una vez.
HC02: ningún supervisor puede asistir a dos o más presentaciones simultáneamente
HC03: Algunos lugares no están disponibles en determinadas franjas horarias
HC04: Algunos supervisores no están disponibles en determinadas franjas horarias
HC05: Todas las presentaciones deben programarse para una misma franja horaria sin compartir las sedes
### Blandas
SC01: El número de presentaciones consecutivas no debe exceder la preferencia del supervisor
SC02: El número de días en los que un supervisor necesita asistir a una presentación no debe exceder la preferencia del supervisor
SC03: Algunos supervisores prefieren no cambiar de lugar mientras asisten a presentaciones consecutivas

Traducción realizada con la versión gratuita del traductor DeepL.com

# Archivos de entrada

SupExaAssign.csv especifica los supervisores que están a cargo de las presentaciones.
HC03 especifica las sedes no disponibles
HC04 especifica los supervisores no disponibles en determinadas franjas horarias
SC01 especifica el número preferido de presentaciones consecutivas de los supervisores
SC02 especifica el número de días que prefieren los supervisores para completar todas las presentaciones
SC03 especifica las preferencias de los supervisores en cuanto al cambio de lugar durante las presentaciones consecutivas; "sí" indica que los supervisores prefieren asistir a las presentaciones consecutivas sin cambiar de lugar, mientras que "no" indica que los supervisores no desean cambiar de lugar mientras asisten a las presentaciones consecutivas.

# Implementación en Phyton
## Paquetes
* NumPy: proporciona una potente estructura de matrices n-dimensionales y herramientas de cálculo numérico. Es ideal para crear matrices, y tiene una velocidad de acceso a datos significativamente más rápida y un uso de memoria más eficiente que la lista de Python.
* Numba: es un compilador justo a tiempo (JIT) para Python que puede acelerar la ejecución de código que utilice matrices y funciones NumPy, y bucles frecuentes. Las partes de las funciones definidas por el usuario en Python van precedidas del decorador @njit(cache=True). @njit() compila la función decorada en modo nopython para que el código compilado se ejecute sin la intervención del intérprete de Python. cache=True indica que el resultado de la compilación de la función se guardará en una caché basada en archivos para ahorrar tiempo de compilación al invocar funciones decoradas.
* Matplotlib: es una completa biblioteca para crear visualizaciones interactivas en Python. Una de sus API, pyplot se utiliza para crear gráficos interactivos en una figura. El gráfico interactivo muestra la gráfica de la mejora de los puntos de penalización a lo largo del número de iteraciones en HGASA. El gráfico se puede ampliar, desplazar, configurar y guardar como una figura.
* PrettyTable: puede utilizarse para visualizar datos tabulares en formato de tabla ASCII. Se utiliza para dibujar el calendario del programa de presentación.

## Ejecución 
Comandos Windows para la instalación de paquetes Python:
* NumPy $ pip install numpy
* Numba $ pip install numba
* Matplotlib $ pip install matplotlib
* PrettyTable $ pip install PTable
Debería haber una carpeta llamada input_files en el mismo directorio que contiene todos los archivos csv (SupExaAssign.csv, HC03.csv, HC04.csv, SC01.csv, SC02.csv y SC03.csv).

Ejecuta hybrid_system.py.

🔓 Modifica data.py y input_files para otros formatos de datos, como json o txt.

# Resultados Experimentales
(imagenes)

# Referencias
(libros e inspo)
