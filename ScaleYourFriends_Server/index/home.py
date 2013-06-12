'''
Created on 10 Jun 2013

@author: Alex
'''

from libavg import avg,AVGApp
import sys,thread
 
from twisted.internet import reactor
from twisted.python import log
 
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

###THIS CLASS SIMPLY HOLDS THE CONNECTED CLIENT IPS####
class IPStorage():
    def __init__(self):
        self._ipList=dict({})
        
    def addNewClient(self,ip,connection): ##adds a new Client to the Dictionary
        self._ipList[ip]=connection 
    
    def dropConnection(self,ip):##removes Connection out of Dict
        del self._ipList[ip]
        
    def getAllCurrentConnections(self):#returns all currently active Connections
        return self._ipList
    
    def getConnectionForIp(self,ip):##returns a Connection to a Client with a certain IP
        return self._ipList[ip]
    
    def updateAll(self,msg): #sends Message to all connected Clients
        for key in self._ipList:
            self._ipList[key].sendMessage(msg)
        

###WEBSOCKETPROTOCOL USED FOR COMMUNICATION####
class EchoServerProtocol(WebSocketServerProtocol):
    
    def onClose(self,wasClean,code,reason):
        print "Client left"
        ips.dropConnection(self.peer.host) ##Drop Connection out of IPStorage when Client disconnects
        ips.updateAll("Client with IP "+self.peer.host+" has disconnected")#Update all
        
    def onOpen(self):
        ips.addNewClient(self.peer.host, self) ##adds current Connection and Client IP to the Storage
        ips.updateAll("New Client with IP "+self.peer.host+" has joined")
              
    def onMessage(self, msg, binary):
        print "sending echo:", msg ##print incoming message
        userarray.append(msg)
        self.sendMessage(msg)##send back message to initiating client
        
        

class libAvgAppWithRect (AVGApp): ##Main LibAVG App that uses WebSockets
    def __init__(self): ##Create one WordsNode for the Text and RectNode to send to a certain Client and set player, canvas,..
        self.player=avg.Player.get()
        self.canvas=self.player.createMainCanvas(size=(600,480))
        self.rootNode=self.canvas.getRootNode()
        self.text=avg.WordsNode(pos=(200,140),parent=self.rootNode,color="ffffff",text="")
        self.rectWhite=avg.RectNode(size=(200,200),pos=(200,140),parent=self.rootNode,color="ffffff",fillcolor="ffffff", fillopacity=1)
        self.rectWhite.connectEventHandler(avg.CURSORDOWN, avg.MOUSE, self.rectWhite, self.onWhiteRectClick)
        thread.start_new_thread(self.initializeWebSocket, ()) ##start the WebSocket in new Thread
        
            
    def onWhiteRectClick(self,event):##send Message "Hello there" to First Client in IPStorage
        if (ips.getAllCurrentConnections()):
            ips.getAllCurrentConnections()[ips.getAllCurrentConnections().keys()[0]].sendMessage("Hello there")
        
            
    def initializeWebSocket(self):##Starts the WebSocket
        log.startLogging(sys.stdout)##Create a logfile (not necessary)
        self.factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
        self.factory.protocol = EchoServerProtocol ##assign our Protocol to send/receive Messages
        listenWS(self.factory)
        reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading
        
            
if __name__ == '__main__':
    rcv=libAvgAppWithRect()
    ips=IPStorage()
    userarray = [];
    rcv.player.play()