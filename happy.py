# Generator for happy numbers
def happys(n):
    i = 0
    while True:
        if is_happy(n + i):
            yield n + i
        i += 1

# Generator for happy primes
def happy_primes(n):
    hs = happys(n)
    while True:
        n = next(hs)
        if is_prime(n):
            yield n

# Sum of squares of digits
def sum_squares(n):
    digits = [int(ch) ** 2 for ch in str(n)]
    return sum(digits)

# Find if a number is happy
# Sum of squares of digits sequence converges to 1
def is_happy(n):
    res = n
    unhappys = (42, 20, 4, 16, 37, 58, 89, 145)
    while res != 1 and res not in unhappys:
        res = sum_squares(res)
    return res == 1

# Memoization of finding if a number is prime
nonprimes = set()
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
