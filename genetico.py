#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

genetico.py
------------

Este modulo incluye el algoritmo genérico para algoritmos genéticos, así como un
algoritmo genético adaptado a problemas de permutaciones, como el problema de las
n-reinas o el agente viajero.

Como tarea se pide desarrollar otro algoritmo genético con el fin de probar otro tipo
de métodos internos, así como ajustar ambos algoritmos para que funcionen de la mejor
manera posible.

Para que funcione, este modulo debe de encontrarse en la misma carpeta que blocales.py
y nreinas.py vistas en clase.

"""

__author__ = 'Cruz Luque Juan Manuel'

import nreinas
import random
import time
from itertools import combinations


"""

Clase genérica para un algoritmo genético.
Contiene el algoritmo genético general y las clases abstractas.

"""

class Genetico:

    """

    Algoritmo genético general.

    @param problema: Un objeto de la clase blocal.problema
    @param n_poblacion: Entero con el tamaño de la población
    @param n_generaciones: Número de generaciones a simular
    @param elitismo: Booleano, para aplicar o no el elitismo

    @return: Un estado del problema

    """

    def busqueda(self, problema, n_poblacion=10, n_generaciones=30, elitismo=True):

        poblacion = [problema.estado_aleatorio() for _ in range(n_poblacion)]

        for _ in range(n_generaciones):

            aptitud = [self.calcula_aptitud(individuo, problema.costo) for individuo in poblacion]

            elite = min(poblacion, key = problema.costo) if elitismo else None

            padres, madres = self.seleccion(poblacion, aptitud)

            poblacion = self.mutacion(self.cruza_listas(padres, madres))

            poblacion = poblacion[:n_poblacion]

            if elitismo:
                poblacion.append(elite)

        e = min(poblacion, key = problema.costo)

        return e

    """

    Calcula la adaptación de un individuo al medio, mientras más adaptado mejor, por default
    es inversamente proporcionl al costo (mayor costo, menor adaptción).

    @param individuo: Un estado el problema
    @param costo: Una función de costo (recibe un estado y devuelve un número)

    @return un número con la adaptación del individuo

    """

    def calcula_aptitud(self, individuo, costo=None):

        """"

        return max(0, len(individuo) - costo(individuo))

        return 1.0 / (1.0 + costo(individuo))

        """

    """

    Seleccion de estados.

    @param poblacion: Una lista de individuos

    @return: Dos listas, una con los padres y otra con las madres.
    estas listas tienen una dimensión int(len(poblacion)/2)

    """

    def seleccion(self, poblacion, aptitud):

        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    """

    Cruza una lista de padres con una lista de madres, cada pareja da dos hijos.

    @param padres: Una lista de individuos
    @param madres: Una lista de individuos

    @return: Una lista de individuos

    """

    def cruza_listas(self, padres, madres):

        hijos = []

        for (padre, madre) in zip(padres, madres):

            hijos.extend(self.cruza(padre, madre))

        return hijos

    """

    Cruza a un padre con una madre y devuelve una lista de hijos, mínimo 2.

    @param padre: Una lista de individuos
    @param madre: Una lista de individuos

    @return: Una lista de hijos

    """

    def cruza(self, padre, madre):

        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")

    """

    Mutación de una población. Devuelve una población mutada.

    @param poblacion: Una lista de individuos

    @return: Una lista de individuos mutados

    """

    def mutacion(self, poblacion):

        raise NotImplementedError("¡Este metodo debe ser implementado por la subclase!")


"""

Clase con un algoritmo genético adaptado a problemas de permutaciones.

