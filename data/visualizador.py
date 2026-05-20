import sys
import csv
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QToolTip)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

class MapaLienzo(QWidget):
    """Lienzo personalizado para dibujar miles de celdas de forma instantánea sin huecos."""
    def __init__(self, matriz, max_c, max_r, colores):
        super().__init__()
        self.matriz = matriz
        self.columnas = max_c
        self.filas = max_r
        self.colores = colores
        # Activa el seguimiento del mouse para el ToolTip sin necesidad de hacer clic
        self.setMouseTracking(True) 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen) # Quitamos el borde para no oscurecer celdas

        # Obtenemos las dimensiones totales del lienzo
        ancho_total = self.width()
        alto_total = self.height()

        for (r, c), datos in self.matriz.items():
            color_hex = self.colores.get(datos['tipo'], '#FFFFFF')
            painter.setBrush(QColor(color_hex))
            
            # Cálculo de coordenadas absolutas en enteros para eliminar los huecos blancos
            x1 = int((c / self.columnas) * ancho_total)
            y1 = int((r / self.filas) * alto_total)
            x2 = int(((c + 1) / self.columnas) * ancho_total)
            y2 = int(((r + 1) / self.filas) * alto_total)
            
            # Dibujamos el bloque exacto
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)

    def mouseMoveEvent(self, event):
        # Calculamos en qué celda está el cursor matemáticamente
        w = self.width() / self.columnas
        h = self.height() / self.filas

        c = int(event.position().x() / w)
        r = int(event.position().y() / h)

        if (r, c) in self.matriz:
            datos = self.matriz[(r, c)]
            texto = f"Nodo: {datos['id']}\nFila: {r}, Columna: {c}\nTerreno: {datos['tipo']}"
            QToolTip.showText(event.globalPosition().toPoint(), texto, self)
        else:
            QToolTip.hideText()


class VisualizadorTerreno(QWidget):
    def __init__(self, archivo_csv):
        super().__init__()
        self.archivo_csv = archivo_csv
        
        self.colores_terreno = {
            'Bosque Denso': '#008000',
            'Bosque no Denso': '#66FF66',
            'Baldío': '#A0522D',
            'Zona Urbana': '#C0C0C0',
            'Área Silveste Protegida': '#33CCFF'
        }
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Visualizador de Terreno Masivo y Optimizado')
        self.resize(1000, 700)
        
        layout_principal = QHBoxLayout(self)
        
        # 1. Leer los datos y almacenarlos en memoria
        matriz_datos = {}
        max_r, max_c = 0, 0
        
        try:
            with open(self.archivo_csv, 'r', encoding='UTF-8') as file:
                lector_csv = csv.DictReader(file)
                for fila in lector_csv:
                    nodo_id = fila['nodo_id']
                    r = int(fila['nodo_fila']) 
                    c = int(fila['nodo_columna']) 
                    tipo = fila['tipo_de_terreno']
                    
                    matriz_datos[(r, c)] = {'id': nodo_id, 'tipo': tipo}
                    
                    if r > max_r: max_r = r
                    if c > max_c: max_c = c
                    
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_csv}")
            sys.exit(1)

        # El total de columnas y filas es el máximo índice + 1
        total_filas = max_r + 1
        total_columnas = max_c + 1

        # 2. Instanciar nuestro lienzo de alto rendimiento
        lienzo = MapaLienzo(matriz_datos, total_columnas, total_filas, self.colores_terreno)

        # 3. Crear la leyenda lateral (con ancho fijo)
        leyenda_widget = QWidget()
        leyenda_widget.setFixedWidth(200) 
        layout_leyenda = QVBoxLayout(leyenda_widget)
        layout_leyenda.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        titulo_leyenda = QLabel("<b>Tipos de Terreno</b>")
        layout_leyenda.addWidget(titulo_leyenda)
        
        for tipo, color in self.colores_terreno.items():
            item_layout = QHBoxLayout()
            
            cuadro_color = QLabel()
            cuadro_color.setFixedSize(20, 20)
            cuadro_color.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            
            etiqueta_texto = QLabel(tipo)
            etiqueta_texto.setWordWrap(True) 
            
            item_layout.addWidget(cuadro_color)
            item_layout.addWidget(etiqueta_texto)
            item_layout.addStretch()
            
            layout_leyenda.addLayout(item_layout)

        # 4. Ensamblar la ventana
        layout_principal.addWidget(lienzo, stretch=1)
        layout_principal.addWidget(leyenda_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VisualizadorTerreno('mapa_test.csv')
    ventana.show()
    sys.exit(app.exec())