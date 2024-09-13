import math

def calculate_purchased(K1, K2, K3, size, CEPCI = 397):
    log_size = math.log(size, 10)
    cp0 = 10**(K1 + K2 * log_size + K3 * (log_size ** 2))
    return cp0*(CEPCI/397)

def calculate_bare_module_simple(purchased, bare_module):
    return purchased*bare_module