"""

class GeneticoPermutaciones1(Genetico):

    """

    @param prob_muta : Probabilidad de mutación de un cromosoma (0.01 por defualt)

    """

    def __init__(self, prob_muta = 0.01):

        self.prob_muta = prob_muta

        self.nombre = 'propuesto por el profesor con prob. de mutación ' + str(prob_muta)

    """

    Selección por torneo.

    @param poblacion: Una lista de individuos
    @param aptitud: Una lista con las aptitudes de los individuos

    @return: Dos listas, una con los padres y otra con las madres.
    estas listas tienen una dimensión int(len(poblacion)/2)

    """

    def seleccion(self, poblacion, aptitud):

        padres = []

        baraja = range(len(poblacion))

        random.shuffle(baraja)

        for (ind1, ind2) in [(baraja[i], baraja[i+1]) for i in range(0, len(poblacion)-1, 2)]:

            ganador = ind1 if aptitud[ind1] > aptitud[ind2] else ind2

            padres.append(poblacion[ganador])

        madres = []

        random.shuffle(baraja)

        for (ind1, ind2) in [(baraja[i], baraja[i+1]) for i in range(0, len(poblacion)-1, 2)]:

            ganador = ind1 if aptitud[ind1] > aptitud[ind2] else ind2

            madres.append(poblacion[ganador])

        return padres, madres

    """

    Cruza a un padre con una madre y devuelve una lista de hijos, mínimo 2.

    @param padre: Una lista de individuos
    @param madre: Una lista de individuos

    @return: Una lista de hijos

    """

    def cruza(self, padre, madre):

        hijo1, hijo2 = list(padre), list(madre)

        corte1 = random.randint(0, len(padre)-1)

        corte2 = random.randint(corte1+1, len(padre))

        for i in range(len(padre)):

            if i < corte1 or i >= corte2:

                hijo1[i], hijo2[i] = hijo2[i], hijo1[i]

                while hijo1[i] in padre[corte1:corte2]:

                    hijo1[i] = madre[padre.index(hijo1[i])]

                while hijo2[i] in madre[corte1:corte2]:

                    hijo2[i] = padre[madre.index(hijo2[i])]

        return [tuple(hijo1), tuple(hijo2)]

    """

    Mutación para individus con permutaciones. Utiliza la variable local self.prob_muta.

    @param poblacion: Una lista de individuos (tuplas)

    @return: Los individuos mutados

    """

    def mutacion(self, poblacion):

        poblacion_mutada = []

        for individuo in poblacion:

            individuo = list(individuo)

            for i in range(len(individuo)):

                if random.random() < self.prob_muta:

                    k = random.randint(0, len(individuo) - 1)

                    individuo[i], individuo[k] = individuo[k], individuo[i]

            poblacion_mutada.append(tuple(individuo))

        return poblacion_mutada


################################################################################################
#  AQUI EMPIEZA LO QUE HAY QUE HACER CON LA TAREA
################################################################################################

"""

Clase con un algoritmo genético adaptado a problemas de permutaciones.

