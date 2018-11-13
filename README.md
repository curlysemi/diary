# diary (chacha-sha256)
_N_ plausible deniability

<!-- deniable information access resisting yatterer -->

While the encryption scheme used can theoretically be replaced (as well as the hash function used for the "passwords"), we'll refer to the algorithm contained in this repository as merely `diary`.

It's fairly simple: encrypt a list of messages with different keys.

The main idea explored here is that, in addition to supplied messages, random "messages" are also generated such that it cannot be determined, from the stored data alone, how many additional messages (if any) there may be. The drawback here is tht messages can take up a lot of storage space.

Written in python, even though I'm not that fond of it. There's a "GUI" using TkInter even though I don't really know how to use it. 🙂

### Using the GUI
* **Saving:**
  * Run:
    ```
    ./diary.py
    ```
    This will launch the GUI.
  * You can add text fields for messages using the "Add Msg" navigational button.
    * Likewise, you can remove text fields with "Remove Msg".
  * Once done entering the plaintext messages, select `File > Save`, which will prompt you for a password for each message.
* **Reading:**
  * Select `File > Open...`.
  * Enter an entry ID
  * Enter the password
    * If all goes well, the message(s) encrypted using the password .should be displayed


## Requirements
Python. Only tested on Ubuntu. If `diary` doesn't work on your OS, please open an issue.
Python3 not yet supported.

### Dependencies
```
sudo apt-get install python-tk
pip install pycryptodome
```

## TODOs
* Support python3
  * Internet keeps dying, so last error that needs to be Googled is `TypeError: Object type <class 'str'> cannot be passed to C code`.

## Example (using diary_io)
```
entry = create_entry([('secret','real'),('decoy','fake')])
save_entry(entry)
read_entry(0, 'real')
```