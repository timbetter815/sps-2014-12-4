import SocketServer  
from SocketServer import StreamRequestHandler as SRH  
from time import ctime
from processor import Processor
  
host = '127.0.0.1'  
port = 9999  
addr = (host,port)  
  
class Servers(SRH):
    def handle(self):  
        self.processor = Processor()
        print 'got connection from ',self.client_address  
        while True:
            data = self.request.recv(1024) 
            if not data:
                break
            result = self.processor.process_message(data)
            self.request.send(str(result))

print 'server is running....'  
server = SocketServer.ThreadingTCPServer(addr, Servers)  
server.serve_forever()  
