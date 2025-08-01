import tkinter as tk
from controller import ViajeController
from views import ViajeView, GraphView
from service import KruskalGraphStrategy
from utils import PESO_MAXIMO, ESTADO_INICIAL, _DIRECTIONS

class MexicoTravelApp:
    """Aplicación principal que coordina MVC"""
    
    def __init__(self):
        self.root = tk.Tk()
        self._configurar_ventana()
        
        # Inicialización con las dependencias
        self.graph_strategy = KruskalGraphStrategy()
        self.controller = ViajeController(self.graph_strategy)
        self.view = ViajeView(self.root)
        
        # Corrección 1: Usar el frame correcto para el gráfico
        graph_frame = self.view.obtener_graph_frame()  # Asegúrate que devuelve un Frame válido
    
        self.graph_view = GraphView(graph_frame)
        self._conectar_eventos()
        self._inicializar_vista()
    
    def _configurar_ventana(self):
        """Configuración básica de la ventana principal"""
        self.root.title("Recorrido por México - Algoritmo de Kruskal")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
    
    def _conectar_eventos(self):
        """Conecta los callbacks de la vista con los métodos del controlador"""
        self.view.on_confirmar_seleccion = self._manejar_confirmacion
        self.view.on_siguiente_estado = self._manejar_siguiente_estado
        self.view.on_mostrar_grafo_completo = self._manejar_grafo_completo
    
    def _inicializar_vista(self):
        """Inicializa la vista con los datos iniciales"""
        self._actualizar_vista()
        self._mostrar_mensaje_bienvenida()
    
    def _actualizar_vista(self):
        """Actualiza todos los componentes de la vista"""
        estado_actual = self.controller.obtener_estado_actual()
        
        if estado_actual is not None:
            self.view.actualizar_estado_actual(estado_actual)
            self.view.actualizar_progreso(self.controller.obtener_progreso())
            self.view.actualizar_peso(self.controller.obtener_peso_info())
            self.view.cargar_dulces(self.controller.obtener_dulces_disponibles())
            
            grafos = self.controller.obtener_grafos()
            if grafos and grafos['mst_grafo'] is not None and grafos['pos_estados'] is not None:
                self.graph_view.actualizar_grafo_mst(
                    grafos['mst_grafo'],
                    grafos['pos_estados'],
                    estado_actual.nombre
                )
        else:
            self._mostrar_viaje_completado()
    
    def _mostrar_mensaje_bienvenida(self):
        """Muestra el mensaje de bienvenida inicial"""
        mensajes = [
            "¡Bienvenido al recorrido por México!",
            f"Estado inicial: {ESTADO_INICIAL}",
            f"Peso máximo permitido: {PESO_MAXIMO} kg",
            "\nSelecciona 3 dulces típicos en cada estado.\n"
        ]
        for msg in mensajes:
            self.view.agregar_info_viaje(msg + "\n")
    
    def _manejar_confirmacion(self, indices_seleccionados):
        """Maneja la confirmación de selección de dulces"""
        valido, mensaje = self.controller.validar_seleccion_dulces(indices_seleccionados)
        if not valido:
            self.view.mostrar_mensaje_error("Selección Incorrecta", mensaje)
            return
        
        if self.controller.confirmar_seleccion_dulces(indices_seleccionados):
            estado = self.controller.obtener_estado_actual()
            if estado is not None:  # Verificación importante
                dulces = [self.controller.obtener_dulces_disponibles()[i] for i in indices_seleccionados]
                peso_total = sum(d.peso for d in dulces)
                
                self.view.actualizar_peso(self.controller.obtener_peso_info())
                self.view.agregar_info_viaje(f"✅ {estado.nombre}:\n")
                for dulce in dulces:
                    self.view.agregar_info_viaje(f"  • {dulce}\n")
                self.view.agregar_info_viaje(f"Peso agregado: {peso_total:.1f} kg\n\n")
                
                self.view.habilitar_confirmar(False)
                self.view.habilitar_siguiente(True)
    
    def _manejar_siguiente_estado(self):
        """Maneja el avance al siguiente estado"""
        if self.controller.avanzar_siguiente_estado():
            self._actualizar_vista()
            self.view.habilitar_confirmar(True)
            self.view.habilitar_siguiente(False)
        else:
            self._mostrar_viaje_completado()
    
    def _manejar_grafo_completo(self):
        """Maneja la visualización del grafo completo"""
        grafos = self.controller.obtener_grafos()
        resumen = self.controller.obtener_resumen_final()
        
        if grafos and all(key in grafos for key in ['grafo_completo', 'mst_grafo', 'pos_estados']):
            self.graph_view.mostrar_comparacion_grafos(
                grafos['grafo_completo'],
                grafos['mst_grafo'],
                grafos['pos_estados'],
                resumen['peso_mst'] if resumen else 0.0
            )
    
    def _mostrar_viaje_completado(self):
        """Muestra el resumen final del viaje"""
        resumen = self.controller.obtener_resumen_final()
        
        if resumen:
            self.view.actualizar_progreso("¡Viaje Completado!")
            self.view.habilitar_confirmar(False)
            self.view.habilitar_siguiente(False)
            
            self.view.agregar_info_viaje("="*50 + "\n")
            self.view.agregar_info_viaje("¡VIAJE COMPLETADO!\n")
            self.view.agregar_info_viaje("="*50 + "\n")
            self.view.agregar_info_viaje(f"Estados visitados: {resumen['estados_visitados']}\n")
            self.view.agregar_info_viaje(f"Peso total: {resumen['peso_total']:.1f} kg\n")
            self.view.agregar_info_viaje(f"Total dulces: {resumen['total_dulces']}\n")
            
            self.view.mostrar_mensaje_info(
                "¡Felicidades!",
                f"Recorrido completado:\n"
                f"Estados: {resumen['estados_visitados']}\n"
                f"Peso dulces: {resumen['peso_total']:.1f} kg"
            )
    
    def run(self):
        """Inicia el bucle principal de la aplicación"""
        self.root.mainloop()

def main():
    """Punto de entrada principal"""
    app = MexicoTravelApp()
    app.run()

if __name__ == "__main__":
    main()