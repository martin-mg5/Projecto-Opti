hectareas_por_nodo=500
kilometros_cuadrados_por_nodo=hectareas_por_nodo*0.01
población_límite=int(1039*kilometros_cuadrados_por_nodo)

tipos_de_terreno={1: 'Bosque Denso', 
                  2: 'Bosque no Denso',
                  3: 'Baldío',
                  4: 'Zona Urbana',
                  5: 'Área Silveste Protegida'}

limites_poblacion_terreno={'Bosque Denso': (0, 10), 
                  'Bosque no Denso': (0, int(125*kilometros_cuadrados_por_nodo*0.7)),
                  'Baldío': (0, 5),
                  'Zona Urbana': (int(125*kilometros_cuadrados_por_nodo*2), int(1039*kilometros_cuadrados_por_nodo)),
                  'Área Silveste Protegida': (1, 15)}

infraestructuras={1: 'Metros carreteras',
                2: 'Metros de tendido eléctrico',
                3: 'Centros de Salud',
                4: 'Postas de Salud Rural',
                5: 'Escuelas',
                6: 'Telecomunicaciones'}

servicios={1: 'Consumo Agua (m3)',
           2: 'Consumo Electricidad(kwH)',
           3: 'Consumo Gas(m3)'}

consumo_y_costos_servicios={'agua': (0.55, 4017),
                            'electricidad': (11.98, 12892),
                            'gas': (950, 89)}

fallas={1: 'Dias esperados sin agua',
           2: 'Dias esperados sin electricidad',
           3: 'Dias esperados sin gas'}

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
          9: 'Noviembre'}

tecnologias={1: 'Palas y Hachas',
             2: 'Retroexcavadora',
             3: 'Bulldozer',
             4: 'Tractor',
             5: 'Motoniveladora'}

direccion_viento={1: 'Norte',
                  2: 'Noreste',
                  3: 'Este',
                  4: 'Sureste',
                  5: 'Sur',
                  6: 'Suroeste',
                  7: 'Oeste',
                  8: 'Noroeste'}

ecosistemas={1: 'Araucarias',
             2: 'Eucalipto',
             3: 'Roble',
             4: 'Raulí',
             5: 'Pino',
             6: 'Urbano'}

densidad={'Araucarias': 9,
          'Eucalipto': 175,
          'Roble': 133,
          'Raulí': 145 ,
          'Pino': 187,
          'Urbano': 0}