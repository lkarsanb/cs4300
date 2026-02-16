import pytest
from src import task2

@pytest.mark.parametrize("value", [task2.int1, task2.int2, task2.int_sum])
def test_integer(value):
    """ Tests to check if value is an integer. """
    assert isinstance(value, int)


@pytest.mark.parametrize("value", [task2.int_sum])
def test_sum(value):
    """ Tests if the two integers results in an integer."""
    assert value == 4


@pytest.mark.parametrize("f_val", [task2.float1, task2.float2])
def test_float(f_val):
    """ Tests to check if value is a float. """
    assert isinstance(f_val, float)


@pytest.mark.parametrize("s_val", [task2.str1, task2.str2, task2.concat_str])
def test_string(s_val):
    """ Tests to check if value is a string. """
    assert isinstance(s_val, str)


@pytest.mark.parametrize("result", [task2.concat_str])
def test_concatenation(result):
    """ Tests if the two strings concatente correctly."""
    assert result == "Hello, world!"


@pytest.mark.parametrize("b_val", [task2.bool1, task2.bool2])
def test_bool(b_val):
    """ Tests to check if value is a boolean. """
    assert isinstance(b_val, bool)