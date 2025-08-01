from typing import Dict, List
from models import Estado, Dulce

class DataRepository:
    """Repositorio para gestionar los datos del juego"""
    
    @staticmethod
    def obtener_estados() -> Dict[str, Estado]:
        estados_data = {
            'Aguascalientes': (102.3, 21.9),
            'Baja California': (115.0, 30.4),
            'Baja California Sur': (111.7, 25.4),
            'Campeche': (90.5, 19.8),
            'Chiapas': (92.6, 16.7),
            'Chihuahua': (106.1, 28.6),
            'Coahuila': (101.9, 27.3),
            'Colima': (103.7, 19.2),
            'Durango': (104.6, 24.0),
            'Guanajuato': (101.0, 21.0),
            'Guerrero': (99.8, 17.4),
            'Hidalgo': (98.9, 20.5),
            'Jalisco': (103.3, 20.7),
            'México': (99.1, 19.3),
            'Michoacán': (101.7, 19.4),
            'Morelos': (99.0, 18.7),
            'Nayarit': (104.9, 21.8),
            'Nuevo León': (100.3, 25.7),
            'Oaxaca': (96.7, 17.1),
            'Puebla': (98.2, 19.0),
            'Querétaro': (100.4, 20.6),
            'Quintana Roo': (87.6, 19.6),
            'San Luis Potosí': (100.9, 22.1),
            'Sinaloa': (107.4, 25.0),
            'Sonora': (110.9, 29.1),
            'Tabasco': (92.6, 18.0),
            'Tamaulipas': (98.7, 24.3),
            'Tlaxcala': (98.2, 19.3),
            'Veracruz': (96.1, 19.2),
            'Yucatán': (89.0, 20.7),
            'Zacatecas': (102.6, 23.3),
            'Ciudad de México': (99.1, 19.4)
        }
        return {
            nombre: Estado(nombre, coordenadas) 
            for nombre, coordenadas in estados_data.items()
        }
    
    @staticmethod
    def obtener_dulces() -> List[Dulce]:
        dulces_data = {
            'Ate de membrillo': 0.5,
            'Cajeta': 0.3,
            'Chongos zamoranos': 0.4,
            'Dulce de leche': 0.3,
            'Alegrías': 0.2,
            'Cocadas': 0.25,
            'Obleas': 0.1,
            'Muéganos': 0.35,
            'Palanquetas': 0.3,
            'Jamoncillo': 0.4,
            'Borrachitos': 0.15,
            'Glorias': 0.25,
            'Merengues': 0.1,
            'Alfeñiques': 0.05,
            'Dulce de camote': 0.4,
            'Mangoneadas': 0.3,
            'Pepitorias': 0.2,
            'Charamuscas': 0.15,
            'Corazones de almendra': 0.2,
            'Dulce de tamarindo': 0.25,
            'Gomitas de mango': 0.15,
            'Mazapanes': 0.2,
            'Orejones': 0.1,
            'Piloncillo': 0.3,
            'Rosquetas de anís': 0.25,
            'Tamarindos enchilados': 0.2,
            'Tortitas de nata': 0.3,
            'Yemitas': 0.15,
            'Dulce de cacahuate': 0.35,
            'Dulce de calabaza': 0.4
        }
        return [Dulce(nombre, peso) for nombre, peso in dulces_data.items()]