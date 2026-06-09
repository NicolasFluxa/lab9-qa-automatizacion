# app/carrito.py
class Carrito:
    """Gestiona los artículos del carrito de compras."""

    def __init__(self):
        self._items = []

    def agregar(self, nombre: str, precio: float) -> None:
        """Agrega un artículo al carrito."""
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._items.append({"nombre": nombre, "precio": precio})

    def cantidad(self) -> int:
        """Retorna el número de artículos en el carrito."""
        return len(self._items)

    def total(self) -> float:
        """Retorna el precio total de todos los artículos."""
        return sum(item["precio"] for item in self._items)

    def vaciar(self) -> None:
        """Elimina todos los artículos del carrito."""
        self._items.clear()
