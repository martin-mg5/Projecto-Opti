#CODIGO PARA PROYECTO OPTI CALCULO DE LAS DIRECCIONES
def WindDirection(filas,columnas, v, nu, c1= None,c2 = None,c3 = None, zeta = None, theta = None, sigma = None): #codigo hasta ahora de solo las direcciones
    #Primero, normalizar parametros indicados
    zetas_norm = []

    if theta[2] != theta[0]:
        divisor_theta = (theta[2] - theta[0])  
    else:
        divisor_theta = 1.0
    theta_norm = (theta[1] - theta[0]) / divisor_theta

    if sigma[2] != sigma[0]:
        divisor_sigma = (sigma[2] - sigma[0])
    else:
        divisor_sigma = 1.0
     
    sigma_norm = (sigma[1] - sigma[0]) / divisor_sigma

    z_min = float(min(zeta))
    z_max = float(max(zeta))
    if z_max != z_min:
        divisor_z = z_max - z_min 
    else:
        divisor_z = 1

    for i in range(len(zeta)):
        zeta_i = (float(zeta[i]) - z_min)/ divisor_z
        zetas_norm.append(zeta_i)
    
    
    #asumamos cuadrilla f x c
    listadetodasdirecciones = []
    f = int(filas)
    c = int(columnas)

    vectores_direccion = {
        1: [-1, 1], 2: [0, 1], 3: [1, 1],
        4: [-1, 0],            5: [1, 0],
        6: [-1, -1], 7: [0, -1], 8: [1, -1]
    }
    finales = {
        1: -c - 1, 2: -c, 3: -c + 1,
        4: -1,            5: 1,
        6: c - 1,  7: c,  8: c + 1}
    nombres_direcciones = {
        1: "Arriba a la izquierda", 2: "Arriba", 3: "Arriba a la derecha",
        4: "Izquierda",             5: "Derecha",
        6: "Abajo a la izquierda",  7: "Abajo",  8: "Abajo a la derecha"}


    factores = {}
    for id, d in vectores_direccion.items():   #esto lo saque de gemini porque el codigo me habia quedado mal optimizado (funcionaba pero consumia mas)
        producto_punto = (v[0] * d[0]) + (v[1] * d[1]) #id es lo mismo que llave o nombre o como lo quiera definir
        if producto_punto > 0:       # A favor
            factores[id] = 1 + nu        
        elif producto_punto < 0:     # En contra
            factores[id] = 1 - nu
        else:                        # Perpendicular
            factores[id] = 1

    for i in range(f):
        direcciones_de_fila = []
        for j in range(c):
            nodo = j+ i*c
            zeta_i = zetas_norm[nodo]
            direcciones_del_nodo = []

            if i == 0:   #fila inicial
                if j == 0:
                    llaves = [5, 7, 8]
                    
                elif j == c - 1:
                    llaves = [4, 6, 7]
                    
                else:
                    llaves = [4,5,6,7,8]
                    
            elif i == f - 1:
                if j == 0:
                    llaves = [2, 3, 5]                    
                elif j == c - 1:
                    llaves = [1, 2, 4]                    
                else:
                    llaves = [1,2,3,4,5]    

            else:
                if j == 0:
                    llaves = [2,3,5, 7, 8]                    
                elif j == c - 1:
                    llaves = [1,2,4,6, 7]
                else:
                    llaves = [1,2,3,4,5,6,7,8]

            for k in llaves:
                nodo_final = nodo + finales[k]
                zeta_j = zetas_norm[nodo_final] #parametro del nodo final
                phi_ij = factores[k]
                
                #calculo del omega
                w_base = c1 * ((zeta_i + zeta_j) / 2) + (c2 * theta_norm) + (c3 * sigma_norm)
                w_ij = (w_base * phi_ij) / (1 + nu)
                
            
                #eje x, eje y, Nombre, Nodo inicio, Nodo final, Factor phi, Parametro w  #esto es 
                vector = vectores_direccion[k]
                info_dir = [vector[0], vector[1], nombres_direcciones[k], nodo, nodo_final, phi_ij, w_ij]
                
                direcciones_del_nodo.append(info_dir)        
                    
            
            direcciones_de_fila.append(direcciones_del_nodo)
            
        listadetodasdirecciones.append(direcciones_de_fila)
    return listadetodasdirecciones

                    
