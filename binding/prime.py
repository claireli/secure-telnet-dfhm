import ctypes

_prime = ctypes.CDLL('liberato.so')
_prime.generate_sieve_prime.argtypes = (ctypes.c_int, ctypes.c_int)

def generate_sieve_prime(n, prime_len):
    global _prime
    result = _prime.generate_sieve_prime(ctypes.c_int(n), ctypes.c_int(prime_len))
    #print("THIS IS THE RESULT INSIDE OF THE WRAPPER ", result)
    return int(result)

def find_primitive_roots(n):
    global _prime
    result = _prime.find_primitive_roots(ctypes.c_int(n))
    return result
