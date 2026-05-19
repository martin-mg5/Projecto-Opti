import random

población_límite=30000

tipos_de_terreno={1: 'Bosque Denso', 
                  2: 'Bosque no Denso',
                  3: 'Baldío',
                  4: 'Zona Urbana',
                  5: 'Área Silveste Protegida'}

infraestructuras={1: 'Carreteras',
                2: 'Tendido Electrico',
                3: 'Centros de Salud',
                4: 'Postas de Salud Rural',
                5: 'Escuelas',
                6: 'Telecomunicaciones'}

def crear_datos(x, y):
    with open('mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        primera_linea=f'nodo_id,nodo_fila,nodo_columna,tipo_de_terreno,población,{string_infraestructura(infraestructuras)}\n'
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

def poblacion_calculo(tipo_de_terreno):
    if tipo_de_terreno=='Bosque Denso':
        return random.randint(0, 1000)
    elif tipo_de_terreno=='Bosque no Denso':
        return random.randint(0, 2000)
    elif tipo_de_terreno=='Baldío':
        return 0
    elif tipo_de_terreno=='Zona Urbana':
        return random.randint(2000, población_límite)
    elif tipo_de_terreno=='Área Silveste Protegida':
        return 0

def string_infraestructura(infraestructuras):
    out=''
    keys=list(infraestructuras.keys())
    i=0
    while i<len(keys):
        aux=infraestructuras[keys[i]]
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
        tendido=int(carreteras*1.1)
        centros_salud=poblacion//30000
        escuelas=max(1, poblacion//4000)
        telecom=max(1, poblacion//5000)
    elif tipo_terreno in ['Bosque Denso', 'Bosque no Denso']:
        carreteras=random.randint(200, 1000)
        if poblacion>=500:
            postas_rurales=1
            escuelas=1 if poblacion>100 else 0
            telecom=1
            tendido=int(carreteras*0.5)
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

crear_datos(20, 21)

