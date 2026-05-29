class nodo:
    def _init_(self, **kwargs):
        for clave, valor in kwargs.items():
            setattr(self, clave, valor)

class arco:
    def _init_(self, nodo_origen, nodo_destino, facilidad_propacion):
        self.origen=nodo_origen
        self.destino=nodo_destino
        self.propagacion=facilidad_propacion
        self.tiene_cortafuegos=False