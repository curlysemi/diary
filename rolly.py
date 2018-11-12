# felipa
# https://codegolf.stackexchange.com/questions/10701/fastest-code-to-find-the-next-prime

# legendre symbol (a|m)
# note: returns m-1 if a is a non-residue, instead of -1
def legendre(a, m):
  return pow(a, (m-1) >> 1, m)

xrange=range

# strong probable prime
def is_sprp(n, b=2):
  d = n-1
  s = 0
  while d&1 == 0:
    s += 1
    d >>= 1
  x = pow(b, d, n)
  if x == 1 or x == n-1:
    return True
  for r in range(1, s):
    x = (x * x)%n
    if x == 1:
      return False
    elif x == n-1:
      return True
  return False

# lucas probable prime
# assumes D = 1 (mod 4), (D|n) = -1
def is_lucas_prp(n, D):
  P = 1
  Q = (1-D) >> 2
  # n+1 = 2**r*s where s is odd
  s = n+1
  r = 0
  while s&1 == 0:
    r += 1
    s >>= 1
  # calculate the bit reversal of (odd) s
  # e.g. 19 (10011) <=> 25 (11001)
  t = 0
  while s > 0:
    if s&1:
      t += 1
      s -= 1
    else:
      t <<= 1
      s >>= 1
  # use the same bit reversal process to calculate the sth Lucas number
  # keep track of q = Q**n as we go
  U = 0
  V = 2
  q = 1
  # mod_inv(2, n)
  inv_2 = (n+1) >> 1
  while t > 0:
    if t&1 == 1:
      # U, V of n+1
      U, V = ((U + V) * inv_2)%n, ((D*U + V) * inv_2)%n
      q = (q * Q)%n
      t -= 1
    else:
      # U, V of n*2
      U, V = (U * V)%n, (V * V - 2 * q)%n
      q = (q * q)%n
      t >>= 1
  # double s until we have the 2**r*sth Lucas number
  while r > 0:
      U, V = (U * V)%n, (V * V - 2 * q)%n
      q = (q * q)%n
      r -= 1
  # primality check
  # if n is prime, n divides the n+1st Lucas number, given the assumptions
  return U == 0

# primes less than 212
small_primes = set([
    2,  3,  5,  7, 11, 13, 17, 19, 23, 29,
   31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
   73, 79, 83, 89, 97,101,103,107,109,113,
  127,131,137,139,149,151,157,163,167,173,
  179,181,191,193,197,199,211])

# pre-calced sieve of eratosthenes for n = 2, 3, 5, 7
indices = [
    1, 11, 13, 17, 19, 23, 29, 31, 37, 41,
   43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
   89, 97,101,103,107,109,113,121,127,131,
  137,139,143,149,151,157,163,167,169,173,
  179,181,187,191,193,197,199,209]

# distances between sieve values
offsets = [
  10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6,
   6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4,
   2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6,
   4, 2, 4, 6, 2, 6, 4, 2, 4, 2,10, 2]

max_int = 2147483647

# an 'almost certain' primality check
def is_prime(n):
  if n < 212:
    return n in small_primes
  for p in small_primes:
    if n%p == 0:
      return False
  # if n is a 32-bit integer, perform full trial division
  if n <= max_int:
    i = 211
    while i*i < n:
      for o in offsets:
        i += o
        if n%i == 0:
          return False
    return True
  # Baillie-PSW
  # this is technically a probabalistic test, but there are no known pseudoprimes
  if not is_sprp(n): return False
  a = 5
  s = 2
  while legendre(a, n) != n-1:
    s = -s
    a = s-a
  return is_lucas_prp(n, a)

# next prime strictly larger than n
def next_prime(n):
  if n < 2:
    return 2
  # first odd larger than n
  n = (n + 1) | 1
  if n < 212:
    while True:
      if n in small_primes:
        return n
      n += 2
  # find our position in the sieve rotation via binary search
  x = int(n%210)
  s = 0
  e = 47
  m = 24
  while m != e:
    if indices[m] < x:
      s = m
      m = (s + e + 1) >> 1
    else:
      e = m
      m = (s + e) >> 1
  i = int(n + (indices[m] - x))
  # adjust offsets
  offs = offsets[m:]+offsets[:m]
  while True:
    for o in offs:
      if is_prime(i):
        return i
      i += o



