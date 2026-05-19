import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class VisualizadorTerreno(QWidget):
    def __init__(self, archivo_csv):
        super().__init__()
        self.archivo_csv = archivo_csv
        
        # Diccionario de colores hexadecimales (ajustados para buena visibilidad)
        # Nota: Se mantiene 'Silveste' tal como se genera en tu código
        self.colores_terreno = {
            'Bosque Denso': '#008000',          # Verde oscuro
            'Bosque no Denso': '#66FF66',       # Verde claro
            'Baldío': '#A0522D',                # Café / Marrón
            'Zona Urbana': '#C0C0C0',           # Gris
            'Área Silveste Protegida': '#33CCFF'# Celeste
        }
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Visualizador de Terreno')
        
        # Layout principal (Horizontal: Grilla a la izquierda, Leyenda a la derecha)
        layout_principal = QHBoxLayout()
        
        # 1. Crear la grilla de nodos
        layout_grilla = QGridLayout()
        layout_grilla.setSpacing(0) # Sin espacio entre celdas para que parezca un mapa continuo
        
        try:
            with open(self.archivo_csv, 'r', encoding='UTF-8') as file:
                lector_csv = csv.DictReader(file)
                for fila in lector_csv:
                    nodo_id = fila['nodo_id']
                    r = int(fila['nodo_fila'])
                    c = int(fila['nodo_columna'])
                    tipo = fila['tipo_de_terreno']
                    
                    # Crear la celda (QLabel)
                    celda = QLabel(nodo_id)
                    celda.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    celda.setFixedSize(40, 40) # Tamaño cuadrado fijo
                    
                    # Aplicar estilos (Color de fondo y borde negro)
                    color_fondo = self.colores_terreno.get(tipo, '#FFFFFF') # Blanco si no encuentra el tipo
                    estilo = f"""
                        background-color: {color_fondo};
                        border: 1px solid black;
                        font-weight: bold;
                    """
                    celda.setStyleSheet(estilo)
                    
                    # Añadir al layout de grilla en la posición correspondiente
                    layout_grilla.addWidget(celda, r, c)
                    
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_csv}")
            sys.exit(1)

        # 2. Crear la leyenda lateral
        layout_leyenda = QVBoxLayout()
        layout_leyenda.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        titulo_leyenda = QLabel("<b>Tipos de Terreno</b>")
        layout_leyenda.addWidget(titulo_leyenda)
        
        for tipo, color in self.colores_terreno.items():
            # Contenedor horizontal para cada ítem de la leyenda
            item_layout = QHBoxLayout()
            
            # Cuadro de color
            cuadro_color = QLabel()
            cuadro_color.setFixedSize(20, 20)
            cuadro_color.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            
            # Etiqueta de texto
            etiqueta_texto = QLabel(tipo)
            
            item_layout.addWidget(cuadro_color)
            item_layout.addWidget(etiqueta_texto)
            item_layout.addStretch() # Empuja el contenido hacia la izquierda
            
            # Añadir al layout vertical de la leyenda
            layout_leyenda.addLayout(item_layout)

        # 3. Ensamblar todo
        # Añadimos la grilla y la leyenda al layout principal
        layout_principal.addLayout(layout_grilla)
        layout_principal.addSpacing(30) # Espacio entre la grilla y la leyenda
        layout_principal.addLayout(layout_leyenda)
        
        self.setLayout(layout_principal)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Instanciar el visualizador apuntando al archivo generado
    ventana = VisualizadorTerreno('mapa_test.csv')
    ventana.show()
    
    sys.exit(app.exec())