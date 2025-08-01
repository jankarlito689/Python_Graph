import tkinter as tk
from abc import ABC, abstractmethod

class BaseView(ABC):
    """Vista base abstracta"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        pass