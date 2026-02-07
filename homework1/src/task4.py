from decimal import Decimal, ROUND_HALF_UP

def calculate_discount(price, discount):
    """
    Returns the resulting price after applying a discount to a given price.

    Parameters:
        price (int, float): The original price of the item.
        discount (int, float): The discount to apply to the price.
    
    Returns:
        rounded_value (str): A string of the price of the product after applying the discount in the format of #.##.
    """

    if not isinstance(price, (int, float)):
        raise TypeError(f"Expected an int or float for price, recieved a {type(price).__name__}")
    if not isinstance(discount, (int, float)):
        raise TypeError(f"Expected an int or float for discount, recieved a {type(discount).__name__}")
    if discount < 0 or discount > 100:
        raise ValueError(f"Expected discount to be in range 0 to 100.")
    
    d_price = Decimal(price)
    d_discount = Decimal(discount)
    value = d_price - (Decimal(price) * Decimal(d_discount) / 100)
    
    # Properly round up with format of #.##5
    rounded_value = value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    return f"{rounded_value}"