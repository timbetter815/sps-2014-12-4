from socket import *
from message import Message, MessageType

host = '127.0.0.1'  
port = 9999  
bufsize = 1024  
addr = (host,port)  
client = socket(AF_INET,SOCK_STREAM)  
client.connect(addr)

m = {\
     "type":MessageType.REG,\
     "body":{\
             "sps_agent_ip":"10.10.10.10",\
             "sps_agent_port":"99999",\
             "certificate_type":"PKCS#11",\
             "certificate_value":"XXXXX",\
            }\
    }
client.send(str(m))
result = client.recv(1024)
print result
client.close()
