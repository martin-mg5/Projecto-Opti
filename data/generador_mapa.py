import random
import math

hectareas_por_nodo=10
kilometros_cuadrados_por_nodo=hectareas_por_nodo*0.01
población_límite=int(1039*kilometros_cuadrados_por_nodo)

tipos_de_terreno={1: 'Bosque Denso', 
                  2: 'Bosque no Denso',
                  3: 'Baldío',
                  4: 'Zona Urbana',
                  5: 'Área Silveste Protegida'}

limites_poblacion_terreno={'Bosque Denso': (0, int(2*kilometros_cuadrados_por_nodo)), 
                  'Bosque no Denso': (0, int(2*kilometros_cuadrados_por_nodo)),
                  'Baldío': (0, 0),
                  'Zona Urbana': (int(125*kilometros_cuadrados_por_nodo), int(1039*kilometros_cuadrados_por_nodo)),
                  'Área Silveste Protegida': (0, 1)}

infraestructuras={1: 'Carreteras',
                2: 'Tendido Electrico',
                3: 'Centros de Salud',
                4: 'Postas de Salud Rural',
                5: 'Escuelas',
                6: 'Telecomunicaciones'}

servicios={1: 'Agua',
           2: 'Electricidad',
           3: 'Gas'}

tipos_vivienda={1: 'Casa Unifamiliar',
                2: 'Departamento 5 a 10 pisos',
                3: 'Departamente más de 10 pisos',
                4: 'Vivienda Social',
                5: 'Casa Grande'}



def crear_datos(x, y):
    with open('mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        primera_linea=f'nodo_id,nodo_fila,nodo_columna,tipo_de_terreno,población,{string_aux(infraestructuras)}\n'
        archivo.write(primera_linea)

        id_actual=0
        i=0
        while i<y:
            j=0
            while j<x:
                tipo_aux=random.randint(min(tipos_de_terreno.keys()), max(tipos_de_terreno.keys()))
                tipo_terreno=tipos_de_terreno[tipo_aux]
                poblacion_aux=poblacion_calculo(tipo_terreno)
                infraestructura=valores_infraestructura(tipo_terreno, poblacion_aux)
                linea_aux=f'{id_actual},{j},{i},{tipo_terreno},{poblacion_aux},{infraestructura}\n'
                archivo.write(linea_aux)
                id_actual+=1
                j+=1
            i+=1

def crear_datos(x, y):
    with open('mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        primera_linea=f'nodo_id,nodo_fila,nodo_columna,tipo_de_terreno,población,{string_aux(infraestructuras)}\n'
        archivo.write(primera_linea)
        centro_ciudad=(random.randint(0, x-1), random.randint(0, y-1))
        centro_protegido=(random.randint(0, x-1), random.randint(0, y-1))
        while math.dist(centro_ciudad, centro_protegido)<min(x, y)/2:
            centro_protegido=(random.randint(0, x-1), random.randint(0, y-1))
            
        centro_baldio=(centro_ciudad[0]+random.randint(-3, 3),centro_ciudad[1]+random.randint(-3, 3))

        id_actual = 0
        for i in range(y):
            for j in range(x):
                # 2. Calcular la distancia de la celda actual a los centros
                dist_ciudad=math.dist((j, i), centro_ciudad)
                dist_protegido=math.dist((j, i), centro_protegido)
                dist_baldio=math.dist((j, i), centro_baldio)

                ruido_ciudad=dist_ciudad+random.uniform(-1.5, 1.5)
                ruido_protegido=dist_protegido+random.uniform(-1.5, 1.5)
                ruido_baldio=dist_baldio+random.uniform(-1.5, 1.5)

                # 4. Asignación espacial del terreno
                if ruido_ciudad<4.0:
                    tipo_terreno='Zona Urbana'
                elif ruido_protegido<4.5:
                    tipo_terreno='Área Silveste Protegida' # Controla el tamaño del parque (ya no será 1/5 del mapa)
                elif ruido_baldio<3.5:
                    tipo_terreno = 'Baldío'
                elif ruido_ciudad<7.0:
                    # Zona de transición periférica a la ciudad
                    tipo_terreno='Bosque no Denso' if random.random()>0.3 else 'Baldío'
                elif ruido_protegido<8.0:
                    # Zona circundante al parque nacional
                    tipo_terreno='Bosque Denso' if random.random()>0.2 else 'Bosque no Denso'
                else:
                    # Relleno del resto de la geografía
                    tipo_terreno='Bosque Denso' if random.random()>0.6 else 'Bosque no Denso'

                poblacion_aux=poblacion_calculo(tipo_terreno)
                infraestructura=valores_infraestructura(tipo_terreno, poblacion_aux)
                linea_aux=f'{id_actual},{j},{i},{tipo_terreno},{poblacion_aux},{infraestructura}\n'
                archivo.write(linea_aux)
                id_actual+=1

def poblacion_calculo(tipo_de_terreno):
    return random.randint(*limites_poblacion_terreno[tipo_de_terreno])

def string_aux(diccionario):
    out=''
    keys=list(diccionario.keys())
    i=0
    while i<len(keys):
        aux=diccionario[keys[i]]
        if i!=len(keys)-1:
            out=out+f'{aux},'
        else:
            out=out+f'{aux}'
        i+=1
    return out

def valores_infraestructura(tipo_terreno, poblacion):
    carreteras=0
    tendido=0
    centros_salud=0
    postas_rurales=0
    escuelas=0
    telecom=0
    if tipo_terreno=='Zona Urbana':
        carreteras=random.randint(3000, 6000)
        tendido=int(carreteras*2)
        centros_salud=poblacion//30000
        escuelas=max(1, poblacion//4000)
        telecom=max(1, poblacion//5000)
    elif tipo_terreno in ['Bosque Denso', 'Bosque no Denso']:
        carreteras=random.randint(200, 1000)
        if poblacion>=500:
            postas_rurales=1
            escuelas=1 if poblacion>100 else 0
            telecom=1
            tendido=carreteras
    elif tipo_terreno=='Área Silveste Protegida':
        carreteras=random.randint(100, 500)
        telecom=1
        tendido=200
    valores=[carreteras, tendido, centros_salud, postas_rurales, escuelas, telecom]

    salida=''
    i=0
    while i<len(valores):
        if i!=len(valores)-1:
            salida=salida+f'{valores[i]},'
        else:
            salida=salida+f'{valores[i]}'
        i+=1
    return salida

crear_datos(120, 100)

