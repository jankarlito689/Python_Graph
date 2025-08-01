import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Optional
from models import Estado, Dulce
from views import BaseView
from utils import _DIRECTIONS


class ViajeView(BaseView):
    """Vista principal de la aplicación"""
    
    def setup_ui(self):
        self.root.title("Recorrido por México - Algoritmo de Kruskal")
        self.root.geometry("1400x800")
        
        # Callbacks
        self.on_confirmar_seleccion: Optional[Callable] = None
        self.on_siguiente_estado: Optional[Callable] = None
        self.on_mostrar_grafo_completo: Optional[Callable] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=_DIRECTIONS)  # Cambiado aquí
        
        # Configurar el grid para expandirse
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Frame izquierdo para controles
        self.control_frame = ttk.Frame(main_frame)
        self.control_frame.grid(row=0, column=0, sticky=_DIRECTIONS, padx=(0, 10))  # Cambiado aquí
        
        # Frame derecho para el grafo
        self.graph_frame = ttk.LabelFrame(main_frame, text="Visualización del Recorrido", padding="5")
        self.graph_frame.grid(row=0, column=1, sticky=_DIRECTIONS)  # Cambiado aquí
        
        self._setup_control_frame()
        
    def _setup_control_frame(self):
        """Configura el frame de controles"""
        # Título
        title_label = ttk.Label(self.control_frame, text="Recorrido por México", 
                            font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Estado actual
        self.estado_actual_label = ttk.Label(self.control_frame, text="", 
                                            font=('Arial', 12, 'bold'))
        self.estado_actual_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Progreso
        self.progreso_label = ttk.Label(self.control_frame, text="")
        self.progreso_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Peso actual
        self.peso_label = ttk.Label(self.control_frame, text="Peso actual: 0 kg / 20 kg")
        self.peso_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Lista de dulces
        ttk.Label(self.control_frame, text="Selecciona 3 dulces típicos:").grid(row=4, column=0, columnspan=2, pady=10)
        
        self._setup_dulces_section()
        self._setup_buttons()
        self._setup_info_section()
    
    def _setup_dulces_section(self):
        """Configura la sección de dulces"""
        dulces_frame = ttk.Frame(self.control_frame)
        dulces_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
        dulces_frame.rowconfigure(0, weight=1)
        dulces_frame.columnconfigure(0, weight=1)
        
        # Listbox para dulces
        self.dulces_listbox = tk.Listbox(dulces_frame, height=8, selectmode=tk.MULTIPLE, 
                                        font=('Arial', 10), bg='white', 
                                        selectbackground='lightblue')
        self.dulces_listbox.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar para listbox
        scrollbar = ttk.Scrollbar(dulces_frame, orient=tk.VERTICAL, command=self.dulces_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="nsew")
        self.dulces_listbox.config(yscrollcommand=scrollbar.set)
    
    def _setup_buttons(self):
        """Configura los botones"""
        button_frame = ttk.Frame(self.control_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        self.confirmar_btn = ttk.Button(button_frame, text="Confirmar Selección", 
                                    command=self._on_confirmar_clicked)
        self.confirmar_btn.pack(side=tk.LEFT, padx=5)
        
        self.siguiente_btn = ttk.Button(button_frame, text="Siguiente Estado", 
                                    command=self._on_siguiente_clicked, state=tk.DISABLED)
        self.siguiente_btn.pack(side=tk.LEFT, padx=5)
        
        self.mostrar_grafo_btn = ttk.Button(button_frame, text="Ver Grafo Completo", 
                                        command=self._on_mostrar_grafo_clicked)
        self.mostrar_grafo_btn.pack(side=tk.LEFT, padx=5)
    
    def _setup_info_section(self):
        """Configura la sección de información"""
        info_frame = ttk.LabelFrame(self.control_frame, text="Información del Viaje", padding="5")
        info_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky=_DIRECTIONS)
        info_frame.rowconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        
        self.info_text = tk.Text(info_frame, height=6, width=50)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.config(yscrollcommand=info_scrollbar.set)
        self.info_text.grid(row=0, column=0, sticky=_DIRECTIONS)
        info_scrollbar.grid(row=0, column=1, sticky=_DIRECTIONS)
    
    def _on_confirmar_clicked(self):
        """Maneja el clic en confirmar selección"""
        if self.on_confirmar_seleccion:
            seleccionados = list(self.dulces_listbox.curselection())
            self.on_confirmar_seleccion(seleccionados)
    
    def _on_siguiente_clicked(self):
        """Maneja el clic en siguiente estado"""
        if self.on_siguiente_estado:
            self.on_siguiente_estado()
    
    def _on_mostrar_grafo_clicked(self):
        """Maneja el clic en mostrar grafo completo"""
        if self.on_mostrar_grafo_completo:
            self.on_mostrar_grafo_completo()
    
    # Métodos públicos para actualizar la vista
    def actualizar_estado_actual(self, estado: Estado):
        """Actualiza la información del estado actual"""
        self.estado_actual_label.config(text=f"Estado Actual: {estado.nombre}")
    
    def actualizar_progreso(self, progreso: str):
        """Actualiza el progreso del viaje"""
        self.progreso_label.config(text=progreso)
    
    def actualizar_peso(self, peso_info: str):
        """Actualiza la información del peso"""
        self.peso_label.config(text=peso_info)
    
    def cargar_dulces(self, dulces: List[Dulce]):
        """Carga la lista de dulces en el listbox"""
        self.dulces_listbox.delete(0, tk.END)
        for dulce in dulces:
            self.dulces_listbox.insert(tk.END, str(dulce))
        self.dulces_listbox.selection_clear(0, tk.END)
    
    def mostrar_mensaje_error(self, titulo: str, mensaje: str):
        """Muestra un mensaje de error"""
        messagebox.showwarning(titulo, mensaje)
    
    def mostrar_mensaje_info(self, titulo: str, mensaje: str):
        """Muestra un mensaje informativo"""
        messagebox.showinfo(titulo, mensaje)
    
    def agregar_info_viaje(self, texto: str):
        """Agrega texto al área de información del viaje"""
        self.info_text.insert(tk.END, texto)
        self.info_text.see(tk.END)
    
    def habilitar_confirmar(self, habilitado: bool):
        """Habilita/deshabilita el botón confirmar"""
        state = tk.NORMAL if habilitado else tk.DISABLED
        self.confirmar_btn.config(state=state)
    
    def habilitar_siguiente(self, habilitado: bool):
        """Habilita/deshabilita el botón siguiente"""
        state = tk.NORMAL if habilitado else tk.DISABLED
        self.siguiente_btn.config(state=state)
    
    def obtener_graph_frame(self):
        """Retorna el frame para el grafo"""
        return self.graph_frame
