# tests/test_carrito.py
import pytest
from app.carrito import Carrito


def test_carrito_vacio_al_iniciar(carrito_vacio):
    # Assert
    assert carrito_vacio.cantidad() == 0


def test_agregar_producto_incrementa_cantidad(carrito_vacio, productos_muestra):
    # Arrange
    producto = productos_muestra[0]  # Laptop, 800
    # Act
    carrito_vacio.agregar(producto["nombre"], producto["precio"])
    # Assert
    assert carrito_vacio.cantidad() == 1


def test_total_suma_precios_correctamente(carrito_vacio, productos_muestra):
    # Act: Laptop(800) + Monitor(300)
    carrito_vacio.agregar(productos_muestra[0]["nombre"], productos_muestra[0]["precio"])
    carrito_vacio.agregar(productos_muestra[1]["nombre"], productos_muestra[1]["precio"])
    # Assert
    assert carrito_vacio.total() == 1100


def test_agregar_producto_duplicado_incrementa_cantidad(carrito_vacio, productos_muestra):
    # Arrange
    producto = productos_muestra[0]  # mismo SKU dos veces
    # Act
    carrito_vacio.agregar(producto["nombre"], producto["precio"])
    carrito_vacio.agregar(producto["nombre"], producto["precio"])
    # Assert
    assert carrito_vacio.cantidad() == 2


def test_vaciar_deja_carrito_en_cero(carrito_vacio, productos_muestra):
    # Arrange
    carrito_vacio.agregar(productos_muestra[0]["nombre"], productos_muestra[0]["precio"])
    carrito_vacio.agregar(productos_muestra[1]["nombre"], productos_muestra[1]["precio"])
    # Act
    carrito_vacio.vaciar()
    # Assert
    assert carrito_vacio.cantidad() == 0
