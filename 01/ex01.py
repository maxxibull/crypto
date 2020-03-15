from functools import reduce
from math import gcd

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def modular_division(b, n):
    g, x, _ = extended_gcd(b, n)
    if g == 1:
        return x % n

class LCG:
    def __init__(self, seed, multiplier, increment, modulus):
        self.state = seed
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = modulus

    def generate_next(self):
        self.state = (self.state * self.multiplier + self.increment) % self.modulus
        return self.state

class LCG_Cracker:
    def crack_increment(self, values):
        self.increment = (values[1] - values[0] * self.multiplier) % self.modulus

    def crack_multiplier(self, values):
        self.multiplier = (values[2] - values[1]) * modular_division(values[1] - values[0], self.modulus) % self.modulus
        self.crack_increment(values[:2])

    def crack_modulus(self, values):
        differences = [value2 - value1 for value1, value2 in zip(values, values[1:])]
        zeroes = [diff3 * diff1 - diff2 ** 2 for diff1, diff2, diff3 in zip(differences, differences[1:], differences[2:])]
        self.modulus = abs(reduce(gcd, zeroes))
        self.state = values[-1]
        self.crack_multiplier(values[:3])

    def crack(self, values):
        self.crack_modulus(values)

    def generate_next(self):
        self.state = (self.state * self.multiplier + self.increment) % self.modulus
        return self.state


def distinguisher():
    lcg_generator = LCG(123, 672257317069504227, 7382843889490547368, 9223372036854775783)
    lcg_cracker = LCG_Cracker()
    values = [123] + [lcg_generator.generate_next() for _ in range(5)]
    lcg_cracker.crack(values)
    print(lcg_cracker.generate_next() == lcg_generator.generate_next())

distinguisher()