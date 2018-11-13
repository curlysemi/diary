# diary-chacha-sha256
_N_ plausible deniability

<!-- deniable
information
access
resource
retrieval
yandee/yabba/yardel/yar-nut/yentz -->


While the encryption scheme used can theoretically be replaced (as well as the hash function used for the "passwords"), we'll refer to the algorithm contained in this repository as merely `diary`.

It's fairly simple: encrypt a list of messages with different keys.

## Requirements
Python. Only tested on Ubuntu. If `diary` doesn't work on your OS, please open an issue.
Python3 not yet supported.

## Installation
```
pip install pycryptodome
```

## TODOs
* Support python3
  * Internet keeps dying, so last error that needs to be Googled is `TypeError: Object type <class 'str'> cannot be passed to C code`.

## Example
```
entry = create_entry([('secret','real'),('decoy','fake')])
save_entry(entry)
read_entry(0, 'real')
```

https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file/14870531#14870531