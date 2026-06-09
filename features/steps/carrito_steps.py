# features/steps/carrito_steps.py
from behave import given, when, then
from app.carrito import Carrito
from app.descuentos import calcular_descuento


@given('tengo un carrito vacío')
def step_carrito_vacio(context):
    context.carrito = Carrito()


@when('agrego el producto "{nombre}" con precio {precio:d} y cantidad {cantidad:d}')
def step_agregar_producto(context, nombre, precio, cantidad):
    for _ in range(cantidad):
        context.carrito.agregar(nombre, precio)


@when('vacío el carrito')
def step_vaciar_carrito(context):
    context.carrito.vaciar()


@when('aplico el código de descuento "{codigo}"')
def step_aplicar_descuento(context, codigo):
    context.total_con_descuento = calcular_descuento(context.carrito.total(), codigo)


@then('el carrito tiene {cantidad:d} artículo')
def step_carrito_tiene_articulo_singular(context, cantidad):
    assert context.carrito.cantidad() == cantidad


@then('el carrito tiene {cantidad:d} artículos')
def step_carrito_tiene_articulos_plural(context, cantidad):
    assert context.carrito.cantidad() == cantidad


@then('el total del carrito es {total:d}')
def step_total_carrito(context, total):
    assert context.carrito.total() == total


@then('el total con descuento es {total_final:d}')
def step_total_con_descuento(context, total_final):
    assert abs(context.total_con_descuento - total_final) < 0.01
