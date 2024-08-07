# presentation-scheduling-ga-pso-hybrid
This repo is intended to solve Presentation Scheduling problem using a hybrid GA and PSO algorithm.

![logo-utn(1)](https://user-images.githubusercontent.com/70183535/190873516-80c3ce3f-310f-48bc-9a89-cd00ac7fbd6b.png)
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
![image](https://github.com/user-attachments/assets/13e0195f-a4b3-41f6-a422-4d15cb1e5d19)
Es un algoritmo de optimización inspirado en el comportamiento social de los enjambres de animales, como los pájaros o los peces. En este algoritmo, cada solución posible al problema se representa como una partícula que se mueve en un espacio de búsqueda multidimensional. Las partículas se atraen entre sí y hacia las mejores posiciones que han encontrado, buscando así la mejor solución global.
