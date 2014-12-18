from format import Format
from message import MessageType
from random import randint

class Processor(object):
    def __init__(self):
        pass
    
    def process_message(self, data):
        m = Format.format(data)
        m_type = m.get_type()
        body = m.get_body()
        cert = "123456"
        if self.identify(cert): 
            if m_type == MessageType.REG:
                result = self.register(body)
            if m_type == MessageType.STRA:
                result = self.process_strategy(body)
            return result

    def identify(self, cert):
        return True

    def register(self, body):
        uuid = self.create_uuid()
        agent_ip = body['sps_agent_ip']
        agent_port = body['sps_agent_port']
        cert_type = body['certificate_type']
        cert_value = body['certificate_value']
        info = (uuid, agent_ip, agent_port, cert_type, cert_value)
        self.sync_ckm(info)
        if self.sync_database(info):
            return {'return':'success', 'sps_agent_uuid':uuid}

    def create_uuid(self):
        uuid = randint(1, 1000)
        return uuid

    def sync_ckm(self, info):
        print "send info %s to ckm success" % str(info)
        return True

    def sync_database(self, info):
        print "write %s to database success" % str(info)
        return True

    def process_strategy(self, body):
        vm_uuid = body['vm_uuid']
        vm_info = self.get_info_from_nova(vm_uuid)
        self.get_strategy_from_database()
        self.send_info_to_ckm()
        strategy = self.packet_strategy()
        return strategy
