from diccionarios import (tipos_de_terreno, limites_poblacion_terreno, infraestructuras, servicios, tipos_vivienda,
                          periodos, tecnologias, direccion_viento, fallas, ecosistemas, consumo_y_costos_servicios, densidad)
import random
import math

hectareas_por_nodo=500
kilometros_cuadrados_por_nodo=hectareas_por_nodo*0.01
población_límite=int(1039*kilometros_cuadrados_por_nodo)

def crear_datos(x, y):
    with open('data/mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        primera_linea='Dimension X,Dimension Y,Dirección del Viento\n'
        archivo.write(primera_linea)
        segunda_linea=f'{x},{y},{definir_viento()}\n'
        archivo.write(segunda_linea)
        tercera_linea=f'Nodo ID,Nodo Fila,Nodo Columna,Tipo de Terreno,Población,{string_aux(tipos_vivienda)},{string_aux(infraestructuras)},{string_aux(servicios)},{string_aux(fallas)},Ecosistema,Densidad de material Combustible\n'
        archivo.write(tercera_linea)
        centro_ciudad=(random.randint(0, x-1), random.randint(0, y-1))
        centro_protegido=(random.randint(0, x-1), random.randint(0, y-1))
        while math.dist(centro_ciudad, centro_protegido)<min(x, y)/2:
            centro_protegido=(random.randint(0, x-1), random.randint(0, y-1))

        lim_trans_urbana=min(7.0, min(x, y) / 2.0)
        lim_trans_protegida=min(8.0, min(x, y) / 1.8)

        id_actual=0
        i=0
        while i<y:
            j=0
            while j<x:
                dist_ciudad=math.dist((j, i), centro_ciudad)
                dist_protegido=math.dist((j, i), centro_protegido)

                if (j, i)==centro_ciudad:
                    tipo_terreno='Zona Urbana'
                elif (j, i)==centro_protegido:
                    tipo_terreno='Área Silveste Protegida'
                elif dist_ciudad<lim_trans_urbana:
                    tipo_terreno='Bosque no Denso' if random.random()>0.1 else 'Baldío'
                elif dist_protegido<lim_trans_protegida:
                    tipo_terreno='Bosque Denso' if random.random()>0.2 else 'Bosque no Denso'
                else:
                    tipo_terreno='Bosque Denso' if random.random()>0.6 else 'Bosque no Denso'

                poblacion_aux=poblacion_calculo(tipo_terreno)
                infraestructura=valores_infraestructura(tipo_terreno, poblacion_aux)
                servicios_aux=valores_servicios(poblacion_aux)
                falla=dias_falla()
                ecos=areas_ecosistemas(tipo_terreno)
                viviendas_aux=viviendas(tipo_terreno, poblacion_aux)
                linea_aux=f'{id_actual},{i},{j},{tipo_terreno},{poblacion_aux},{viviendas_aux},{infraestructura},{servicios_aux},{falla},{ecos}\n'
                archivo.write(linea_aux)
                id_actual+=1
                j+=1
            i+=1
        i=0

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
        if poblacion>=200:
            postas_rurales=random.randint(0,1)
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


def definir_viento():
    return direccion_viento[random.randint(1, 8)]

def valores_servicios(poblacion):
    agua_pc=consumo_y_costos_servicios['agua'][0]
    agua=round(random.uniform(agua_pc*0.9, agua_pc*1.1), 2)*poblacion*consumo_y_costos_servicios['agua'][1]
    electricidad_pc=consumo_y_costos_servicios['electricidad'][0]
    electricidad=round(random.uniform(electricidad_pc*0.9, electricidad_pc*1.1), 2)*poblacion*consumo_y_costos_servicios['electricidad'][1]
    gas=round(random.uniform(900, 1000), 2)*poblacion*consumo_y_costos_servicios['gas'][1]
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
    salida=''
    i=0
    while i<len(aux):
        valores.append(random.randint(1,7))
        i+=1
    i=0
    while i<len(valores):
        if i!=len(valores)-1:
            salida=salida+f'{valores[i]},'
        else:
            salida=salida+f'{valores[i]}'
        i+=1
    return salida

def areas_ecosistemas(tipo_terreno):
    aux=ecosistemas[random.randint(1, 6)]
    return aux+','+str(densidad[aux])

def viviendas(tipo_terreno, poblacion):
    total_viviendas=poblacion//4

    c_uni=0
    d_5_10=0
    d_mas_10=0
    v_soc=0
    c_grande=0
    if total_viviendas==0:
        return f'{c_uni},{d_5_10},{d_mas_10},{v_soc},{c_grande}'

    if tipo_terreno == 'Zona Urbana':
        total_deptos=int(total_viviendas*0.25)

        d_mas_10=int(total_deptos*0.30)
        d_5_10=total_deptos-d_mas_10
        
        restantes=total_viviendas-total_deptos
        r1=random.random()
        r2=random.random()
        r3=random.random()
        suma=r1+r2+r3
        
        c_uni=int((r1/suma)*restantes)
        v_soc=int((r2/suma)*restantes)
        c_grande=restantes-(c_uni+v_soc)

    elif tipo_terreno == 'Bosque no Denso':
        r1=random.random()
        r2=random.random()
        suma=r1+r2
        c_uni=int((r1/suma)*total_viviendas)
        c_grande=total_viviendas-c_uni

    elif tipo_terreno=='Bosque Denso':
        c_grande=total_viviendas

    elif tipo_terreno=='Baldío':
        c_grande=total_viviendas

    elif tipo_terreno=='Área Silveste Protegida':
        pass
    return f'{c_uni},{d_5_10},{d_mas_10},{v_soc},{c_grande}'

crear_datos(10, 10)

