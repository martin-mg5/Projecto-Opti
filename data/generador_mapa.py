import random
#Esto solo por el momento, despues lo hago realista
tipos_de_terreno={'Bosque Denso': 1, 'Bosque no Denso': 2, 'Baldío': 3, 'Area Urbana': 4,'Area Silveste Protegida':5}
foco_inicial=(0, 1)
población_límites=(0, 30000)

def crear_datos(x, y):

    with open('mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        archivo.write('nodo_id, nodo_fila, nodo_columna, tipo_de_terreno, foco_inicial, población\n')

        id_actual=0
        foco_asignado=random.randint(0,(x*y)-1)
        i=0
        while i<y:
            j=0
            while j<x:
                if id_actual==foco_asignado:
                    foco=1
                else:
                    foco=0
                tipo_de_terreno=random.randint(1,5)
                linea_aux=f'{id_actual},{j},{i}, {tipo_de_terreno},{foco},{población_cálculo(tipo_de_terreno)}\n'
                archivo.write(linea_aux)
                id_actual+=1
                j+=1
            i+=1

def población_cálculo(tipo_de_terreno):
    if tipo_de_terreno==1:
        return random.randint(población_límites[0], 30)
    elif tipo_de_terreno==2:
        return random.randint(población_límites[0], 500)
    elif tipo_de_terreno==3:
        return 0
    elif tipo_de_terreno==4:
        return random.randint(población_límites[1]//15, población_límites[1])
    elif tipo_de_terreno==5:
        return 0



