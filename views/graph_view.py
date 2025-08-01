import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Optional, Dict, Tuple

class GraphView:
    """Vista para la visualización de grafos"""
    
    
    
    def __init__(self, parent_frame: tk.Frame):
        self.parent_frame = parent_frame
        self.fig = None
        self.canvas = None
        self.setup_canvas()
    
    def setup_canvas(self):
        """Configura el canvas para matplotlib"""
        try:
            # Crear nueva figura si no existe
            if self.fig is None:
                self.fig = Figure(figsize=(8, 6), dpi=100)
            
            # Configurar canvas
            if self.canvas is None:
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                self.canvas.get_tk_widget().destroy()  # Eliminar el canvas viejo
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
        except Exception as e:
            print(f"Error al configurar canvas: {e}")
            self._recreate_canvas()
    
    def _recreate_canvas(self):
        """Recrea el canvas desde cero"""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def actualizar_grafo_mst(
        self, 
        mst_grafo: nx.Graph, 
        pos_estados: Dict[str, Tuple[float, float]], 
        estado_actual: Optional[str] = None
    ):
        """Actualiza la visualización del MST"""
        if not mst_grafo or not pos_estados:
            return
        
        try:
            # Limpiar figura de manera segura
            if self.fig is None:
                self._recreate_canvas()
            else:
                self.fig.clf()  # Usar clf() en lugar de clear() para mayor compatibilidad
            
            # Crear subplot con manejo de errores
            ax = self.fig.add_subplot(111) if self.fig else None
            if ax is None:
                raise ValueError("No se pudo crear el subplot")
            
            # Convertir posiciones a formato numérico seguro
            pos_numerico = {
                nodo: (float(x), float(y)) 
                for nodo, (x, y) in pos_estados.items()
            }
            
            # Dibujar el MST
            nx.draw_networkx(
                mst_grafo, 
                pos=pos_numerico, 
                ax=ax,
                with_labels=True,
                node_color='lightgreen',
                node_size=800,
                font_size=8,
                font_weight='bold'
            )
            
            # Etiquetas de peso
            edge_labels = {
                (u, v): f"{d['weight']:.1f}" 
                for u, v, d in mst_grafo.edges(data=True)
            }
            nx.draw_networkx_edge_labels(
                mst_grafo,
                pos=pos_numerico,
                edge_labels=edge_labels,
                ax=ax,
                font_size=6
            )
            
            # Resaltar estado actual
            if estado_actual and estado_actual in pos_numerico:
                x, y = pos_numerico[estado_actual]
                ax.scatter(
                    [x], [y],
                    c='red',
                    s=1000,
                    alpha=0.7,
                    zorder=3
                )
            
            ax.set_title("Ruta Óptima (Algoritmo de Kruskal)", fontsize=12, fontweight='bold')
            ax.axis('off')
            
            # Actualizar canvas de manera segura
            if self.canvas:
                self.canvas.draw()
            else:
                self._recreate_canvas()
                
        except Exception as e:
            print(f"Error al actualizar grafo MST: {e}")
            self._recreate_canvas()
    
    def mostrar_comparacion_grafos(
        self, 
        grafo_completo: nx.Graph, 
        mst_grafo: nx.Graph, 
        pos_estados: Dict[str, Tuple[float, float]], 
        peso_mst: float
    ):
        """Muestra una ventana con la comparación de grafos"""
        if not grafo_completo or not mst_grafo or not pos_estados:
            return
        
        graph_window = None
        try:
            graph_window = tk.Toplevel()
            graph_window.title("Comparación de Grafos")
            graph_window.geometry("1200x600")
            
            fig = Figure(figsize=(16, 8), dpi=100)
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            pos_numerico = {
                nodo: (float(x), float(y)) 
                for nodo, (x, y) in pos_estados.items()
            }
            
            # Grafo completo
            ax1 = fig.add_subplot(121)
            nx.draw_networkx(
                grafo_completo,
                pos=pos_numerico,
                ax=ax1,
                with_labels=True,
                node_color='lightblue',
                node_size=600,
                font_size=6,
                font_weight='bold'
            )
            
            # MST
            ax2 = fig.add_subplot(122)
            nx.draw_networkx(
                mst_grafo,
                pos=pos_numerico,
                ax=ax2,
                with_labels=True,
                node_color='lightgreen',
                node_size=600,
                font_size=6,
                font_weight='bold'
            )
            
            canvas.draw()
            
        except Exception as e:
            print(f"Error en comparación de grafos: {e}")
            if graph_window and graph_window.winfo_exists():
                try:
                    graph_window.destroy()
                except:
                    pass