# Generator for happy numbers, starting at n
def happys(n = 1):
    i = 0
    while True:
        if is_happy(n + i):
            yield n + i
        i += 1

# Generator for happy primes, starting at n
def happy_primes(n = 1):
    hs = happys(n)
    while True:
        n = next(hs)
        if is_prime(n):
            yield n

# Sum of squares of digits
def sum_squares(n):
    digits = [int(ch) ** 2 for ch in str(n)]
    return sum(digits)

# Sets for memoization
# Functions is_happy and is_prime add to these when the find numbers that
# aren't happy or aren't prime, respectively
# TODO this is probably a bad design, considering there are many more unhappys
# than there are happys
nonprimes = set()
unhappys = {42, 20, 4, 16, 37, 58, 89, 145}

# Find if a number is happy
# Sum of squares of digits sequence eventually goes to 1
def is_happy(n):
    res = n
    while res != 1 and res not in unhappys:
        res = sum_squares(res)
    if res != 1:
        unhappys.add(n)
        return False
    else:
        return True

# Find if a number is prime
def is_prime(n):
    if n % 2 == 0 or n in nonprimes:
       return n == 2 # 2 is prime but even
    else:
        if len(factors(n)) > 2:
            nonprimes.add(n)
            return False
    return True

# Finds the factors of a number
def factors(n):
    i = n - 1
    facts = {1, n}
    while i > 1:
        if n % i == 0:
            facts.add(i)
        i -= 1
    return facts

# Main program
if __name__ == '__main__':
    # Instantiate a generator for happy numbers
    h = happys(1)

    # Print the first hundred happy numbers
    i = 0
    while i < 100:
        print(next(h))
        i += 1

    # Instantiate a generator for happy primes
    p = happy_primes(1)

    # Print the first hundred happy primes
    i = 0
    while i < 100:
        print(next(p))
        i += 1
