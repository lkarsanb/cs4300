def is_positive(val):
    """ Returns if a value is positive, negative, or zero."""
    if val > 0:
        return "positive"
    elif val < 0:
        return "negative"
    else:
        return "zero"



def n_primes(n):
    """
    Returns the first n prime numbers, up to prime number 5003, using Sieve of Eratosthenes algorithm.
    (Essentially, algorithm works by finding a prime number, then eliminating all multiples of that prime number).

    Parameters:
        n (int): Number of prime values to return.
    
    Returns:
        prime_vals (list): A list containing the first n prime numbers.
    """
    # As a boundary, make limit of largest prime number to find 5003.
    max = 5003

    is_prime = [True] * (max + 1)

    # 0 and 1 are not prime, so initialize with False.
    is_prime[0] = False
    is_prime[1] = False

    # Set up counter to keep track of number of primes found.
    num_primes = 0

    # Set up list to hold prime numbers found.
    prime_vals = []

    # 1 is not prime, so start iteration from i = 2 up to max.
    for i in range(2, max + 1):
        if is_prime[i]:
            num_primes += 1
            prime_vals.append(i)
            for multiple in range(i * i, max + 1, i):
                # Mark all multiples as not prime.
                is_prime[multiple] = False
        
        if num_primes == n:
            break
    
    return prime_vals


def sum_to_n(n):
    """
    Returns the sum of values from 1 to n.

    Parameters:
        n (int): Max value to add to.
    
    Returns:
        sum (int): The sum of values added.
    """

    counter = 1
    sum = 0
    while n >= counter:
        sum += counter
        counter += 1

    return sum