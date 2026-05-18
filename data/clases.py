class nodo:
    def __init__(self, nodo_numero, tipo_de_terreno, densidad_poblacion):
        self.numero=nodo_numero
        self.tipo=tipo_de_terreno
        self.densidad=densidad_poblacion

class arco:
    def __init__(self, nodo_origen, nodo_destino, facilidad_propacion):
        self.origen=nodo_origen
        self.destino=nodo_destino
        self.propagacion=facilidad_propacion
        self.tiene_cortafuegos=False