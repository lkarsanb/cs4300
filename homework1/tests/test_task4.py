import pytest, re
from src import task4
from decimal import InvalidOperation

@pytest.mark.parametrize("price, discount, value", [(100, 20, "80.00"), (50.50, 15, "42.93"), (20, 0, "20.00"), (100, 100, "0.00"), ("100", 25.5, "74.50")])
def test_calculate_discount(price, discount, value):
    """ Tests calculate_discount if price and discount are not ints or floats. """
    assert task4.calculate_discount(price, discount) == value

    # Ensure prices are returned in format #.##
    pattern = r"\d+\.\d{2}" 
    assert re.match(pattern, task4.calculate_discount(price, discount))


@pytest.mark.parametrize("price, discount", [("abc", 100), ("!123", 5)])
def test_calculate_discount_invalid_operation(price, discount):
    """ Tests calculate_discount if discount value is not between 0 and 100. """
    with pytest.raises(InvalidOperation):
        task4.calculate_discount(price, discount)


@pytest.mark.parametrize("price, discount", [(100, "abc"), (50, "-1"), ("hi", "hi"), ("100", "hi")])
def test_calculate_discount_type_error(price, discount):
    """ Tests calculate_discount if strings are given for either price. """
    with pytest.raises(TypeError):
        task4.calculate_discount(price, discount)


@pytest.mark.parametrize("price, discount", [(100, 101), (100, -1),("Hi", -1)])
def test_calculate_discount_value_error(price, discount):
    """ Tests calculate_discount if strings are given for either price. """
    with pytest.raises(ValueError):
        task4.calculate_discount(price, discount)