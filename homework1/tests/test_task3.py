import pytest
from src import task3

@pytest.mark.parametrize("value", [-1, 100, -1.1, 0, 1, -100, 5.6])
def test_positive(value):
    """ Tests function that returns whether value is positive, negative, or zero. """
    assert task3.is_positive(value)


def test_n_primes():
    """ Tests function that returns n prime numbers. """
    assert task3.n_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]



def test_sum_to_n():
    """ Tests function that returns sum of values from 1 to n. """
    assert task3.sum_to_n(100) == 5050