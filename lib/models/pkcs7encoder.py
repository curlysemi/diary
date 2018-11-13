### https://gist.github.com/chrix2/4171336

import binascii
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from ..utils.safe_encodings import safe_encode

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
        encoded = binascii.unhexlify(output.getvalue())
        print(type(encoded))
        print(encoded)
        print(type(text))
        print(text)
        encoded = ''.join( chr(x) for x in bytearray(encoded) )
        # text = ''.join( chr(x) for x in bytearray(text) )
        text = safe_encode(text, 'ascii')
        return text + encoded