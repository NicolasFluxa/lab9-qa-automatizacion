# tests/conftest.py
import pytest
from app.carrito import Carrito


@pytest.fixture
def carrito_vacio():
    """Retorna una instancia limpia de Carrito antes de cada test."""
    c = Carrito()
    yield c
    c.vaciar()  # teardown — limpieza garantizada aunque el test falle


@pytest.fixture(scope='module')
def productos_muestra():
    """Catálogo de productos reutilizado en todo el módulo."""
    return [
        {"sku": "SKU-001", "nombre": "Laptop", "precio": 800},
        {"sku": "SKU-002", "nombre": "Monitor", "precio": 300},
        {"sku": "SKU-003", "nombre": "Teclado", "precio": 80},
    ]
