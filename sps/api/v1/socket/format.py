from message import Message, MessageType

class Format(object):
    def __init__(self):
        pass
      
    @classmethod
    def format(cls, data):
        info = eval(data)
        m = Message()
        type = info['type']
        body = info['body']
        m.set_type(type)
        m.set_body(body)
        return m
