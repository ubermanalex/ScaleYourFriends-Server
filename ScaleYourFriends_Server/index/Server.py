'''
Created on 17 Jun 2013

@author: Alex
'''
import pdb
import sys,thread
from libavg import *
#import listnode
import databases
from twisted.internet import reactor
from twisted.python import log
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

global hostip,g_idindex
g_idindex = 0
hostip = "ws://localhost:9034"

##SERVER

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
        ips.dropConnection(self.peer.host) ##Drop Connection out of IPStorage when Client disconnects
        #ips.updateAll("Client with IP "+self.peer.host+" has disconnected")#Update all
        
    def onOpen(self):
        #TODO:UNCOMMENT
        #for user in userdb: ##check if userip already exists
        #    if self.peer.host == user.userip:
        #        self.sendMessage("USEREXI"+user.username)
        #        return 0
        ips.addNewClient(self.peer.host, self) ##adds current Connection and Client IP to the Storage
        #ips.updateAll("New Client with IP "+self.peer.host+" has joined")
        
    def onMessage(self, msg, binary):
        print "received:", msg ##print incoming message
                    
        ##add user
        
        if (msg[0:10] == 'USERNAME: '):
            msglen = len(msg)
            usern = msg[10:]
            for user in userdb:
                if user.username.upper() == usern.upper():
                    self.sendMessage('NAMUSED')
                    return 0
            userdb.addUser(userdb.getlen(),self.peer.host,usern)
            self.sendMessage('USERADD')
            print msg[10:msglen], "connected"
            
        ##add group

        if (msg[0:7] == 'GROUP: '):
            msglen = len(msg)
            msg = msg.replace(" ","")   #deletes spaces
            group = msg[6:].split('##')
            name = group[0]
            master = userdb.getUser(group[1])
            global g_idindex
            master.groups.append(g_idindex)
            users = [master]
            notfound = []   #users that havnt been found in database
            i = 2
            while i < len(group):   #create usersarray
                x = True
                for user in users: #checks if user already in users
                    if group[i] == user.username:
                        x = False
                        break
                if x:
                    user = userdb.getUser(group[i])
                    if user == 0:
                        notfound.append(group[i])
                        i+=1
                        continue
                    users.append(user)
                    user.groups.append(g_idindex)   #add group to users
                i+=1
                
            notfoundstr = ""
            y = False
            for user in notfound:
                notfoundstr += user+'##'
                y = True
                
            if y:
                notfoundstr = notfoundstr[:-2]
            self.sendMessage('NOTFOUN'+notfoundstr)
            groupdb.addGroup(g_idindex, name, master, users)           
            g_idindex += 1
            for user in users:
                self.sendgroups(user.u_ip)
            
            #for group in groupdb:
            #    print "GROUP",group.toStr()
            #for user in userdb:
            #    print "USER",user.toStr()
        
        ##add round
        
        if (msg[0:7] == 'ROUND: '):
            msglen = len(msg)
            users = msg[7:msglen].split('##')
            groupid = int(users[0])
            
            users = []
            i = 1
            while i < len(group):   #create usersarray
                user = userdb[int(users[i])]
                if not(groupid in user.groups):     #antihack
                    return 0
                users.append(user)
                i+=1
                
            groupdb[groupid].round = databases.Round(users)

        if (msg[0:10] == 'MYGROUPS: '):
            self.sendgroups(self.peer.host)
                
        if (msg[0:11] == 'THISGROUP: '):
            print msg[11:]
            groupname = msg[11:]
            group = groupdb.getGroup(groupname)
            user = userdb.getUserByIP(self.peer.host)
            if not(group.validUser(user.u_id)):
                return 0
            
            push = "MYGROUP"
            
            for player in group.users:
                push += player.username + '##'
            
            push += groupname + '##'
            
            if group.master.username == user.username:
                push += 'M'
            else:
                push += 'U'
            self.sendMessage(push)
        
        if (msg[0:10] == 'DELGROUP: '):
            groupname = msg[10:]
            group = groupdb.getGroup(groupname)
            if group.master.u_ip == self.peer.host:
                for user in group.users:
                    user.groups.remove(group.g_id)
                    ip = user.u_ip
                    ips.getConnectionForIp(ip).sendMessage('DELGROU'+groupname)
                groupdb.removeGroup(group.name)
            
        if (msg[0:9] == 'DELUSER: '):
            groupname = msg[9:]
            group = groupdb.getGroup(groupname)
            user = userdb.getUserByIP(self.peer.host)
            group.users.remove(user)
            user.groups.remove(group.g_id)
            self.sendMessage('DELUSER'+groupname)
            
        if (msg[0:10] == 'KICKUSER: '):
            groupanduser = msg[10:]
            groupanduser = groupanduser.split('##')
            groupname = groupanduser[0]
            username = groupanduser[1]
            group = groupdb.getGroup(groupname)
            if not(self.peer.host == group.master.u_ip):
                return 0
            user = userdb.getUser(username)
            if user == 0:
                self.sendMessage('NOKICKU'+username)
                return 0
            group.users.remove(user)
            user.groups.remove(group.g_id)
            ips.getConnectionForIp(user.u_ip).sendMessage('KICUSER'+groupname)
            
    def sendgroups(self,ip):
        user = userdb.getUserByIP(ip)
        print "USER",user.toStr()    
        push = "MGROUPS"
            
        for groupid in user.groups:
            group = groupdb.getGroupByID(groupid)
            if group.validUser(user.u_id):
                push += group.name + '##' + group.master.username + '!#!'
                print "PUSH",push
        if len(push) > 7:
            ips.getConnectionForIp(ip).sendMessage(push[:-3])
        else:
            ips.getConnectionForIp(ip).sendMessage(push)
            
class libAvgAppWithRect (AVGApp): ##Main LibAVG App that uses WebSockets
    def __init__(self): ##Create one WordsNode for the Text and RectNode to send to a certain Client and set player, canvas,..

        self.player=avg.Player.get()
        self.canvas=self.player.createMainCanvas(size=(175,60))
        self.rootNode=self.canvas.getRootNode()

        self.textsyf =avg.WordsNode(pos=(10,10),parent=self.rootNode,color="FFFFFF",text="Scale Your Friends")
        self.textsyf =avg.WordsNode(pos=(60,25),parent=self.rootNode,color="FFFFFF",text="Server")
        

        thread.start_new_thread(self.initializeWebSocket, ()) ##start the WebSocket in new Thread        
                      
    def initializeWebSocket(self):##Starts the WebSocket
        log.startLogging(sys.stdout)##Create a logfile (not necessary)
        self.factory = WebSocketServerFactory(hostip, debug = False)
        self.factory.protocol = EchoServerProtocol ##assign our Protocol to send/receive Messages
        listenWS(self.factory)
        
        reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading

             
         
if __name__ == '__main__':
    rcv=libAvgAppWithRect()
    ips=IPStorage()
    groupdb = databases.GroupDatabase()
    userdb = databases.UserDatabase()
    rcv.player.play()