# app/pagos.py
class ProcesadorPago:
    """Procesa pagos usando una pasarela de pago externa."""

    def __init__(self, pasarela):
        """
        Args:
            pasarela: Objeto PasarelaPago (puede ser mock en tests).
        """
        self.payment_gateway = pasarela

    def procesar(self, monto: float, cliente: str) -> dict:
        """
        Procesa un cobro a través de la pasarela.
        Returns: dict con 'estado' y 'txn_id'.
        Raises: ConnectionError si la pasarela no está disponible.
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero")
        resultado = self.payment_gateway.cobrar(monto=monto)
        return resultado
