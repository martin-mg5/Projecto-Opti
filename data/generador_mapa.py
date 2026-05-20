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

limites_poblacion_terreno={'Bosque Denso': (0, 3), 
                  'Bosque no Denso': (0, 3),
                  'Baldío': (0, 1),
                  'Zona Urbana': (int(125*kilometros_cuadrados_por_nodo), int(1039*kilometros_cuadrados_por_nodo)),
                  'Área Silveste Protegida': (0, 1)}

infraestructuras={1: 'Metros carreteras',
                2: 'Metros de tendido eléctrico',
                3: 'Centros de Salud',
                4: 'Postas de Salud Rural',
                5: 'Escuelas',
                6: 'Telecomunicaciones'}

servicios={1: 'Consumo Agua (L)',
           2: 'Consumo Electricidad(kwH)',
           3: 'Consumo Gas(m3)'}

tipos_vivienda={1: 'Casa Unifamiliar',
                2: 'Departamento 5 a 10 pisos',
                3: 'Departamente más de 10 pisos',
                4: 'Vivienda Social',
                5: 'Casa Grande'}

periodos={1: 'Marzo',
          2: 'Abril',
          3: 'Mayo',
          4: 'Junio',
          5: 'Julio',
          6: 'Agosto',
          7: 'Septiembre',
          8: 'Octubre',
          9: 'Noviembre',
          10: 'Diciembre'}

tecnologias={1: 'Palas y Hachas',
             2: 'Retroexcavadora',
             3: 'Bulldozer',
             4: 'Tractor',
             5: 'Motoniveladora'}


def crear_datos(x, y):
    with open('data/mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        primera_linea='dimension_x, dimension_y'
        archivo.write(primera_linea)
        segunda_linea=f'{x},{y}'
        archivo.write(segunda_linea)
        tercera_linea=f'nodo_id,nodo_fila,nodo_columna,tipo_de_terreno,población,{string_aux(infraestructuras)},{string_aux(servicios)}\n'
        archivo.write(tercera_linea)
        centro_ciudad=(random.randint(0, x-1), random.randint(0, y-1))
        centro_protegido=(random.randint(0, x-1), random.randint(0, y-1))
        while math.dist(centro_ciudad, centro_protegido)<min(x, y)/2:
            centro_protegido=(random.randint(0, x-1), random.randint(0, y-1))
            
        centro_baldio=(centro_ciudad[0]+random.randint(-3, 3),centro_ciudad[1]+random.randint(-3, 3))

        id_actual=0
        i=0
        while i<y:
            j=0
            while j <x:
                dist_ciudad=math.dist((j, i), centro_ciudad)
                dist_protegido=math.dist((j, i), centro_protegido)
                dist_baldio=math.dist((j, i), centro_baldio)

                ruido_ciudad=dist_ciudad+random.uniform(-1.5, 1.5)
                ruido_protegido=dist_protegido+random.uniform(-1.5, 1.5)
                ruido_baldio=dist_baldio+random.uniform(-1.5, 1.5)

                if ruido_ciudad<4.0:
                    tipo_terreno='Zona Urbana'
                elif ruido_protegido<4.5:
                    tipo_terreno='Área Silveste Protegida'
                elif ruido_baldio<3.5:
                    tipo_terreno='Baldío'
                elif ruido_ciudad<7.0:
                    tipo_terreno='Bosque no Denso' if random.random()>0.3 else 'Baldío'
                elif ruido_protegido<8.0:
                    tipo_terreno='Bosque Denso' if random.random()>0.2 else 'Bosque no Denso'
                else:
                    tipo_terreno='Bosque Denso' if random.random()>0.6 else 'Bosque no Denso'

                poblacion_aux=poblacion_calculo(tipo_terreno)
                infraestructura=valores_infraestructura(tipo_terreno, poblacion_aux)
                servicios_aux=valores_servicios(poblacion_aux)
                falla=dias_falla()
                linea_aux=f'{id_actual},{j},{i},{tipo_terreno},{poblacion_aux},{infraestructura},{servicios_aux},{falla}\n'
                archivo.write(linea_aux)
                id_actual+=1
                j+=1
            i+=1

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
        centros_salud=random.randint(0, 1)
        escuelas=random.randint(0, 1)
        telecom=1
    elif tipo_terreno in ['Bosque Denso', 'Bosque no Denso']:
        carreteras=random.randint(200, 1000)
        if poblacion>=0:
            postas_rurales=1
            escuelas=random.randint(0, 1)
            telecom=random.randint(0, 1)
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

def valores_servicios(poblacion):
    agua=random.randint(120, 200)*poblacion
    electricidad=random.randint(10, 30)*poblacion
    gas=random.randint(900, 1000)*poblacion
    valores=[agua, electricidad, gas]
    salida=''
    i=0
    while i<len(valores):
        if i!=len(valores)-1:
            salida=salida+f'{valores[i]},'
        else:
            salida=salida+f'{valores[i]}'
        i+=1
    return salida

def dias_falla():
    valores=[]
    aux=servicios.keys()
    i=0
    while i<len(aux):
        valores.append(random.randint(1,7))
        i+=1
    while i<len(valores):
        if i!=len(valores)-1:
            salida=salida+f'{valores[i]},'
        else:
            salida=salida+f'{valores[i]}'
        i+=1
    return salida

crear_datos(100, 100)

