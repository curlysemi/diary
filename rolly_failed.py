# THIS DOESN'T WORK
# Nonprimitive roots don't generate mutually exclusive elements

import os

DEBUG=True
def dlog(msg):
    if DEBUG: print(msg)

#http://lucumr.pocoo.org/2014/1/5/unicode-in-2-and-3/
import codecs

def encode(s, name, *args, **kwargs):
    codec = codecs.lookup(name)
    rv, length = codec.encode(s, *args, **kwargs)
    if not isinstance(rv, (str, bytes, bytearray)):
        raise TypeError('Not a string or byte codec')
    return rv

# felipa
# https://codegolf.stackexchange.com/questions/10701/fastest-code-to-find-the-next-prime

# legendre symbol (a|m)
# note: returns m-1 if a is a non-residue, instead of -1
def legendre(a, m):
  return pow(a, (m-1) >> 1, m)

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

# import numpy as np
# def seive(n):
#     mask = np.ones(n+1)
#     mask[:2] = 0
#     for i in range(2, int(n**.5)+1):
#         if not mask[i]:
#             continue
#         mask[i*i::i] = 0
#     return np.argwhere(mask)
#
# def get_larger_prime(old_number):
#     try:
#         n = np.max(seive(2*old_number-1))
#         if n < old_number+1:
#             return None
#         return n
#     except ValueError:
#         return None

def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a

def get_primitive_roots(modulus):
    coprime_set = {num for num in range(1, modulus) if gcd(num, modulus) == 1}
    return [g for g in range(1, modulus) if coprime_set == {pow(g, powers, modulus)
            for powers in range(1, modulus)}]

def distinct_with_order(seq): # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def get_useful_nonprimitive_roots(modulus):
    roots = get_primitive_roots(modulus)
    symmetric_difference = set(roots) ^ set(range(modulus)) # by starting from 2, we're ignoring 0 and 1
    distincts = []
    distincts_dict = dict()
    for s in symmetric_difference:
        vals = []
        for i in range(2, modulus):
            vals.append(s**i % modulus)
        distinct = distinct_with_order(vals)
        # print(str(s) + ': (' + str(len(distinct)) + ')')
        # print('\t' + str(distinct))
        # print('')
        distinct_set = set(distinct)
        distincts.append(distinct_set)
        distincts_dict[str(distinct_set)] = s
    # print(len(symmetric_difference))
    return distincts, distincts_dict

def get_candidates(nonprimitive_roots, max_length):
    candidates = []
    for i,n in enumerate(nonprimitive_roots):
        #print(n)
        for j,m in enumerate(nonprimitive_roots):
            if len(n.intersection(m)) == 0 and len(n) >= max_length and len(m) >= max_length:
                candidates.append(set([i, j]))
    return candidates

def rand_max(max_val):
    return int(encode(os.urandom(4),'hex'), 16) % max_val

def rand_min(min_val):
    if min_val >= 0:
        min_val = 1
    return (int(encode(os.urandom(4),'hex'), 16) + min_val - 1) % (2 * min_val)

def next_with_updated_dict(char_dict):
    min_key = min(char_dict, key=char_dict.get)
    min_val = char_dict[min_key]
    curr_set = []
    for key in char_dict:
        if char_dict[key] == min_val:
            curr_set.append(key)
    next_val = curr_set[rand_max(len(curr_set))]
    char_dict[next_val] = char_dict[next_val] + 1
    return next_val, char_dict

def freq_inner(msg, ascii_dict = None):
    if ascii_dict is None:
        # dlog('None!')
        ascii_dict = dict()
        ascii_in_number = range(0,256) # or 128?
        for i in ascii_in_number:
            ascii_dict[chr(i)] = 0
    for c in msg:
        if c is not None:
            ascii_dict[c] = ascii_dict[c] + 1
    return ascii_dict

# def freq(msgs):
#     ascii_dict = dict()
#     for msg in msgs:
#         ascii_dict = freq_inner(msg, ascii_dict)
#     return ascii_dict

def roll(real, fake, power = 10):
    rolled = []
    msgs = [real, fake]
    max_len = len(max(msgs, key=len))
    # len_to_use = next_prime(rand_min(max_len * (len(msgs) + diff)))
    seq0,seq1,key0,key1=get_keys(power, max_len)
    for i in range(2**power):
        if i in seq0 and real is not '':
            rolled.append(real[0])
            real = real[1:]
        elif i in seq1 and fake is not '':
            rolled.append(fake[0])
            fake = fake[1:]
        else:
            rolled.append(None)
    analysis = freq_inner(rolled)
    # print(rolled)
    new_rolled = rolled.copy()
    # print(new_rolled)
    for i,c in enumerate(rolled):
        # print(c)
        if c is None:
            new_c, analysis = next_with_updated_dict(analysis)
            new_rolled[i] = new_c
    return ''.join(new_rolled), key0, key1

    # for msg in msgs:
    #     for c in msg:
    #         rolled.append(c)

def get_modulus(num):
    return 1023
    # return num # TODO: pass in actual prime!

def get_keys(power = 10, max_length = None):
    if max_length is None:
        max_length = power-1
    nps, nps_dict = get_useful_nonprimitive_roots(get_modulus(2**power))
    cands = get_candidates(nps, max_length)
    this_index = rand_max(len(cands))
    this_cand = list(cands[this_index])
    a,b = nps[this_cand[0]], nps[this_cand[1]]
    y,z = nps_dict[str(a)], nps_dict[str(b)]
    return a,b,y,z

def get_msg(enc_msg, key, power):
    modulus = get_modulus(2**power)
    msg = ''
    for i in range(2, modulus):
        msg = msg + enc_msg[key**i % modulus]
        # vals.append(key**i % modulus)
    return msg
    

encrypted, secret_key, decoy_key = roll('secret', 'decoy')

print(encrypted)
print('')
print('secret_key: ' + str(secret_key))
print('')
# secret_message = 
print('secret_msg:' )
print('decoy_key: ' + str(decoy_key))
print('')