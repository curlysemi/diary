import os, json
from lib.models.entry import Entry
import lib.utils.diary_util as diary_util

DIRECTORY = '.entries'
EXT = '.dat'

def filename_to_index(filename):
    return int(filename.replace(EXT, ''))

def index_to_filename(index):
    return os.path.join(DIRECTORY, str(index) + EXT)

def get_next_available_index():
    next_index = 0
    if os.path.exists(DIRECTORY):
        files = [f for f in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, f))]
        if files:
            files.sort(key=filename_to_index)
            last = filename_to_index(files[-1])
            next_index = last + 1
    return next_index

def create_entry(message_password_pairs):
    index = get_next_available_index()
    # print(index)
    messages = []
    passwords = []
    for message,password in message_password_pairs:
        messages.append(message)
        passwords.append(password)
    # print(messages)
    # print(passwords)
    encrypted_entry_data = diary_util.enc(messages, passwords, index=index)
    entry = Entry(encrypted_entry_data, index)
    return entry

def save_entry(entry):
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    filename = index_to_filename(entry.index)
    entry_file = open(filename, 'w')
    entry_file.write(entry.serialize())
    entry_file.close()

import base64
def read_entry(index, password):
    # try:
    filename = index_to_filename(index)
    entry_file = open(filename, 'r')
    serialized_encrypted_entry_data = entry_file.read()
    entry_file.close()
    encrypted_entry_data = json.loads(serialized_encrypted_entry_data)
    data = []
    for datum in encrypted_entry_data:
        data.append(base64.b64decode(datum))
    return diary_util.dec(data, password, index)
    # except:
    #     print('Error reading file!')
    #     return None