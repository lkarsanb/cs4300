import pytest, re
from src import task4

@pytest.mark.parametrize("price, discount, value", [(100, 20, "80.00"), (50.50, 15, "42.93"), (20, 0, "20.00"), (100, 100, "0.00")])
def test_invalid_types(price, discount, value):
    """ Tests calculate_discount if price and discount are not ints or floats. """
    assert task4.calculate_discount(price, discount) == value

    # Ensure prices are returned in format #.##
    pattern = r"\d+\.\d{2}" 
    assert re.match(pattern, task4.calculate_discount(price, discount))

@pytest.mark.parametrize("price, discount", [(100, 101), (100, -1)])
def test_invalid_discount_val(price, discount):
    """ Tests calculate_discount if discount value is not between 0 and 100. """
    with pytest.raises(ValueError):
        task4.calculate_discount(price, discount)


@pytest.mark.parametrize("price, discount", [(100, "Hi"), ("Hi", -1), ("10", "10")])
def test_apply_discount(price, discount):
    """ Tests calculate_discount if valid entries given. """
    with pytest.raises(TypeError):
        task4.calculate_discount(price, discount)