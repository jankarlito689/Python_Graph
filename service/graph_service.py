import networkx as nx
from typing import Dict, List, Tuple, Optional
from models.estado import Estado
from abc import ABC, abstractmethod

class GraphStrategy(ABC):
    """Interfaz de grafos"""
    @abstractmethod
    def calcular_ruta(self, estados: Dict[str, Estado]) -> Tuple[nx.Graph, List[Estado]]:
        pass
    
    @abstractmethod
    def obtener_peso_total_mst(self) -> float:
        """Nuevo método abstracto requerido"""
        pass

class KruskalGraphStrategy(GraphStrategy):
    """Implementación concreta usando algoritmo de Kruskal"""
    def __init__(self):
        self.grafo_completo: Optional[nx.Graph] = None
        self.mst_grafo: nx.Graph = nx.Graph()  # Inicializado con grafo vacío
        self.pos_estados: Optional[Dict[str, Tuple[float, float]]] = None
    
    def calcular_distancia(self, estado1: Estado, estado2: Estado) -> float:
        x1, y1 = estado1.coordenadas
        x2, y2 = estado2.coordenadas
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    def construir_grafo_completo(self, estados: Dict[str, Estado]) -> nx.Graph:
        self.grafo_completo = nx.Graph()
        estados_lista = list(estados.values())
        
        for i in range(len(estados_lista)):
            for j in range(i + 1, len(estados_lista)):
                estado1 = estados_lista[i]
                estado2 = estados_lista[j]
                distancia = self.calcular_distancia(estado1, estado2)
                self.grafo_completo.add_edge(estado1.nombre, estado2.nombre, weight=distancia)
        return self.grafo_completo
    
    def calcular_ruta(self, estados: Dict[str, Estado]) -> Tuple[nx.Graph, List[Estado]]:
        if not self.grafo_completo:
            self.construir_grafo_completo(estados)
        
        if self.grafo_completo is None:
            raise ValueError("El grafo completo no se ha construido correctamente")
        
        self.mst_grafo = nx.minimum_spanning_tree(self.grafo_completo, algorithm="kruskal")
        self.pos_estados = {
            estado.nombre: (estado.longitud, estado.latitud) 
            for estado in estados.values()
        }
        
        ruta = self._generar_ruta_dfs(estados, 'Ciudad de México')
        return self.mst_grafo, ruta
    
    def _generar_ruta_dfs(self, estados: Dict[str, Estado], inicio: str) -> List[Estado]:
        visitados = set()
        ruta: List[Estado] = []
        
        if not hasattr(self.mst_grafo, 'neighbors'):
            raise AttributeError("El MST no se ha generado correctamente")
        
        def dfs(nombre_estado: str):
            nonlocal visitados, ruta
            visitados.add(nombre_estado)
            ruta.append(estados[nombre_estado])
            
            if self.mst_grafo is None:
                raise ValueError("El MST no está inicializado")
                
            for vecino in self.mst_grafo.neighbors(nombre_estado):
                if vecino not in visitados:
                    dfs(vecino)
        
        dfs(inicio)
        return ruta
    
    def obtener_peso_total_mst(self) -> float:
        if self.mst_grafo is None:
            return 0.0
        return sum(data['weight'] for _, _, data in self.mst_grafo.edges(data=True))