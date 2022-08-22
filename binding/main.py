import sum
import ctypes

import prime

#print(sum.our_function([1,2,-3,4,-5,6]))
print(prime.generate_sieve_prime(5000,4))
x = prime.find_primitive_roots(7)
print(x)
a = ctypes.cast(x, ctypes.py_object).value
#print(a)