#http://lucumr.pocoo.org/2014/1/5/unicode-in-2-and-3/
import codecs

def encode(s, name, *args, **kwargs):
    codec = codecs.lookup(name)
    rv, length = codec.encode(s, *args, **kwargs)
    if not isinstance(rv, (str, bytes, bytearray)):
        raise TypeError('Not a string or byte codec')
    return rv

import os

def rand_max(max_val):
    return int(encode(os.urandom(4),'hex'), 16) % max_val

def rand_min(min_val):
    if min_val <= 0:
        min_val = 1
    return (int(encode(os.urandom(4),'hex'), 16) + min_val - 1) % (2 * min_val)

### https://gist.github.com/chrix2/4171336

import binascii
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class PKCS7Encoder(object):
    def __init__(self, k=16):
       self.k = k

    ## @param text The padded text for which the padding is to be removed.
    # @exception ValueError Raised when the input padding is missing or corrupt.
    def decode(self, text):
        '''
        Remove the PKCS#7 padding from a text string
        '''
        nl = len(text)
        val = int(binascii.hexlify(text[-1]), 16)
        if val > self.k:
            raise ValueError('Input is not padded or padding is corrupt')

        l = nl - val
        return text[:l]

    ## @param text The text to encode.
    def encode(self, text):
        '''
        Pad an input string according to PKCS#7
        '''
        l = len(text)
        output = StringIO()
        val = self.k - (l % self.k)
        for _ in xrange(val):
            output.write('%02x' % val)
        return text + binascii.unhexlify(output.getvalue())


###
import json
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from random import SystemRandom

import hashlib

def get_nonce(index):
    s = bin(index)[2:].zfill(12*8)
    bs = []
    for i in range(0, len(s), 8):
        bs.append(int(s[i : i + 8], 2))
    return bytearray(bs)

def get_prefix(index):
    return "<%" + str(index) + "%>"

def prepend(msg, index):
    return get_prefix(index) + msg 

def enc(msgs, keys, diff = 0, index = 0):
    new_msgs = []
    for msg in msgs:
        if msg is not None:
            new_msgs.append(prepend(msg, index))
        else:
            new_msgs.append(None)
    msgs = new_msgs
    max_len = len(max(msgs, key=len))
    # print(max_len)
    len_to_use = next_prime(rand_min(next_prime(max_len * (len(msgs) + diff))))
    # print(len_to_use)
    ciphertexts = []
    encoder = PKCS7Encoder(len_to_use)
    nonce = get_nonce(index)
    for i in range(len_to_use):
        if i >= len(msgs) or msgs[i] is None:
            plaintext = get_random_bytes(len_to_use)
        else:
            plaintext = msgs[i]
            plaintext = encoder.encode(plaintext)
        #n = int(hashlib.sha256(keys[i]).hexdigest(), 16) 
        if i >= len(keys) or keys[i] is None:
            key = get_random_bytes(32)
        else:
            key = hashlib.sha256(keys[i]).digest()  #str(n).encode()
        # print(key)
        cipher = ChaCha20.new(key=key, nonce=nonce)
        # cipher = ChaCha20.new(key=key)
        ciphertext = cipher.encrypt(plaintext)
        # nonce = b64encode(cipher.nonce).decode('utf-8')
        ciphertexts.append(ciphertext)
    cryptorand = SystemRandom()
    cryptorand.shuffle(ciphertexts)
    return ciphertexts

from base64 import b64decode

def dec(msgs, key, index):
    key = hashlib.sha256(key).digest()
    nonce = get_nonce(index)
    decs = []
    encoder = PKCS7Encoder(len(msgs))
    for enc_msg in msgs:
        ciphertext = enc_msg # b64decode(enc_msg)
        cipher = ChaCha20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            decs.append(encoder.decode(plaintext))
        except:
            pass
    matches = []
    prefix = get_prefix(index)
    for dec in decs:
        if dec.startswith(prefix):
            matches.append(dec.replace(prefix, ''))
    return matches

"""
TODOs:
    [X] Real message must be at random position
    [X] Add special character sequence at beginning message using nonce value so that decryption of a message can be differentiated from failed decryptions
"""
