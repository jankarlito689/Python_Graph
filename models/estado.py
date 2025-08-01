from dataclasses import dataclass
from typing import Tuple

@dataclass
class Estado:
    """Modelo que representa un estado de México"""
    nombre: str
    coordenadas: Tuple[float, float]
    
    @property
    def longitud(self) -> float:
        return self.coordenadas[0]
    
    @property
    def latitud(self) -> float:
        return self.coordenadas[1]

@dataclass
class Dulce:
    """Modelo que representa un dulce típico"""
    nombre: str
    peso: float
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.peso} kg)"