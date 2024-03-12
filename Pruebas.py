from collections import deque
import subprocess

##colores de impresion"
OK = '\033[92m' #GREEN
WARNING = '\033[93m' #YELLOW
FAIL = '\033[91m' #RED
RESET = '\033[0m' #RESET COLOR
NOTA = '\[\033[0;33m\]' #RESET COLOR
REJILLA = "\[\033[0;34m\]" #BLUE
##-----------------------

#Clase que define las caracteristicas de movimiento, visualizacion y sucerores de un nodo en el puzzle
class Nodo:
    def __init__(self, estado, padre, movimiento, profundidad, piezas_correctas):        
        self.estado = estado                        #configuracion atual de las piezas del puzzle
        self.padre = padre                          #Nodo desde el que se llega a este nodo
        self.movimiento = movimiento                #Movimiento para encontrar este nodo desde el padre
        self.profundidad = profundidad              #Posición del nodo en el árbol de búsqueda
        self.piezas_correctas = piezas_correctas    #Total de piezas en su lugar para este estado

    #Método para el movimiento de las piezas en las direcciones posibles
    def desplazar(self, direccion):
        estado = list(self.estado)
        ind = estado.index(0)

        if direccion == "arriba":            
            if ind not in [6, 7, 8]:                
                temp = estado[ind + 3]
                estado[ind + 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "abajo":            
            if ind not in [0, 1, 2]:                
                temp = estado[ind - 3]
                estado[ind - 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "derecha":            
            if ind not in [0, 3, 6]:                
                temp = estado[ind - 1]
                estado[ind - 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "izquierda":            
            if ind not in [2, 5, 8]:                
                temp = estado[ind + 1]
                estado[ind + 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None        

    #Método que encuentra y regresa todos los nodos sucesores del nodo actual.
    def encontrar_sucesores(self):
        sucesores = []
        sucesorArriba = self.desplazar("arriba")
        sucesorAbajo = self.desplazar("abajo")
        sucesorDerecha = self.desplazar("derecha")
        sucesorIzquierda = self.desplazar("izquierda")
        
        sucesores.append(Nodo(sucesorArriba, self, "arriba", self.profundidad + 1, Manhattan(sucesorArriba)))
        sucesores.append(Nodo(sucesorAbajo, self, "abajo", self.profundidad + 1, Manhattan(sucesorAbajo)))
        sucesores.append(Nodo(sucesorDerecha, self, "derecha", self.profundidad + 1, Manhattan(sucesorDerecha)))
        sucesores.append(Nodo(sucesorIzquierda, self, "izquierda", self.profundidad + 1, Manhattan(sucesorIzquierda)))
        
        sucesores = [nodo for nodo in sucesores if nodo.estado != None] ## va buscando sucesores siempre y cuando existan nodos
        return sucesores

    #Método que encuentra el camino desde el nodo inicial hasta el noto actual
    def encontrar_camino(self, inicial):
        camino = []
        nodo_actual = self
        while nodo_actual.profundidad >= 1:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

    #Método para la impresión del estado de un nodo (ordenadamente)
    def imprimir_nodo(self):
        renglon = 0
        for pieza in self.estado:
            if pieza == 0:
                print("\t","\033[0;34m"+"["+"\033[0m","\033[91m"+str(pieza)+"\033[0m", "\033[0;34m"+"]"+"\033[0m", end = " ")
            else:
                print ("\t","\033[0;34m"+"["+"\033[0m",pieza,"\033[0;34m"+"]"+"\033[0m", end = " ")
            renglon += 1
            if renglon == 3:
                print()
                renglon = 0       

correcto=()

def establecerEstadosDesdeArchivo(nombreArchivo):
    try:
        with open(nombreArchivo, 'r') as archivo:
            contenido = archivo.read().splitlines()

        matrizInicial = []
        matrizFinal = []
        listInicial = []
        listFinal = []

        leyendoConfiguracionFinal = False

        for i, linea in enumerate(contenido):
            if linea.strip() == "-":
                leyendoConfiguracionFinal = True
                continue

            fila = [int(valor) for valor in linea.split()]

            if len(fila) == 3 and all(0 <= valor < 9 for valor in fila):
                if leyendoConfiguracionFinal:
                    matrizFinal.append(fila)
                else:
                    matrizInicial.append(fila)
            else:
                raise ValueError(f"Error en el formato en la línea {i + 1} del archivo. Contenido: {linea}")

        if len(matrizInicial) != 3 or len(matrizInicial[0]) != 3:
            raise ValueError("La matriz inicial no tiene el formato esperado de 3x3.")

        if len(matrizFinal) != 3 or len(matrizFinal[0]) != 3:
            raise ValueError("La matriz final no tiene el formato esperado de 3x3.")

        print("CONFIGURACIÓN INICIAL:")
        imprimirMatriz(matrizInicial)

        print("\nCONFIGURACIÓN FINAL:")
        imprimirMatriz(matrizFinal)

        for i in range(len(matrizInicial)):
            listInicial.extend(matrizInicial[i])
            listFinal.extend(matrizFinal[i])

        return listInicial, listFinal, matrizInicial, matrizFinal

    except FileNotFoundError:
        print("¡Archivo no encontrado!")
    except ValueError as e:
        print(f"Error: {e}")

    return None, None

def Manhattan(estado):
    valor_correcto = 0
    piezas_correctas = 0
    manDict=0
    if estado:
        initial_config=list(estado)
        for i,item in enumerate(initial_config):
            prev_row,prev_col = int(i/ 3) , i % 3
            goal_row,goal_col = int(item /3),item % 3
            manDict += abs(prev_row-goal_row) + abs(prev_col - goal_col)
        for valor_pieza, valor_correcto in zip(estado, correcto):
            if valor_pieza == valor_correcto:
                piezas_correctas += 1
            valor_correcto += 1
            
    return piezas_correctas

def CalcularHeuristica(estado):
    manDict=0
    if estado:
        initial_config=list(estado)
        for i,item in enumerate(initial_config):
            prev_row,prev_col = int(i/ 3) , i % 3
            goal_row,goal_col = int(item /3),item % 3
            manDict += abs(prev_row-goal_row) + abs(prev_col - goal_col)
            
    return manDict

#BPA
def BPA(inicial, meta):
    cerrado = set()    #Conjunto de nodos en estados cerrado
    abierto = []  #Nodos sin explorar
    abierto.append(Nodo(inicial, None, None, 0, Manhattan(inicial)))
    
    while abierto:                                      #Mientras haya nodos por explorar
        nodo = abierto.pop(0)                        #Se toma el primer nodo

        if nodo.estado not in cerrado:                  #Si no se había abierto
            cerrado.add(nodo.estado)                    #se agrega al conjunto de cerrado
            
            if nodo.estado == meta:                         #Si el nodo es la meta
                print("\nMETA ENCONTRADA")            
                return nodo.encontrar_camino(inicial)       #se regresa el camino para llegar a él y termina la ejecución del algoritmo      
            
            for sucesor in nodo.encontrar_sucesores():  #Expandir el nodo
                abierto.append(sucesor)
        
        else:                                           #Si ya se había abierto
            continue                                    #se ignora y continua la ejecución del programa

    print("\nMETA NO ENCONTRADA")
    return None

#BPP
def BPP(inicial, meta, profundidad_max):
    cerrado = set()    #Conjunto de nodos en estados cerrado
    abierto = deque()  #Nodos sin explorar
    abierto.append(Nodo(inicial, None, None, 0, Manhattan(inicial)))
    while abierto:                                      #Mientras haya nodos por explorar
        nodo = abierto.pop()                            #Se toma el primer nodo

        if nodo.estado not in cerrado:                  #Si no se había abierto
            cerrado.add(nodo.estado)                    #se agrega al conjunto de cerrado
        else:                                           #Si ya se había abierto
            continue                                    #se ignora y continua la ejecución del programa
        
        if nodo.estado == meta:                         #Si es una meta, se regresa el camino para llegar a él y termina el algoritmo.
            print("\nMETA ENCONTRADA")            
            return nodo.encontrar_camino(inicial)
        else:                                           #Si no es una meta             
            if profundidad_max > 0:                                         #Si se estableció una profundidad 
                if nodo.profundidad < profundidad_max:                      #y no se ha llegado al lmite de cerrado           
                    abierto.extend(nodo.encontrar_sucesores())              #se agregan sus sucesores al conjunto de nodos sin explorar (Abierto)
            else:                                                           #Si no se estableció una búsqueda con profundidad
                abierto.extend(nodo.encontrar_sucesores())                  #de igual forma se agregan los sucesores a los nodos por explorar.

#Ascenso de Colina
def ascensoColina(inicial):
    cerrado = set()    #Conjunto de estados cerrado
    nodo_actual = Nodo(inicial, None, None, 0, Manhattan(inicial))
    print(Manhattan(inicial))
    while nodo_actual.piezas_correctas < 9:             #Mientras el estado actual no sea la meta
        sucesores = nodo_actual.encontrar_sucesores()   #Se buscan los sucesores del estado actual
        max_piezas_correctas = -1

        #Se busca el sucesores que tenga más piezas posicionadas correctamente
        for nodo in sucesores:   
            if nodo.piezas_correctas >= max_piezas_correctas and nodo not in cerrado:
                max_piezas_correctas = nodo.piezas_correctas
                nodo_siguiente = nodo

            cerrado.add(nodo_actual)

        #Si el nodo encontrado tiene más piezas posicionadas correctamente que el nodo actual
        #pasa a ser el nodo actual para realizar la búsqueda sobre éste
        if nodo_siguiente.piezas_correctas >= nodo_actual.piezas_correctas:
            nodo_actual = nodo_siguiente
        #Si no, significa que se llegó a un máximo local y el algoritmo termina
        else:
            print("\nMáximo local alcanzado. No se encontró la meta.")
            break
    else:
        print("\nMETA ENCONTRADA")        
    return nodo_actual.encontrar_camino(inicial)

#A*
def aAsterisco(inicial, meta):
    cerrado = set()    #Conjunto de estados cerrado
    abierto = deque()  #Nodos sin explorar
    abierto.append(Nodo(inicial, None, None, 0, Manhattan(inicial)))
    
    while abierto:                                      #Mientras haya nodos por explorar
        nodo = abierto.popleft()                        #Se toma el primer nodo

        if nodo.estado not in cerrado:                  #Si no se había abierto 
            cerrado.add(nodo.estado)                    #se agrega al conjunto de cerrado
        else:                                           #Si ya se había abierto
            continue                                    #se ignora y continua la ejecución del programa
        
        if nodo.estado == meta:                         #Si es una meta
            print("\nMETA ENCONTRADA")            
            return nodo.encontrar_camino(inicial)       #se retorna el camino para llegar a él y finaliza la ejecución del algoritmo       
        else:                                           #de lo contrario
            abierto.extend(nodo.encontrar_sucesores())  #se agregan sus sucesores a los nodos por explorar

def imprimirMatriz(matriz):
    for fila in matriz:
        for valor in fila:
            if valor == 0:
                print("\t", "\033[0;33m" + "[" + "\033[0m", "\033[0;34m" + str(valor) + "\033[0m", "\033[0;33m" + "]" + "\033[0m", end=" ")
            else:
                print("\t", "\033[0;33m" + "[" + "\033[0m", valor, "\033[0;33m" + "]" + "\033[0m", end=" ")
        print()
    print()

def establecerEstadoInicial(matrizInicial):
    listInicial=[]
    condicion=0
    print("Ingrese la configuracion inicial del puzzle \n")
    print("\033[0;33m"+"Nota: Para representar el espacio vacio digite el numero 0 \n"+"\033[0m")
    for i in range(3):
        if condicion !=1:
            matrizInicial.append([])
            for j in range(3):
                valor= int(input("FILA {}, COLUMNA {}:".format(i+1,j+1)))
                if valor <9 and valor >=0:
                    matrizInicial[i].append(valor)
                else:
                    print(f"{WARNING}¡Valor Incorrecto!. Ingrese un valor entre 0 y 8 \n {RESET}")
                    condicion=1
                    matrizInicial=[]
                    break
    if condicion !=1:
        print(f"{OK}CONFIGURACION INICIAL: {RESET}")
        k=list(matrizInicial)
        for i in range (len(k)):
            listInicial.extend(k[i])
        imprimirMatriz(matrizInicial)
    else:
        matrizInicial=[]
    return listInicial, matrizInicial

def establecerEstadoFinal(matrizFinal):
    listFinal = []
    condicionF = 0
    print("Ingrese la configuracion final del puzzle")
    print("\033[0;33m" + "Nota: Para representar el espacio vacio digite el numero 0 \n" + "\033[0m")
    for i in range(3):
        if condicionF != 1:
            matrizFinal.append([])
            for j in range(3):
                valor = int(input("FILA {}, COLUMNA {}:".format(i + 1, j + 1)))
                if valor < 9 and valor >= 0:
                    matrizFinal[i].append(valor)
                else:
                    print(f"{WARNING}¡Valor Incorrecto!. Ingrese un valor entre 0 y 8 \n {RESET}")
                    condicionF = 1
                    matrizFinal = []
                    break
    if condicionF != 1:
        print(f"{OK}CONFIGURACION FINAL: {RESET}")
        m = list(matrizFinal)
        for i in range(len(m)):
            listFinal.extend(m[i])
        imprimirMatriz(matrizFinal)
    else:
        matrizFinal = []
    return listFinal, matrizFinal

#genetico
def execute_script(script_name):
    result = subprocess.run(["python", script_name])
    if result.returncode == 0:
        print(f"")
    else:
        print(f"Failed to execute: {script_name}")

#Función main.
if __name__ == "__main__":
    j=0
    matrizInicial =[]
    matrizFinal =[]
    listInicial=[]
    listFinal=[]
    tuplaInicial=()
    tuplaFinal=()
    while j!=1:
        #Menú principal
        print("Seleccione una de las siguientes opciones: \n"
            "1). Obtener configuracíon inicial del archivo de texto\n"
            "2). Imprimir el Estado Inicial del Puzzle\n"
            "3). Imprimir el Estado Final del Puzzle\n"
            "4). BPP - Busqueda de Primero en Profundidad\n"
            "5). BPA - Busqueda de Primero en Amplitud BPA\n"
            "6). Busqueda por Ascenso de Colina\n"
            "7). Busqueda por A*\n"
            "8). Busqueda por Algoritmo genetico\n"
            "9). Salir \n")
        opcion = int(input("Ingrese el numero de la opción que desea ejecutar: "))
        print("Ha seleccionado la opción:",opcion,"\n")

        if opcion==1:
            archivo = "configuracion_inicial.txt"  # Reemplaza con el nombre de tu archivo
            estado_inicial, estado_final, matriz_inicial, matriz_final = establecerEstadosDesdeArchivo(archivo)
            matrizInicial = matriz_inicial
            matrizFinal = matriz_final
            listInicial = estado_inicial
            listFinal = estado_final
            tuplaInicial=tuple(listInicial)
            tuplaFinal=tuple(listFinal)

        elif opcion==2:
            if len(matrizInicial) != 0:
                print(f"{OK}CONFIGURACION INICIAL DEL PUZZLE-8: {RESET}\n")
                imprimirMatriz(matrizInicial)
            else:
                print(f"{FAIL}Ingresar una configuracion inicial \n{RESET}")
        elif opcion==3:
            if len(matrizFinal) != 0:
                print(f"{OK}CONFIGURACION FINAL DEL PUZZLE-8: {RESET}\n")
                imprimirMatriz(matrizFinal)
            else:
                print(f"{FAIL}Ingresar una configuracion final \n{RESET}") 
        elif opcion == 4:
            if len(matrizInicial) != 0:
                if len(matrizFinal) !=0:
                    print("Tupla inicial:",tuplaInicial)
                    print("Tupla final:",tuplaFinal)
                    print("\n¿Establecer un límite de profundidad?\n"
                    "Escriba el límite como un entero mayor que 0\n"
                    "o digite 0 para continuar sin límite.")
                    profundidad_max = int(input("Profundidad: "))
                    print(f"\n{WARNING}Ejecutando Algoritmo BPP.........\n{RESET}")
                    nodos_camino = BPP(tuplaInicial, tuplaFinal, profundidad_max)
                    if nodos_camino:
                        print (f"\n{OK}Cantidad de nodos generados:", len(nodos_camino))
                        print (f"\n{OK}El camino tiene", len(nodos_camino),f"movimientos.\n{RESET}")
                        imprimir_camino = (input ("¿Desea imprimir dicho camino? s/n: "))

                        if imprimir_camino == "s" or imprimir_camino == "S":
                            print("\nEstado inicial:")
                            (Nodo(tuplaInicial, None, None, 0, Manhattan(tuplaInicial))).imprimir_nodo()
                            print ("Piezas posicionadas correctamente:", Manhattan(tuplaInicial), "\n")
                            input("Presione la tecla Enter para continuar")
                            print (f"\n{OK}Distancia de Manhattan:", CalcularHeuristica(tuplaInicial),f"\n{RESET}")
                            for nodo in nodos_camino:
                                print("\nSiguiente movimiento:", nodo.movimiento)
                                print("Estado actual:")
                                nodo.imprimir_nodo()
                                print("Piezas posicionadas correctamente:", nodo.piezas_correctas, "\n")     
                                input("Presione la tecla Enter para continuar")
                    else:
                        print ("\nLas condiciones dadas no permitieron encrontrar la meta")
                else:
                    print(f"{FAIL}Debe ingresar una configuracion final \n{RESET}") 
            else:
                print(f"{FAIL}Debe ingresar una configuracion inicial \n{RESET}") 
        elif opcion == 5:
            if len(matrizInicial) != 0:
                if len(matrizFinal) !=0:
                    print("tuplainicial:\n",tuplaInicial)
                    print("tuplaFinal:\n",tuplaFinal)
                    print(f"\n{WARNING}Ejecutando Algoritmo BPA.......\n",f"{RESET}")
                    nodos_camino = BPA(tuplaInicial, tuplaFinal)
                    if nodos_camino:
                        print (f"\n{OK}Cantidad de nodos generados:", len(nodos_camino))
                        print (f"\n{OK}El camino tiene", len(nodos_camino), f"movimientos.\n{RESET}")
                        imprimir_camino = (input ("¿Desea imprimir dicho camino? s/n: "))

                        if imprimir_camino == "s" or imprimir_camino == "S":
                            print("\nEstado inicial:")
                            (Nodo(tuplaInicial, None, None, 0, Manhattan(tuplaInicial))).imprimir_nodo()
                            print ("Piezas posicionadas correctamente:", Manhattan(tuplaInicial), "\n")
                            input("Presione la tecla Enter para continuar")
                            print (f"\n{OK}Distancia de Manhattan:", CalcularHeuristica(tuplaInicial),f"\n{RESET}")        
                            for nodo in nodos_camino:
                                print("\nSiguiente movimiento:", nodo.movimiento)
                                print("Estado actual:")
                                nodo.imprimir_nodo()
                                print("Piezas posicionadas correctamente:", nodo.piezas_correctas, "\n")     
                                input("Presione la tecla Enter para continuar")
                    else:
                        print (f"\n{WARNING}Las condiciones dadas no permitieron encrontrar la meta\n{RESET}")
                else:
                    print(f"{FAIL}Debe ingresar una configuracion final \n{RESET}") 
            else:
                print(f"{FAIL}Debe ingresar una configuracion inicial \n{RESET}") 
        elif opcion==6:
            if len(matrizInicial) != 0:
                if len(matrizFinal) !=0:
                    print("tuplainicial:\n",tuplaInicial)
                    print("tuplaFinal:\n",tuplaFinal)
                    print(f"\n{WARNING}Ejecutando Algoritmo Ascenso de Colina........\n",f"{RESET}")
                    nodos_camino = ascensoColina(tuplaInicial)
                    if nodos_camino:
                            print (f"\n{OK}Cantidad de nodos generados:", len(nodos_camino))
                            print (f"\n{OK}El camino tiene", len(nodos_camino), f"movimientos.\n{RESET}")
                            imprimir_camino = (input ("¿Desea imprimir dicho camino? s/n: "))

                            if imprimir_camino == "s" or imprimir_camino == "S":
                                print("\nEstado inicial:")
                                (Nodo(tuplaInicial, None, None, 0, Manhattan(tuplaInicial))).imprimir_nodo()
                                print ("Piezas posicionadas correctamente:", Manhattan(tuplaInicial), "\n")
                                input("Presione la tecla Enter para continuar")
                                print (f"\n{OK}Distancia de Manhattan:", CalcularHeuristica(tuplaInicial),f"\n{RESET}")
                                for nodo in nodos_camino:
                                    print("\nSiguiente movimiento:", nodo.movimiento)
                                    print("Estado actual:")
                                    nodo.imprimir_nodo()
                                    print("Piezas posicionadas correctamente:", nodo.piezas_correctas, "\n")     
                                    input("Presione la tecla Enter para continuar")
                    else:
                        print ("\nLas condiciones dadas no permitieron encrontrar la meta")
                else:
                    print(f"{FAIL}Debe ingresar una configuracion final \n{RESET}") 
            else:
                print(f"{FAIL}Debe ingresar una configuracion inicial \n{RESET}") 
        elif opcion==7:
            if len(matrizInicial) != 0:
                if len(matrizFinal) !=0:
                    print("tuplainicial:\n",tuplaInicial)
                    print("tuplaFinal:\n",tuplaFinal)
                    print(f"\n{WARNING}Ejecutando Algoritmo A*.......\n",f"{RESET}")
                    nodos_camino = aAsterisco(tuplaInicial,tuplaFinal)
                    if nodos_camino:
                            print (f"\n{OK}Cantidad de nodos generados:", len(nodos_camino))
                            print (f"\n{OK}El camino tiene", len(nodos_camino), f"movimientos.\n{RESET}")
                            imprimir_camino = (input ("¿Desea imprimir dicho camino? s/n: "))

                            if imprimir_camino == "s" or imprimir_camino == "S":
                                print("\nEstado inicial:")
                                (Nodo(tuplaInicial, None, None, 0, Manhattan(tuplaInicial))).imprimir_nodo()
                                print ("Piezas posicionadas correctamente:", Manhattan(tuplaInicial), "\n")
                                input("Presione la tecla Enter para continuar")
                                print (f"\n{OK}Distancia de Manhattan:", CalcularHeuristica(tuplaInicial),f"\n{RESET}")
                                for nodo in nodos_camino:
                                    print("\nSiguiente movimiento:", nodo.movimiento)
                                    print("Estado actual:")
                                    nodo.imprimir_nodo()
                                    print("Piezas posicionadas correctamente:", nodo.piezas_correctas, "\n")     
                                    input("Presione la tecla Enter para continuar")
                    else:
                        print ("\nLas condiciones dadas no permitieron encrontrar la meta")
                else:
                    print(f"{FAIL}Debe ingresar una configuracion final \n{RESET}") 
            else:
                print(f"{FAIL}Debe ingresar una configuracion inicial \n{RESET}")
        elif opcion==8:
            execute_script("genetic.py")
            
        elif opcion==9:
            print(f"{FAIL}Hasta pronto\n {RESET}")
        
        elif opcion==10:
            if len(matrizInicial)!=0:
                matrizInicial =[]
                listInicial, matrizInicial =establecerEstadoInicial(matrizInicial)
                tuplaInicial=tuple(listInicial)
            else:
                listInicial, matrizInicial =establecerEstadoInicial(matrizInicial)
                tuplaInicial=tuple(listInicial)
        elif opcion==11:
            if len(matrizFinal)!=0:
                matrizFinal=[]
                listFinal, matrizFinal =establecerEstadoFinal(matrizFinal)
                tuplaFinal=tuple(listFinal)
                correcto=tuplaFinal
            else:
                listFinal, matrizFinal =establecerEstadoFinal(matrizFinal)
                tuplaFinal=tuple(listFinal)
                correcto=tuplaFinal
        else:
            print(f"{WARNING}Por favor ingrese una opcion valida\n {RESET}")