"""

class GeneticoPermutaciones2(Genetico):

    """

    Aqui puedes poner algunos de los parámetros que quieras utilizar en tu clase.

    """

    def __init__(self, prob_muta = 0.01):

        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
        #

        self.prob_muta = prob_muta

        self.nombre = 'propuesto por el alumno con prob. de mutación ' + str(prob_muta)

    """

    Desarrolla un método específico de medición de aptitud.

    """

    ####################################################################
    #                          20 PUNTOS
    ####################################################################
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
    #

    def calcula_aptitud(self, individuo, costo=None):

        #return 1.0 / (1.0 + costo(individuo))
        return costo(individuo)

    """

    Desarrolla un método específico de selección.

    """

    #####################################################################
    #                          20 PUNTOS
    #####################################################################
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ----------------------------------
    #

    """

    Selección por ruleta.

    @param poblacion: Una lista de individuos
    @param aptitud: Una lista con las aptitudes de los individuos

    @return: Dos listas, una con los padres y otra con las madres.
    estas listas tienen una dimensión int(len(poblacion)/2)

    """

    def seleccion(self, poblacion, aptitud):

        # Suma de las aptitudes
        sa = sum(aptitud)

        # Media de la aptitud
        mf = float(sa)/len(aptitud)

        # Se calcula el valor esperado de cada individuo
        vei = []

        for i in aptitud:
            vei.append(float(i)/mf)

        # Suma de los valores esperados
        sve = sum(vei)

        # Tupla con el individuo,aptitud y valor esperado
        ind = zip(poblacion,aptitud,vei)

        #print ind

        padres = []

        suma = 0

        r = random.uniform(0, sve)

        x = 0

        #print 'numero aleatorio = ' + str(r)

        while x < len(aptitud) / 2:

            for i in ind:

                temp = i[2]

                suma += temp

                #print 'suma = ' + str(suma)

                if suma > r  and len(padres) < len(aptitud)/2:

                    #print 'hola'

                    padres.append(i[0])

                    suma = 0

                    r = random.uniform(0, sve)

                    x += 1

                    #print 'numero aleatorio = ' + str(r)

        #print 'PADRES'

        #print padres

        madres = []

        suma = 0

        r = random.uniform(0, sve)

        x = 0

        #print 'numero aleatorio = ' + str(r)

        while x < len(aptitud)/2:

            for i in ind:

                temp = i[2]

                suma += temp

                #print 'suma = ' + str(suma)

                if suma > r  and len(madres) < len(aptitud)/2:

                    #print 'hola'

                    madres.append(i[0])

                    suma = 0

                    r = random.uniform(0, sve)

                    x += 1

                    #print 'numero aleatorio = ' + str(r)

        #print 'MADRES'

        #print madres

        return padres, madres

    """

    Cruza a un padre con una madre y devuelve una lista de hijos, mínimo 2.

    @param padre: Una lista de individuos
    @param madre: Una lista de individuos

    @return: Una lista de hijos

    """

    def cruza(self, padre, madre):

        hijo1, hijo2 = list(padre), list(madre)

        corte1 = random.randint(0, len(padre)-1)

        corte2 = random.randint(corte1+1, len(padre))

        for i in range(len(padre)):

            if i < corte1 or i >= corte2:

                hijo1[i], hijo2[i] = hijo2[i], hijo1[i]

                while hijo1[i] in padre[corte1:corte2]:

                    hijo1[i] = madre[padre.index(hijo1[i])]

                while hijo2[i] in madre[corte1:corte2]:

                    hijo2[i] = padre[madre.index(hijo2[i])]

        return [tuple(hijo1), tuple(hijo2)]

    """

    Desarrolla un método específico de mutación.

    """

    ###################################################################
    #                          20 PUNTOS
    ###################################################################
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO --------------------------------
    #

    """

    Mutación para individus con permutaciones. Utiliza la variable local self.prob_muta. El metodo
    a utilizar es el metodo switch el cual intercambia dos valores a la siguiente posicion.
    ejemplo:
    1 2 3
    1 3 2

    @param poblacion: Una lista de individuos (tuplas)

    @return: Los individuos mutados

    """

    def mutacion(self, poblacion):

        poblacion_mutada = []

        for individuo in poblacion:

            individuo = list(individuo)

            for i in range(len(individuo)):

                if random.random() < self.prob_muta:

                    k = random.randint(0, len(individuo) - 1)

                    #print individuo

                    if (k == len(individuo) - 1):

                        individuo[k], individuo[0] = individuo[0], individuo[k]

                    else:

                        individuo[k], individuo[k+1] = individuo[k+1], individuo[k]

                    #print individuo

            poblacion_mutada.append(tuple(individuo))

        return poblacion_mutada

def prueba_genetico_nreinas(algo_genetico, problema, n_poblacion, n_generaciones):

    tiempo_inicial = time.time()

    solucion = algo_genetico.busqueda(problema, n_poblacion, n_generaciones, elitismo = True)

    tiempo_final = time.time()

    #print "\nUtilizando el algoritmo genético " + algo_genetico.nombre

    #print "Con poblacion de dimensión ", n_poblacion

    #print "Con ", str(n_generaciones), " generaciones"

    #print "Costo de la solución encontrada: ", problema.costo(solucion)

    #print "Tiempo de ejecución en segundos: ", tiempo_final - tiempo_inicial

    return solucion, problema.costo(solucion),tiempo_final - tiempo_inicial


if __name__ == "__main__":

    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # Modifica los valores de la función siguiente (o el parámetro del algo_genetico)
    # buscando que el algoritmo encuentre SIEMPRE una solución óptima, utilizando el menor tiempo
    # posible en promedio. Realiza esto para las 8, 16 y 32 reinas.
    #   -- ¿Cuales son en cada caso los mejores valores (escribelos abajo de esta lines)
    #
    #       * 8 reinas *
    #
    #       - probabilidad de mutacion 0.001 - Poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 0.83
    #       Tiempo promedio = 0.0255250382423
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((5, 2, 0, 6, 4, 7, 1, 3), 0, 0.03673601150512695)
    #
    #       - probabilidad de mutacion 0.01 - poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 0.71
    #       Tiempo promedio = 0.026699860096
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((2, 5, 7, 0, 3, 6, 4, 1), 0, 0.02698683738708496)
    #
    #       - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 0.68
    #       Tiempo promedio = 0.0260408782959
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((4, 0, 7, 3, 1, 6, 2, 5), 0, 0.02791881561279297)
    #
    #       * 16 reinas *
    #
    #       - probabilidad de mutacion 0.001 - Poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 3.51
    #       Tiempo promedio = 0.0780597019196
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((14, 10, 2, 15, 3, 8, 13, 5, 1, 11, 6, 12, 0, 4, 7, 9), 2, 0.07854199409484863)
    #
    #       - probabilidad de mutacion 0.01 - poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 3.61
    #       Tiempo promedio = 0.077344493866
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((4, 12, 3, 5, 14, 11, 6, 10, 0, 2, 15, 8, 1, 7, 9, 13), 2, 0.0832369327545166)
    #
    #       - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 3.29
    #       Tiempo promedio = 0.0794121146202
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((0, 8, 13, 3, 6, 9, 14, 1, 4, 10, 15, 2, 11, 5, 7, 12), 1, 0.07831597328186035)
    #
    #       * 32 reinas *
    #
    #       - probabilidad de mutacion 0.001 - Poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 10.11
    #       Tiempo promedio = 0.282851781845
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((22, 5, 26, 9, 20, 12, 23, 18, 19, 17, 0, 24, 31, 4, 6, 1, 3, 29, 14, 21, 16, 27, 11, 28, 7, 25, 13, 15, 10, 30, 2, 8), 7, 0.28515195846557617)
    #
    #       - probabilidad de mutacion 0.01 - poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 10.11
    #       Tiempo promedio = 0.28307256937
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((15, 20, 29, 27, 30, 21, 2, 18, 1, 24, 16, 3, 8, 25, 9, 14, 0, 31, 28, 5, 7, 19, 13, 4, 23, 22, 26, 17, 11, 6, 12, 10), 7, 0.287092924118042)
    #
    #       - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -
    #
    #       Aptitud promedio = 9.91
    #       Tiempo promedio = 0.283889763355
    #       Caracteristicas del super individuo mostrado abajo = Cromosoma + aptitud + tiempo
    #       Super Individuo = ((9, 13, 22, 20, 11, 28, 6, 10, 12, 30, 3, 0, 14, 24, 2, 25, 7, 1, 31, 15, 16, 4, 8, 5, 21, 19, 29, 17, 18, 27, 23, 26), 6, 0.2855989933013916)
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun tu experiencia
    #
    #       * 8 reinas *
    #
    #       En el caso de las 8 reinas la siguiente configuracion tuvo buena aptitud y promedio a comparacion de las otras
    #       a mi criterio claro entonces para el caso de las 8 reinas opto por esta configuracion.
    #        - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -
    #
    #       * 16 reinas *
    #
    #       En el caso de las 16 reinas la siguiente configuracion tuvo buena aptitud y promedio a comparacion de las otras
    #       a mi criterio claro entonces para el caso de las 8 reinas opto por esta configuracion.
    #        - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -
    #
    #       * 32 reinas *
    #
    #       En el caso de las 32 reinas la siguiente configuracion tuvo buena aptitud y promedio a comparacion de las otras
    #       a mi criterio claro entonces para el caso de las 8 reinas opto por esta configuracion.
    #        - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -
    #
    #       Para realizar estas conclusiones me enfoque principalmente en la aptitud promedio ya que pienso que el tiempo
    #       aqui es insignificante. Me he llevado la sorpresa que la mejor configuracion a mi parecer ha sido la siguiente
    #       - probabilidad de mutacion 0.05 - Poblacion 50 - generaciones 10 -

    #""""

    ma = 0
    mt = 0
    it = 100
    for x in xrange(1,it):
        solucion = prueba_genetico_nreinas(algo_genetico = GeneticoPermutaciones2(0.05),
        problema = nreinas.ProblemaNreinas(32),
        n_poblacion = 50,
        n_generaciones = 100)
        temp1 = float(solucion[1])
        temp2 = float(solucion[2])
        ma += temp1
        mt += temp2

        if x == 1:
            si = solucion
        if solucion[1] < si[1]:
            si = solucion




    print 'Aptitud promedio'
    print ma/it
    print 'Tiempo promedio'
    print mt/it
    print 'Super Individuo'
    print si


    #"""

    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # Modifica los valores de la función siguiente (o los posibles parámetro del algo_genetico)
    # buscando que el algoritmo encuentre SIEMPRE una solución óptima, utilizando el menor tiempo
    # posible en promedio. Realiza esto para las 8, 16 y 32 reinas.
    #   -- ¿Cuales son en cada caso los mejores valores (escribelos abajo de esta lines)
    #
    #
    #   -- ¿Que reglas podrías establecer para asignar valores segun tu experiencia? Escribelo aqui
    #   abajo, utilizando tanto espacio como consideres necesario.
    #
    # Recuerda de quitar los comentarios de las lineas siguientes:

    """"

    solucion = prueba_genetico_nreinas(algo_genetico = GeneticoPermutaciones2(0.05),
                                       problema = nreinas.ProblemaNreinas(8),
                                       n_poblacion = 4,
                                       n_generaciones = 1)

    print solucion

    """