#COMO DEFINI LAS DIRECCIONES DEL NODO (N):

#                        2    
#                    1       3
#             
#                  4     N     5
#                  
#                    6       8
#                        7

#CONSIDERACIONES: Lo que retorna la funcion de WindDirection (la puse en ingles pa ser mas poser wuaja)
# es una lista que contiene listas (una asociada a cada fila de la cuadrilla/grilla).
# A su vez, esta lista contiene listas asociadas a los nodos y los valores asociados
# a cada uno de sus arcos (informacion que, nuevamente, esta en listas). La parte del export lo hago con el csv
# pero tecnicamente cualquiera podría hacerlo. Las direcciones del nodo las defini de esa manera para que tambien los 
# arcos estuvieran en orden en relacion a los nodos involucrados desde el nodo de origen.
# Los valores a entregar en la función van en el formato de:
# f = Int que representa numero de filas
# c = Int que representa numero de columnas
# v = Vector, en formato de lista de 2 elementos tal que: [1,1] representarí viento arriba derecha 
# nu = valor que representa la influencia del viento (float) 
# c1, c2, c3 = Floats que representan las constantes para ponderar
# zeta = Lista de f x c elementos (asociados a la cantidad de nodos en total). 
# theta = (Debido a que lo definimos como algo en toda la malla, tome como que entregas una lista de 3 elementos, temperatura minima, la real, y la temperatura maxima)
# sigma = (Lo mismo que el caso del theta) ESTO ES POR AHORA NOMAS

#la parte del exportar lo sacas con la funcion de abajo para un csv. Creo que con esto queda claro


#------------------------------------------------------------------------------------------
#ESTO ES UN TEST DE UNA 10 X 10 AHI CADA QUIEN REVISA LO que quiera
teta = [ 25, 27, 30] #temperatura
sigma = [10, 20,30] #magnitud viento 
zeta = []
c1 = 0.3
c2 = 0.4
c3 = 0.3
import random
for i in range(10000):
    zeta.append(random.uniform(0, 5)) #ejemplo
resultados_completo = WindDirection(100,100,[1,0], 0.3, c1, c2,c3, zeta, teta, sigma) #test
print(resultados_completo)
#eje x, eje y, Nombre, Nodo inicio, Nodo final, Factor phi, Parametro w final
#-------------------------------------------------------------------------------------------





import csv


def exportar_direcciones_a_csv(datos_direcciones, archivo="TESTOPTI.csv"):
    with open(archivo, mode='w', newline='', encoding='utf-8-sig') as archivo_csv:
        escritor = csv.writer(archivo_csv, delimiter=';')
        encabezados = ["Nodo inicial", "Nodo final", "Dirección (x, y)", "Nombre de la dirección","Factor direccional", "w_ij"] 
        escritor.writerow(encabezados)
        for fila in datos_direcciones: # Recorre filas
            for nodo in fila:          # Recorre nodos de la fila
                for dir_info in nodo:  # Recorre las direcciones del nodo
                    eje_x = dir_info[0]
                    eje_y = dir_info[1]
                    nombre_dir = dir_info[2]
                    nodo_inicio = dir_info[3]
                    nodo_final = dir_info[4]
                    factor_viento = dir_info[5]
                    w_ij = dir_info[6]

                    factor_excel = str(factor_viento).replace('.', ',')  #para corregir el problema de excel en español que te lo tira como texto
                    w_ij_excel = str(w_ij).replace('.', ',')
                    direccion= f"({eje_x}, {eje_y})"
                    escritor.writerow([nodo_inicio, nodo_final, direccion, nombre_dir, factor_excel, w_ij_excel])  
                    
    print(f"Revisa '{archivo}'.")
#OTRO TEST, AHORA DE COMO SE EXPORTA
#exportar_direcciones_a_csv(resultados_completo, archivo="C:/Users/samui/OneDrive/Escritorio/TESTOPTI.csv") 


#ACAEMPEZAMOS CON EL EJECTUABLEEE
v = [1,1] #Direccion viento noreste
nu = 0.3
c1 = 0.4
c2 = 0.3
c3 = 0.3
zeta = [] #Lo que falta
theta = [20,30,40]
sigma = [1,10,19]
Resultado = WindDirection(10,10,v,nu,c1,c2,c3,zeta,)