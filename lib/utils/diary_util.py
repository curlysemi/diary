from safe_encodings import safe_encode
from primes import next_prime
from randoms import rand_min, get_random_bytes, shuffle
from ..models.pkcs7encoder import PKCS7Encoder

xrange=range

###
from Crypto.Cipher import ChaCha20

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

def get_key(password):
    key = hashlib.sha256(safe_encode(password, 'utf-8'))
    return key.digest()

def enc(msgs, keys, diff = 0, index = 0):
    new_msgs = []
    for msg in msgs:
        if msg is not None:
            new_msgs.append(prepend(msg, index))
        else:
            new_msgs.append(None)
    msgs = new_msgs
    max_len = len(max(msgs, key=len))
    len_to_use = next_prime(rand_min(next_prime(max_len * (len(msgs) + diff))))
    ciphertexts = []
    encoder = PKCS7Encoder(len_to_use)
    nonce = get_nonce(index)
    for i in range(len_to_use):
        if i >= len(msgs) or msgs[i] is None:
            plaintext = get_random_bytes(len_to_use)
        else:
            plaintext = msgs[i]
            plaintext = encoder.encode(plaintext)
        if i >= len(keys) or keys[i] is None:
            key = get_random_bytes(32)
        else:
            key = get_key(keys[i])
        cipher = ChaCha20.new(key=key, nonce=nonce)
        ciphertext = cipher.encrypt(plaintext)
        ciphertexts.append(ciphertext)
    shuffle(ciphertexts)
    return ciphertexts

def dec(msgs, password, index):
    key = get_key(password)
    nonce = get_nonce(index)
    decs = []
    encoder = PKCS7Encoder(len(msgs))
    for enc_msg in msgs:
        ciphertext = enc_msg
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
    # return decs
