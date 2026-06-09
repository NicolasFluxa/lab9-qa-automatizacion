# tests/test_descuentos.py
import pytest
from app.descuentos import calcular_descuento


@pytest.mark.parametrize('total, codigo, esperado', [
    (100,  'PROMO10',  90.0),   # 10% descuento
    (200,  'PROMO20', 160.0),   # 20% descuento
    (500,  'PROMO10', 450.0),   # 10% sobre total alto
    (0,    'PROMO10',   0.0),   # borde: total cero
    (100,  'INVALIDO', 100.0),  # código inexistente → sin descuento
    (100,  '',         100.0),  # borde: código vacío → sin descuento
])
def test_calcular_descuento(total, codigo, esperado):
    resultado = calcular_descuento(total, codigo)
    assert resultado == pytest.approx(esperado), \
        f'Para total={total}, codigo={codigo!r}: esperado={esperado}, obtenido={resultado}'


def test_descuento_no_acepta_total_negativo():
    with pytest.raises(ValueError, match='El total no puede ser negativo'):
        calcular_descuento(-50, 'PROMO10')
