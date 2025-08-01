from dataclasses import dataclass, field
from typing import List, Dict, Optional
from models import Estado, Dulce

@dataclass
class EstadoViaje:
    """Modelo que representa el estado de un viaje"""
    estado: Estado
    dulces_seleccionados: List[Dulce] = field(default_factory=list)
    
    @property
    def peso_dulces(self) -> float:
        return sum(dulce.peso for dulce in self.dulces_seleccionados)

@dataclass
class Viaje:
    """Modelo principal que representa el viaje completo"""
    ruta_estados: List[Estado] = field(default_factory=list)
    estados_visitados: Dict[str, EstadoViaje] = field(default_factory=dict)
    peso_maximo: float = 20.0
    estado_actual_index: int = 0
    
    @property
    def peso_total(self) -> float:
        return sum(estado_viaje.peso_dulces for estado_viaje in self.estados_visitados.values())
    
    @property
    def estado_actual(self) -> Optional[Estado]:
        if self.estado_actual_index < len(self.ruta_estados):
            return self.ruta_estados[self.estado_actual_index]
        return None
    
    @property
    def viaje_completado(self) -> bool:
        return self.estado_actual_index >= len(self.ruta_estados)
    
    def puede_agregar_dulces(self, dulces: List[Dulce]) -> bool:
        peso_dulces = sum(dulce.peso for dulce in dulces)
        return self.peso_total + peso_dulces <= self.peso_maximo