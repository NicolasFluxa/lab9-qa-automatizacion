# features/carrito.feature
Feature: Gestión del carrito de compras
  Como cliente registrado de la tienda
  Quiero administrar los productos de mi carrito
  Para completar mi compra de forma eficiente

  Background:
    Given tengo un carrito vacío

  Scenario: Agregar un producto al carrito
    When agrego el producto "Laptop" con precio 800 y cantidad 1
    Then el carrito tiene 1 artículo
    And el total del carrito es 800

  Scenario: Agregar múltiples productos distintos
    When agrego el producto "Monitor" con precio 300 y cantidad 2
    And agrego el producto "Teclado" con precio 80 y cantidad 1
    Then el carrito tiene 3 artículos
    And el total del carrito es 680

  Scenario: Vaciar el carrito
    When agrego el producto "Laptop" con precio 800 y cantidad 1
    And agrego el producto "Monitor" con precio 300 y cantidad 1
    When vacío el carrito
    Then el carrito tiene 0 artículos
    And el total del carrito es 0

  Scenario Outline: Aplicar descuento por volumen
    When agrego el producto "Monitor" con precio 300 y cantidad <cantidad>
    And aplico el código de descuento "<codigo>"
    Then el total con descuento es <total_final>

    Examples:
      | cantidad | codigo  | total_final |
      | 1        | PROMO10 | 270         |
      | 2        | PROMO20 | 480         |
