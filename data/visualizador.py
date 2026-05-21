import sys
import csv
import itertools
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QToolTip, QComboBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

class MapaLienzo(QWidget):
    """Lienzo elástico que soporta múltiples capas numéricas dinámicas."""
    def __init__(self, matriz, max_c, max_r, colores_terreno, max_valores):
        super().__init__()
        self.matriz = matriz
        self.columnas = max_c
        self.filas = max_r
        self.colores_terreno = colores_terreno
        self.max_valores = max_valores
        
        self.modo = 'Tipo de Terreno'
        self.setMouseTracking(True) 

    def cambiar_modo(self, nuevo_modo):
        self.modo = nuevo_modo
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen) 

        ancho_total = self.width()
        alto_total = self.height()

        for (r, c), datos in self.matriz.items():
            if self.modo == 'Tipo de Terreno':
                color_hex = self.colores_terreno.get(datos['tipo'], '#FFFFFF')
                painter.setBrush(QColor(color_hex))
            else:
                # MODO CAPA NUMÉRICA: Interpolación lineal (Blanco -> Azul Oscuro)
                valor = datos[self.modo]
                max_v = self.max_valores[self.modo]
                
                factor = (valor / max_v) if max_v > 0 else 0.0
                
                # De Blanco (255, 255, 255) a Azul Oscuro (10, 30, 130)
                red = int(255 - factor * (255 - 10))
                green = int(255 - factor * (255 - 30))
                blue = int(255 - factor * (255 - 130))
                
                painter.setBrush(QColor(red, green, blue))
            
            x1 = int((c / self.columnas) * ancho_total)
            y1 = int((r / self.filas) * alto_total)
            x2 = int(((c + 1) / self.columnas) * ancho_total)
            y2 = int(((r + 1) / self.filas) * alto_total)
            
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)

    def mouseMoveEvent(self, event):
        w = self.width() / self.columnas
        h = self.height() / self.filas

        c = int(event.position().x() / w)
        r = int(event.position().y() / h)

        if (r, c) in self.matriz:
            datos = self.matriz[(r, c)]
            # Construcción dinámica del texto del cursor
            texto = (f"Nodo: {datos['id']}\n"
                     f"Fila: {r}, Columna: {c}\n"
                     f"Terreno: {datos['tipo']}\n")
            
            if self.modo != 'Tipo de Terreno':
                # Muestra el dato específico que estás buscando
                texto += f"{self.modo}: {datos[self.modo]}"
            else:
                # Si estás en modo terreno, muestra la población por defecto
                texto += f"Población: {datos['Población']}"
                
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
        
        # Estas deben coincidir exactamente con los nombres de las columnas en tu CSV
        self.capas_analisis = [
            'Población',
            'Metros carreteras',
            'Metros de tendido eléctrico',
            'Centros de Salud',
            'Postas de Salud Rural',
            'Escuelas',
            'Telecomunicaciones'
        ]
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Visualizador Espacial Multicapa')
        self.resize(1100, 700)
        
        layout_principal = QHBoxLayout(self)
        
        matriz_datos = {}
        max_r, max_c = 0, 0
        
        # Diccionario para rastrear el valor máximo de CADA capa numérica
        self.max_valores = {capa: 0.0 for capa in self.capas_analisis}
        
        try:
            with open(self.archivo_csv, 'r', encoding='UTF-8') as file:
                for linea in file:
                    if linea.startswith('Nodo ID'):
                        iterador_csv = itertools.chain([linea], file)
                        lector_csv = csv.DictReader(iterador_csv)
                        
                        for fila in lector_csv:
                            if not fila or 'Nodo ID' not in fila:
                                continue
                                
                            nodo_id = fila['Nodo ID']
                            r = int(fila['Nodo Fila']) 
                            c = int(fila['Nodo Columna']) 
                            tipo = fila['Tipo de Terreno']
                            
                            datos_celda = {'id': nodo_id, 'tipo': tipo}
                            
                            # Extraemos dinámicamente los valores de todas las capas
                            for capa in self.capas_analisis:
                                valor = float(fila[capa])
                                datos_celda[capa] = valor
                                if valor > self.max_valores[capa]:
                                    self.max_valores[capa] = valor
                                    
                            matriz_datos[(r, c)] = datos_celda
                            
                            if r > max_r: max_r = r
                            if c > max_c: max_c = c
                        break 
                else:
                    print(f"Error: No se encontró el encabezado 'Nodo ID' en {self.archivo_csv}")
                    sys.exit(1)
                    
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_csv}")
            sys.exit(1)

        total_filas = max_r + 1
        total_columnas = max_c + 1

        self.lienzo = MapaLienzo(matriz_datos, total_columnas, total_filas, self.colores_terreno, self.max_valores)

        barra_lateral = QWidget()
        barra_lateral.setFixedWidth(230)
        layout_lateral = QVBoxLayout(barra_lateral)
        layout_lateral.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        label_modo = QLabel("<b>Capa de Visualización:</b>")
        self.selector_modo = QComboBox()
        self.selector_modo.addItem('Tipo de Terreno')
        self.selector_modo.addItems(self.capas_analisis)
        self.selector_modo.currentTextChanged.connect(self.on_modo_cambiado)
        
        layout_lateral.addWidget(label_modo)
        layout_lateral.addWidget(self.selector_modo)
        layout_lateral.addSpacing(20)

        self.leyendas_stack = QStackedWidget()
        
        # --- LEYENDA 1: CAPA TERRENO ---
        leyenda_terreno_widget = QWidget()
        layout_l_terreno = QVBoxLayout(leyenda_terreno_widget)
        layout_l_terreno.setContentsMargins(0, 0, 0, 0)
        layout_l_terreno.addWidget(QLabel("<b>Leyenda de Terreno</b>"))
        
        for tipo, color in self.colores_terreno.items():
            item_layout = QHBoxLayout()
            cuadro = QLabel()
            cuadro.setFixedSize(20, 20)
            cuadro.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            texto = QLabel(tipo)
            texto.setWordWrap(True)
            item_layout.addWidget(cuadro)
            item_layout.addWidget(texto)
            item_layout.addStretch()
            layout_l_terreno.addLayout(item_layout)
            
        self.leyendas_stack.addWidget(leyenda_terreno_widget)

        # --- LEYENDA 2: CAPAS NUMÉRICAS (GRADIENTE DINÁMICO) ---
        leyenda_num_widget = QWidget()
        layout_l_num = QVBoxLayout(leyenda_num_widget)
        layout_l_num.setContentsMargins(0, 0, 0, 0)
        
        self.lbl_titulo_gradiente = QLabel("<b>Intensidad</b>")
        self.lbl_titulo_gradiente.setWordWrap(True)
        layout_l_num.addWidget(self.lbl_titulo_gradiente)
        
        barra_gradiente = QLabel()
        barra_gradiente.setFixedHeight(25)
        barra_gradiente.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                              stop:0 #FFFFFF, stop:1 #0A1E82);
            border: 1px solid black;
        """)
        
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(QLabel("0"))
        labels_layout.addStretch()
        
        # Etiqueta que se actualizará con el valor máximo de la capa actual
        self.lbl_max_valor = QLabel("Max") 
        labels_layout.addWidget(self.lbl_max_valor)
        
        layout_l_num.addWidget(barra_gradiente)
        layout_l_num.addLayout(labels_layout)
        
        self.leyendas_stack.addWidget(leyenda_num_widget)
        layout_lateral.addWidget(self.leyendas_stack)

        layout_principal.addWidget(self.lienzo, stretch=1)
        layout_principal.addWidget(barra_lateral)

    def on_modo_cambiado(self, nuevo_modo):
        self.lienzo.cambiar_modo(nuevo_modo)
        
        if nuevo_modo == "Tipo de Terreno":
            self.leyendas_stack.setCurrentIndex(0)
        else:
            self.leyendas_stack.setCurrentIndex(1)
            # Actualizamos los textos de la leyenda para reflejar la métrica seleccionada
            self.lbl_titulo_gradiente.setText(f"<b>Capa:</b> {nuevo_modo}")
            
            # Formateamos el número para que sea fácil de leer (quitando decimales innecesarios)
            max_v = self.max_valores[nuevo_modo]
            if max_v.is_integer():
                self.lbl_max_valor.setText(f"{int(max_v)}")
            else:
                self.lbl_max_valor.setText(f"{max_v:.2f}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VisualizadorTerreno('data/mapa_test.csv')
    ventana.show()
    sys.exit(app.exec())