#http://lucumr.pocoo.org/2014/1/5/unicode-in-2-and-3/
import codecs

def safe_encode(s, name, *args, **kwargs):
    codec = codecs.lookup(name)
    rv, length = codec.encode(s, *args, **kwargs)
    if not isinstance(rv, (str, bytes, bytearray)):
        raise TypeError('Not a string or byte codec')
    return rv