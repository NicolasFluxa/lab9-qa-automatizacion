# tests/test_pagos.py
#
# f) ¿Por qué es incorrecto usar la PasarelaPago real en los tests automáticos?
#    Usar la pasarela real ejecutaría cobros reales en cada corrida del test, lo cual
#    es inaceptable y tiene consecuencias financieras. Además, los tests dependerían
#    de disponibilidad de red y del servicio externo, perdiendo determinismo y velocidad.
#    Los tests unitarios deben ser aislados, rápidos y sin efectos secundarios externos.
#
# g) ¿Qué diferencia existe entre un Stub y un Mock? ¿Cuál de los dos usaste en
#    test_pago_exitoso_retorna_txn_id?
#    - Stub: test double que devuelve respuestas predefinidas; NO verifica cómo fue llamado.
#    - Mock: test double que devuelve respuestas predefinidas Y VERIFICA que fue llamado
#      con los argumentos y la cantidad de veces correctas (assert_called, assert_called_once_with).
#    En test_pago_exitoso_retorna_txn_id el MagicMock actúa como STUB: solo configuramos
#    el valor de retorno y verificamos el resultado, sin comprobar cómo se invocó la pasarela.

import pytest
from unittest.mock import MagicMock, patch
from app.pagos import ProcesadorPago


@pytest.fixture
def procesador_con_mock():
    """Fixture que provee ProcesadorPago con pasarela mockeada."""
    mock_pasarela = MagicMock()
    mock_pasarela.cobrar.return_value = {"estado": "ok", "txn_id": "TXN-TEST-001"}
    return ProcesadorPago(pasarela=mock_pasarela), mock_pasarela


def test_pago_exitoso_retorna_txn_id(procesador_con_mock):
    procesador, mock_pasarela = procesador_con_mock
    resultado = procesador.procesar(monto=150.0, cliente="ana@mail.com")
    assert resultado["txn_id"] == "TXN-TEST-001"
    assert resultado["estado"] == "ok"


def test_pago_llama_pasarela_con_monto_correcto(procesador_con_mock):
    procesador, mock_pasarela = procesador_con_mock
    procesador.procesar(monto=250.0, cliente="ana@mail.com")
    mock_pasarela.cobrar.assert_called_once_with(monto=250.0)


def test_pago_sin_duplicados(procesador_con_mock):
    """Verifica que no se realizan cobros duplicados."""
    procesador, mock_pasarela = procesador_con_mock
    procesador.procesar(monto=100.0, cliente="juan@mail.com")
    assert mock_pasarela.cobrar.call_count == 1


def test_pago_falla_cuando_pasarela_lanza_excepcion():
    mock_pasarela = MagicMock()
    mock_pasarela.cobrar.side_effect = ConnectionError("Pasarela no disponible")
    procesador = ProcesadorPago(pasarela=mock_pasarela)
    with pytest.raises(ConnectionError):
        procesador.procesar(monto=50.0, cliente="luis@mail.com")
