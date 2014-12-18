class MessageType(object):
    REG = 1

class Message(object):
    def __init__(self):
        self.type = None
        self.body = None

    def get_type(self):
        return self.type

    def get_body(self):
        return self.body

    def set_type(self, type):
        self.type = type

    def set_body(self, body):
        self.body = body
