from diccionarios import (tipos_de_terreno, limites_poblacion_terreno, infraestructuras, servicios, tipos_vivienda,
                          periodos, tecnologias, direccion_viento, fallas, ecosistemas)
import random
import math

hectareas_por_nodo=10
kilometros_cuadrados_por_nodo=hectareas_por_nodo*0.01
población_límite=int(1039*kilometros_cuadrados_por_nodo)

def crear_datos(x, y):
    with open('data/mapa_test.csv', 'w', encoding='UTF-8') as archivo:
        primera_linea='Dimension X,Dimension Y,Dirección del Viento\n'
        archivo.write(primera_linea)
        segunda_linea=f'{x},{y},{definir_viento()}\n'
        archivo.write(segunda_linea)
        tercera_linea=f'Nodo ID,Nodo Fila,Nodo Columna,Tipo de Terreno,Población,{string_aux(tipos_vivienda)},{string_aux(infraestructuras)},{string_aux(servicios)},{string_aux(fallas)},{string_aux(ecosistemas)}\n'
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
            while j<x:
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
                ecos=areas_ecosistemas(tipo_terreno)
                viviendas_aux=viviendas(tipo_terreno, poblacion_aux)
                linea_aux=f'{id_actual},{j},{i},{tipo_terreno},{poblacion_aux},{viviendas_aux},{infraestructura},{servicios_aux},{falla},{ecos}\n'
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
        if poblacion>=0:
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
    if tipo_terreno=='Zona Urbana':
        eco_1=0
        eco_2=0
        eco_3=0
        return f'{eco_1},{eco_2},{eco_3}'
    elif tipo_terreno=='Bosque Denso':
        area_usada=hectareas_por_nodo/2
    elif tipo_terreno=='Bosque no Denso':
        area_usada=hectareas_por_nodo/3
    elif tipo_terreno=='Área Silveste Protegida':
        area_usada=hectareas_por_nodo
    else:
        area_usada=0
    r1=random.random()
    r2=random.random()
    r3=random.random()
    suma_r=r1+r2+r3
    eco_1=round((r1/suma_r)*area_usada, 2)
    eco_2=round((r2/suma_r)*area_usada, 2)
    eco_3=round((r3/suma_r)*area_usada, 2)

    return f'{eco_1},{eco_2},{eco_3}'

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

    elif tipo_terreno in ['Área Silveste Protegida', 'Baldío']:
        pass
    return f'{c_uni},{d_5_10},{d_mas_10},{v_soc},{c_grande}'

crear_datos(100, 100)

