import pytest
from src import task3

@pytest.mark.parametrize("value, result", [(-1, "negative"), (100, "positive"), (-1.1, "negative"), (0, "zero"), (1, "positive"), (-100, "negative"), (5.6, "positive")])
def test_is_positive(value, result):
    """ Tests function that returns whether value is positive, negative, or zero. """
    assert task3.is_positive(value) == result


def test_n_primes():
    """ Tests function that returns n prime numbers. """
    assert task3.n_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    with pytest.raises(ValueError):
        task3.n_primes(0)


@pytest.mark.parametrize("value, result", [(100, 5050), (0, 0), (5, 15), (2.2, 3)])
def test_sum_to_n(value, result):
    """ Tests function that returns sum of values from 1 to n. """
    assert task3.sum_to_n(value) == result
    with pytest.raises(ValueError):
        task3.sum_to_n(-100)