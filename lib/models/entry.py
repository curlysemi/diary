import json, base64

class Entry(object):
    def __init__(self, data, index):
       self.data = data
       self.index = index

    def serialize(self):
        data = []
        for datum in self.data:
            data.append(base64.encodestring(datum))
        return json.dumps(data)

