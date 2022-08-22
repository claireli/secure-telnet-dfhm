#a number g is a primitive root modulo n if every number a coprime to n is congruent to a power of g modulo n. That is, g is a primitive root modulo n if for every integer a coprime to n, there is some integer k for which gk ≡ a (mod n). Such a value k is called the index or discrete logarithm of a to the base g modulo n. So g is a primitive root modulo n if and only if g is a generator of the multiplicative group of integers modulo n.
import prime

def get_co_primes(p):
  print(f"Find all coprime numbers to {p}")

def primitive_root_modulo(p):
  print(f"Find all primitive root modulo {p}")
  get_co_primes(p)

primitive_root_modulo(23)
print(prime.generate_sieve_prime(1000,3))
