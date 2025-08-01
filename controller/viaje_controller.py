from typing import List, Optional, Dict, Tuple, Union
from networkx import Graph
from models import Viaje, EstadoViaje
from models import Estado, Dulce
from repositories import DataRepository
from service import GraphStrategy, KruskalGraphStrategy  # Cambiado de 'service'


class ViajeController:
    """Controlador principal para la lógica del viaje"""
    
    def __init__(self, graph_strategy: Optional[GraphStrategy] = None):
        self.data_repository = DataRepository()
        self.graph_strategy = graph_strategy or KruskalGraphStrategy()  # Valor por defecto
        self.viaje = Viaje()
        self.estados = self.data_repository.obtener_estados()
        self.dulces_disponibles = self.data_repository.obtener_dulces()
        self._inicializar_viaje()
    
    def _inicializar_viaje(self):
        """Inicializa el viaje con la ruta calculada"""
        if not self.graph_strategy:
            raise ValueError("Estrategia de grafo no proporcionada")
        
        _, ruta = self.graph_strategy.calcular_ruta(self.estados)
        self.viaje.ruta_estados = ruta
    
    def obtener_estado_actual(self) -> Optional[Estado]:
        return self.viaje.estado_actual
    
    def obtener_progreso(self) -> str:
        if self.viaje.viaje_completado:
            return "¡Viaje Completado!"
        return f"Progreso: {self.viaje.estado_actual_index + 1}/{len(self.viaje.ruta_estados)}"
    
    def obtener_peso_info(self) -> str:
        return f"Peso actual: {self.viaje.peso_total:.1f} kg / {self.viaje.peso_maximo} kg"
    
    def obtener_dulces_disponibles(self) -> List[Dulce]:
        return self.dulces_disponibles
    
    def validar_seleccion_dulces(self, indices_seleccionados: List[int]) -> Tuple[bool, str]:
        if len(indices_seleccionados) != 3:
            return False, "Debes seleccionar exactamente 3 dulces."
        
        dulces_seleccionados = [self.dulces_disponibles[i] for i in indices_seleccionados]
        
        if not self.viaje.puede_agregar_dulces(dulces_seleccionados):
            peso_seleccion = sum(dulce.peso for dulce in dulces_seleccionados)
            return False, (f"La selección excede el peso máximo.\n"
                        f"Peso actual: {self.viaje.peso_total:.1f} kg\n"
                        f"Peso selección: {peso_seleccion:.1f} kg\n"
                        f"Peso máximo: {self.viaje.peso_maximo} kg")
        
        return True, ""
    
    def confirmar_seleccion_dulces(self, indices_seleccionados: List[int]) -> bool:
        es_valida, mensaje = self.validar_seleccion_dulces(indices_seleccionados)
        if not es_valida:
            return False
        
        estado_actual = self.viaje.estado_actual
        if estado_actual is None:
            raise ValueError("No hay un estado actual para confirmar la selección")
        
        dulces_seleccionados = [self.dulces_disponibles[i] for i in indices_seleccionados]
        estado_viaje = EstadoViaje(estado_actual, dulces_seleccionados)
        self.viaje.estados_visitados[estado_actual.nombre] = estado_viaje
        
        return True
    
    def avanzar_siguiente_estado(self) -> bool:
        if self.viaje.viaje_completado:
            return False
        
        self.viaje.estado_actual_index += 1
        return True
    
    def obtener_resumen_estado(self, nombre_estado: str) -> List[str]:
        if nombre_estado in self.viaje.estados_visitados:
            estado_viaje = self.viaje.estados_visitados[nombre_estado]
            return [str(dulce) for dulce in estado_viaje.dulces_seleccionados]
        return []
    
    def obtener_resumen_final(self) -> Dict[str, float | int]:
        if not self.graph_strategy:
            raise ValueError("Estrategia de grafo no disponible")
        
        return {
            'estados_visitados': len(self.viaje.estados_visitados),
            'peso_total': self.viaje.peso_total,
            'total_dulces': len(self.viaje.estados_visitados) * 3,
            'peso_mst': self.graph_strategy.obtener_peso_total_mst()
        }
    
    def obtener_grafos(self) -> Dict[str, Union[Graph, Dict[str, Tuple[float, float]], None]]:
        if not self.graph_strategy:
            raise ValueError("La estrategia de grafo no tiene los atributos esperados")
        
        return {
            'grafo_completo': getattr(self.graph_strategy, 'grafo_completo', None),
            'mst_grafo': getattr(self.graph_strategy, 'mst_grafo', None),
            'pos_estados': getattr(self.graph_strategy, 'pos_estados', None)
        }