# diary (chacha-sha256)
_N_ plausible deniability, because encryption may not always be enough — systems may need to be coercion-resistant.

<!-- deniable information access resisting yatterer -->

## Example (using diary_io.py)
```
>>> entry = create_entry([('secret','real'),('decoy','fake')])
>>> save_entry(entry)
>>> read_entry(0, password='real')
['secret']
>>> read_entry(0, password='fake')
['decoy']
```

It's fairly simple: encrypt a list of messages with different keys. You can have as many "decoy" messages as you like!

The main idea explored here is that, in addition to the supplied messages, random "messages" are also generated such that it cannot be determined, from the stored data alone, how many additional messages (if any) there may be. The drawback here is that messages can take up a lot of storage space.

While the encryption scheme used (ChaCha20) can theoretically be replaced (as well as the hash function used for the "passwords," which is SHA256), we'll refer to the "algorithm" contained in this repository as merely `diary`.

> This is just a toy proof-of-concept written in python, even though I'm not that fond of it as a language. There's a "GUI" using TkInter even though I don't really know how to use it. 🙂

### Using the GUI
Run:
```
./diary.py
```
This will launch the GUI.
* **Saving:**
  * You can add text fields for messages using the "Add Msg" navigational button.
    * Likewise, you can remove text fields with "Remove Msg".
  * Once done entering the plaintext messages, select `File > Save`, which will prompt you for a password for each message.
* **Reading:**
  * Select `File > Open...`.
  * Enter an entry ID
  * Enter the password
    * If all goes well, the message(s) encrypted using the password should be displayed.

## Requirements
Python. Only tested on Ubuntu 16.04 and 18.04. If `diary` doesn't work on your OS, please open an issue.
Python3 not yet supported.

### Dependencies
```
sudo apt-get install python-tk
pip install pycryptodome
```

## TODOs
* Support Python3
* Make GUI less horrible
* Come up with a cool acronym for `diary`
* Proper setup script
* Better password/message UX
* Alternative to index-based approach for UI
