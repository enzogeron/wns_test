import math


def calculate_quantity_buy(required_g: float) -> float:
    """
    Funcion para calcular cantidad real a comprar (redondeada a multiplos de 250g)
    """
    if required_g <= 0:
        return 0
    return float(math.ceil(required_g / 250) * 250)