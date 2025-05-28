from abc import ABC, abstractmethod

# Elemento base del menú
class ItemMenu(ABC):
    def __init__(self, titulo: str, costo: float):
        self._titulo = titulo
        self._costo = costo

    # Getters
    def get_titulo(self):
        return self._titulo

    def get_costo(self):
        return self._costo

    # Setters
    def set_titulo(self, titulo):
        self._titulo = titulo

    def set_costo(self, costo):
        self._costo = costo

    def obtener_precio(self) -> float:
        return self._costo

    def __str__(self) -> str:
        return f"{self._titulo} - ${self._costo:.2f}"

# Bebida específica
class Refresco(ItemMenu):
    def __init__(self, titulo: str, costo: float, medida: str):
        super().__init__(titulo, costo)
        self._medida = medida

    # Getters
    def get_medida(self):
        return self._medida

    # Setters
    def set_medida(self, medida):
        self._medida = medida

    def __str__(self) -> str:
        return f"{self._titulo} [{self._medida}] - ${self._costo:.2f}"

# Aperitivo
class Picada(ItemMenu):
    def __init__(self, titulo: str, costo: float, compartir: bool):
        super().__init__(titulo, costo)
        self._compartir = compartir

    # Getters
    def get_compartir(self):
        return self._compartir

    # Setters
    def set_compartir(self, compartir):
        self._compartir = compartir

# Plato principal
class ComidaFuerte(ItemMenu):
    def __init__(self, titulo: str, costo: float, vegetariano: bool):
        super().__init__(titulo, costo)
        self._vegetariano = vegetariano

    # Getters
    def get_vegetariano(self):
        return self._vegetariano

    # Setters
    def set_vegetariano(self, vegetariano):
        self._vegetariano = vegetariano

# Manejo del pedido
class Pedido:
    def __init__(self):
        self.detalles = []

    def incluir(self, producto: ItemMenu):
        self.detalles.append(producto)

    def mostrar_resumen(self):
        print("\n🧾 Pedido Final:")
        for prod in self.detalles:
            print(f" • {prod}")
        print(f"\nTotal a pagar: ${self.total_con_descuento():.2f}")

    def total_bruto(self) -> float:
        total = 0.0
        for p in self.detalles:
            total += p.obtener_precio()
        return total

    def total_con_descuento(self) -> float:
        hay_plato_fuerte = False
        for p in self.detalles:
            if isinstance(p, ComidaFuerte):
                hay_plato_fuerte = True
                break

        total = 0.0
        for p in self.detalles:
            precio = p.obtener_precio()
            # Aplica descuento del 20% a refrescos si hay plato fuerte
            if hay_plato_fuerte and isinstance(p, Refresco):
                precio *= 0.8
            total += precio

        # Descuento adicional si más de 3 items
        if len(self.detalles) > 3:
            total *= 0.9

        return total

# Clase para manejo de pagos
class Payment:
    def __init__(self, monto):
        self._monto = monto
        self._pagado = False

    # Getters y setters
    def get_monto(self):
        return self._monto

    def set_monto(self, monto):
        self._monto = monto

    def pagar(self, cantidad):
        if cantidad >= self._monto:
            self._pagado = True
            cambio = cantidad - self._monto
            print(f"Pago recibido: ${cantidad:.2f}. Cambio: ${cambio:.2f}. ¡Gracias por su compra!")
            return cambio
        else:
            faltante = self._monto - cantidad
            print(f"Pago insuficiente. Faltan ${faltante:.2f}.")
            return None

    def esta_pagado(self):
        return self._pagado

# Menú disponible
catalogo = [
    Refresco("Limonada Natural", 2.50, "Mediana"),
    Refresco("Espresso", 3.00, "Chico"),
    Refresco("Té Frutal", 2.75, "Grande"),
    Picada("Spring Rolls", 5.50, True),
    Picada("Tostadas con Ajo", 4.00, False),
    ComidaFuerte("Pechuga Grillada", 12.00, False),
    ComidaFuerte("Pasta Vegana", 10.50, True),
    ComidaFuerte("Burger Clásica", 11.25, False),
    ComidaFuerte("Tofu Stir-Fry", 9.75, True),
    Picada("Nachos con Queso", 6.00, True)
]

if __name__ == "__main__":
    mi_pedido = Pedido()
    mi_pedido.incluir(catalogo[1])  # Espresso
    mi_pedido.incluir(catalogo[3])  # Spring Rolls
    mi_pedido.incluir(catalogo[5])  # Pechuga Grillada
    mi_pedido.incluir(catalogo[8])  # Tofu Stir-Fry
    mi_pedido.mostrar_resumen()

    pago = Payment(mi_pedido.total_con_descuento())
    pago.pagar(30)
