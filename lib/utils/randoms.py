import os

from safe_encodings import safe_encode

from random import SystemRandom
from Crypto.Random import get_random_bytes as get_random_bytes_

def rand_max(max_val):
    return int(safe_encode(os.urandom(4),'hex'), 16) % max_val

def rand_min(min_val):
    if min_val <= 0:
        min_val = 1
    return (int(safe_encode(os.urandom(4),'hex'), 16) + min_val - 1) % (2 * min_val)

def get_random_bytes(size): return get_random_bytes_(size)

def shuffle(elements):
    cryptorand = SystemRandom()
    cryptorand.shuffle(elements)