'''
Created on 12.06.2013

@author: Alex
'''

'''
PYSENDTOGGLE
einkommentieren fuer pyclient tests
auskommentieren fuer handyapp tests
'''

import sys,thread
import time
from libavg import *
#import listnode
import databases
from twisted.internet import reactor
from twisted.python import log
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
global clicked
clicked = False
global hostip, pysend, pysend2, pyclient, sendpermission, pointgrow
#pyend := string of top7 songs
#pysend2 := string of top3 users
#pyclient := ip of pyclient
#sendpermission := sendpermission for pyclient 
#pointgrow := list of users who
hostip = "ws://localhost:9034"
pointgrow = []

##LISTNODE
##TODO:Auslagern
##TODO:in Datei speicher, lesen
##TODO:immer checken, ob pyclient noch connectet ist, wenn er sendet

###scrollable list of WordsNodes###

class ListNode(avg.DivNode):

    def __init__ (self, idindex, slist, scount, **kwargs):
        super(ListNode, self).__init__(**kwargs)
        
        self.slist  = []
        
        for string in slist:
            self.slist.append(string)
         
        self.scount = scount
        
        self.window = avg.DivNode(id=listwindowid, size=(300, 20), pos =(0,0), parent= self)
        self.i = 0
        self.idindex = idindex
        self.p = 0 
        self.node = slist
        for string in slist:
            
            self.node[self.i] = avg.WordsNode(id = str(self.idindex), text= str(string), color="FFFFFF", pos=(5,self.p), parent=self.window)
            self.node[self.i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
            self.p = self.p+20
            self.idindex = self.idindex+1
            self.i = self.i +1
            
            
        self.captureHolder = None
        self.dragOffsetY = 0
        self.dragOffsetX = 0
        self.setEventHandler(avg.CURSORDOWN, avg.MOUSE | avg.TOUCH, self.startScroll)
        self.setEventHandler(avg.CURSORMOTION, avg.MOUSE | avg.TOUCH, self.doScroll)
        self.setEventHandler(avg.CURSORUP, avg.MOUSE | avg.TOUCH, self.endScroll)
        self.setEventHandler(avg.CURSOROUT, avg.MOUSE | avg.TOUCH, self.outofDiv)
        self.SelectedString = ""
        self.node_old = idindex
        self.current_event = None
    
    #method to call when a WordsNode is clicked
    def click(self, event):
        self.current_event = event
        self.selectString()
    
    #selects (highlights) the clicked WordsNode
    def selectString(self):
        event = self.current_event
        if (event.node.id != self.node_old):
            
            if self.node_old >= 0:
                nodeid = rcv.player.getElementByID(str(self.node_old))      
                nodeid.color = "FFFFFF"
            
            if (int(event.node.id) < 5000):
            
                event.node.color = "F4FA58"
            
                rcv.rectadd.color="2EFE2E"
                rcv.rectrej1.color="FE9A2E"
                rcv.rectrej2.color="FE642E"
                rcv.rectrej3.color="FE2E2E"
                rcv.rectblockuser.color="FF0000"
                rcv.rectadd.fillcolor="58FA58"
                rcv.rectrej1.fillcolor="FAAC58"
                rcv.rectrej2.fillcolor="FA8258"
                rcv.rectrej3.fillcolor="FA5858"
                rcv.rectblockuser.fillcolor="FE2E2E"
                rcv.textadd.color="088A08"
                rcv.textrej1.color="8A4B08"
                rcv.textrej2.color="8A2908"
                rcv.textrej3.color="8A0808"
                rcv.textblockuser.color="8A0808"
            
        
        else:
            pass
        
        
        self.node_old = event.node.id
        
        
        
    #adds a WordsNode
    
    def addEle(self, elem):
        i = len(self.slist)
        
        self.node.append("")
        self.slist.append(elem)
        node =  avg.WordsNode(id = str(self.idindex), text= str(elem), color="FFFFFF", pos=(5,self.p), parent=self.window)
        self.node[i] = node
        self.node[i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        
        self.idindex+=1
        self.p = self.p+20
        
        self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y + 20))
        
    #removes a WordsNode
                      
    def removEle(self):
        
        #checks if DJ is allowed to remove the WordsNode (if song-handle buttons are not grey)
        if (rcv.rectadd.color=="A4A4A4"):
            return 0
        
        event = self.current_event
        e = rcv.player.getElementByID(str(event.node.id))
        counter = int(event.node.id)+1
        iterend = len(self.node)
        
        rettext = e.text
        
        self.node.remove(e)
        self.window.removeChild(e)
        self.slist.remove(e.text)
        
        #closes the occured gap by propagating the list elements below the removed one a slot up
        while counter < iterend:
            f = rcv.player.getElementByID(str(counter))
            
            (x,y) = f.pos
            y -= 20
            c = f.color
            t = f.text
        
            self.window.removeChild(f)
            self.node[counter-1] = avg.WordsNode(id = str(counter-1), text= t, color=c, pos=(x,y), parent=self.window)
            self.node[counter-1].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
            
            counter+= 1
            
        self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y - 20))
        
        #colors buttons grey again
        rcv.rectadd.color="A4A4A4"
        rcv.rectrej1.color="A4A4A4"
        rcv.rectrej2.color="A4A4A4"
        rcv.rectrej3.color="A4A4A4"
        rcv.rectblockuser.color="A4A4A4"
        rcv.rectadd.fillcolor="BDBDBD"
        rcv.rectrej1.fillcolor="BDBDBD"
        rcv.rectrej2.fillcolor="BDBDBD"
        rcv.rectrej3.fillcolor="BDBDBD"
        rcv.rectblockuser.fillcolor="BDBDBD"
        rcv.textadd.color="424242"
        rcv.textrej1.color="424242"
        rcv.textrej2.color="424242"
        rcv.textrej3.color="424242"
        rcv.textblockuser.color="424242"
        
        #checks if list is empty after removal
        self.current_event = None
        if len(self.slist) == 0:
            self.node_old = -1
        else:
            self.node_old = 0
        self.p = self.p-20
        
        self.idindex -= 1
        
        #returns removed song to caller
        return rettext
    
    #updates list with given songlist
    def update(self, songlist, idindex):
        self.window.pos = avg.Point2D(0,0)
        i = 0
        idind = idindex
        lsl = len(self.slist)
        while i < len(self.slist):
            e = rcv.player.getElementByID(str(idind))
            e.text = ""
            i = i + 1
            idind += 1
        p = 0
        s = 0
        ii = 0
        iidind = idindex
        node = songlist
        l1 = songlist[0:lsl-1]
        l2 = songlist[lsl:len(songlist)-1]
        if len(songlist) < lsl:
            for string in l1:
                e = rcv.player.getElementByID(str(iidind))
                e.text = string
                ii = ii +1
                iidind += 1
                p = p+20
            while s < (lsl - len(songlist)):
                self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y - 20))
                s = s+1
        elif len(songlist) > lsl:
            for string in l1:
                e = rcv.player.getElementByID(str(iidind))
                e.text = string
                ii = ii +1
                iidind += 1
                p = p+20
            for string in l2:
                ii = ii +1
                iidind += 1
                node[ii] = avg.WordsNode(id = str(iidind), text= str(string), color="79CDCD", pos=(5,p), parent=self.window)
                node[ii].setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.selectString)
                self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y + 20))
                p = p+20
        else:
            for string in songlist:
                e = rcv.player.getElementByID(str(iidind))
                e.text = string
                ii = ii +1
                iidind += 1
        self.slist = songlist

    #makes list scrollable
    def startScroll(self, event):
        if self.captureHolder is None:
            self.captureHolder = event.cursorid
            self.dragOffsetY = self.window.pos.y - event.pos.y
            self.dragOffsetX = self.window.pos.x - event.pos.x
    
    def doScroll(self, event):
        if self.window.size.y > event.node.size.y:
            if event.cursorid == self.captureHolder:
                self.window.pos = avg.Point2D(self.window.pos.x, event.pos.y + self.dragOffsetY)
        if self.window.size.x > event.node.size.x:
            if event.cursorid == self.captureHolder:
                self.window.pos = avg.Point2D(event.pos.x + self.dragOffsetX, self.window.pos.y)
                
    def endScroll(self, event):
        if event.cursorid == self.captureHolder:
            self.captureHolder = None
        if self.window.pos.y >=  self.size.y -20:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, self.size.y -21, 50, 1000)
                anim.start()
        if self.window.pos.y + self.window.size.y - 20 <=  -1:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, 20 - self.window.size.y, 50, 1000)
                anim.start()
    
    #avoids that list can disappear completely by scrolling
    
    def outofDiv(self, event):
        self.captureHolder = None
        if self.window.pos.y >=  self.size.y -20:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, self.size.y -21, 50, 1000)
                anim.start()
        if self.window.pos.y + self.window.size.y - 20 <=  -1:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, 20 - self.window.size.y, 50, 1000)
                anim.start()

###IPStorage holds the connected client ips####
class IPStorage():
    def __init__(self):
        self._ipList=dict({})
    
    #adds a new client to the dictionary
    def addNewClient(self,ip,connection):
        self._ipList[ip]=connection 
        
    #removes connection out of dictionary
    def dropConnection(self,ip):
        del self._ipList[ip]
    
    #returns all currently active connections
    def getAllCurrentConnections(self):
        return self._ipList
    
    #returns a connection to a client with a certain IP
    def getConnectionForIp(self,ip):
        return self._ipList[ip]
    
    #sends message to all connected clients
    def updateAll(self,msg):
        for key in self._ipList:
            self._ipList[key].sendMessage(msg)
        

###websocket for communication###
class EchoServerProtocol(WebSocketServerProtocol):
    
    #method called when someone connects        
    def onOpen(self):
        #TODO: ???
        if self.peer.host == pyclient:
            return 0
        
        #checks if user already exists, if so user receives his stats
        for user in userdb:
            if self.peer.host == user.userip:
                self.sendMessage("USEREXI"+user.username)
                self.sendMessage("ACTVOTE"+str(user.numberofvotes))
                if user.song1.interpret == "LE##ER" and user.song2.interpret == "LE##ER":
                    x = 2
                elif user.song1.interpret == "LE##ER" or user.song2.interpret == "LE##ER":
                    x = 1
                else:
                    x = 0
                self.sendMessage("ACTSUGG"+str(x))
                self.sendMessage("POINTCO"+str(user.numberofpoints))
                self.sendMessage("SONGDB1"+songdb.tostring())
                
                #TODO:deletable?
                #ips.addNewClient(self.peer.host, self) ##adds current Connection and Client IP to the Storage
                #ips.updateAll("New Client with IP "+self.peer.host+" has joined")
                ips.dropConnection(self.peer.host) ##Drop Connection out of IPStorage when Client disconnects
                ips.addNewClient(self.peer.host, self) ##adds current Connection and Client IP to the Storage
                return 0
        
        #adds new client if user doesn't exist
        ips.addNewClient(self.peer.host, self)
    
    #parses message received
    def onMessage(self, msg, binary):
        
        #a pyclient tries to connect
        if (msg[0:10] == 'PYCLIENT: '):
            msglen = len(msg)
            global pyclient
            if pyclient == 0: #pyclient final
                pyclient = self.peer.host
            
        #a user tries to connect
        if (msg[0:10] == 'USERNAME: '):
            msglen = len(msg)
            usern = msg[10:msglen]
            for user in userdb: #checks if username is already used
                if user.username.upper() == usern.upper():
                    self.sendMessage('NAMUSED')
                    return 0
            self.sendMessage('NAMFREE')
            userdb.addUser(userdb.getlen(),self.peer.host,msg[10:msglen],0,3) #adds user to userdb
            user = userdb.getUserByName(usern)
            self.sendMessage('SONGDB1'+songdb.tostring()) #sends songdb to user
            
        ##adds song to requestlist
        if (msg[0:6] == 'SONG: '):
            msglen = len(msg)
            songelems = msg[6:msglen].split('##')
            interpret = songelems[0]
            songtitle = songelems[1]
            
            testinterpret = interpret.upper()
            testsongtitle = songtitle.upper()
            
            
            #checks if song already in songdb or requestlist
            for song in songdb.database:
                interp = song.interpret.upper()
                songtit = song.songtitle.upper()
                if interp == testinterpret and testsongtitle == songtit:
                    push = "SONGIND"+song.interpret+" - "+song.songtitle
                    self.sendMessage(str(push))
                    return 0
                
            for song in requestlist.slist:
                intandtit = song.split(' / ')
                interp = intandtit[1].upper()
                songtit = intandtit[2].upper()
                if interp == testinterpret and testsongtitle == songtit:
                    push = "SONGINP"+intandtit[1]+" - "+intandtit[2]
                    self.sendMessage(str(push))
                    return 0
            
            for song in rejdb.database:
                interp = song.interpret.upper()
                songtit = song.songtitle.upper()
                if interp == testinterpret and testsongtitle == songtit:
                    push = "SONGINR"+song.interpret+" - "+song.songtitle
                    self.sendMessage(str(push))
                    return 0
            
            #updates user's suggestioncounter
            for userobj in userdb:
                if (userobj.username == songelems[2]):
                    if (userobj.song1.interpret == "LE##ER"):
                        userobj.song1.interpret = interpret
                        userobj.song1.songtitle = songtitle
                        userobj.song1.status = 0
                        if (userobj.song2.interpret == "LE##ER"):
                            self.sendMessage('ACTSUGG1')
                        else:
                            self.sendMessage('ACTSUGG0')
                    elif (userobj.song2.interpret == "LE##ER"):
                        userobj.song2.interpret = interpret
                        userobj.song2.songtitle = songtitle
                        userobj.song2.status = 0
                        if (userobj.song1.interpret == "LE##ER"):
                            self.sendMessage('ACTSUGG1')
                        else:
                            self.sendMessage('ACTSUGG0')
                    else:
                        self.sendMessage('MAXSONG')
                        return 0
            
            #print userdb.getUser(interpret,songtitle).username,"schlaegt '",interpret,"/",songtitle,"' vor"
            
            #adds requested song to requestlist
            rcv.player.setTimeout(0, lambda : requestlist.addEle(str(len(requestlist.node)+1)+" / "+interpret+" / "+songtitle))
            
        #applies vote
        if (msg[0:6] == 'VOTE: '):
            msglen = len(msg)
            userandsong = msg[6:msglen].split('##')
            user = userandsong[0]
            interpret = userandsong[1]
            songtitle = userandsong[2]
            
            userdblen = userdb.getlen()
            songdblen = songdb.getlen()
            for i in range(0,userdblen): #searches user who voted in userdb
                if (user == userdb[i].username): 
                    if (userdb[i].numberofvotes == 0): #checks if user still has votes
                        self.sendMessage('MAXVOTE'+str(rcv.timer.text))
                        return 0
                    x = True
                    for song in songdb: #checks if song exists in songdb
                        if song.interpret == interpret and song.songtitle == songtitle:
                            x = False
                            break
                    if x: #cancels if song doesn't exist
                        return 0
                    userdb[i].numberofvotes -= 1
                    self.sendMessage('ACTVOTE'+str(userdb[i].numberofvotes)) #updates user's votecounter
                    userdb[i].votedfor.append(interpret+'##'+songtitle) #applies song to user.votedfor
                    break
                
            for i in range(0,songdblen): #searches song in songdb
                if (songtitle == songdb[i].songtitle and interpret == songdb[i].interpret): 
                    songdb[i].numberofvotes += 1
                    j = i-1
                    k = i
                    while j>=0: ##sorts songarray
                        if (songdb[k].numberofvotes <= songdb[j].numberofvotes):
                            break
                        songdb[j].interpret,songdb[k].interpret = songdb[k].interpret,songdb[j].interpret
                        songdb[j].songtitle,songdb[k].songtitle = songdb[k].songtitle,songdb[j].songtitle
                        songdb[j].numberofvotes,songdb[k].numberofvotes = songdb[k].numberofvotes,songdb[j].numberofvotes
                        songdb[j].fromuser,songdb[k].fromuser = songdb[k].fromuser,songdb[j].fromuser
                        
                        j -= 1
                        k -= 1
                    break
            
            #sends songdb to all clients
            for user in userdb:
                ips.getConnectionForIp(user.userip).sendMessage('SONGDB1'+songdb.tostring());
             
            #updates top7 list on DJ's screen
            topseven.update(songdb.tolist(),5000)
            
            #updates pysend
            x = songdb.tolist()
            global pysend
            pysend = ""
            for y in x:
                a = y.split(' / ')
                if len(a)==1:
                    pysend+=' ## ##0!#!'
                else:
                    pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'
                        
            pysend = pysend[0:len(pysend)-3]
            
###DjApp that uses websockets###
            
class libAvgAppWithRect (AVGApp):
    
    #sends current top7 songs to pyclient every 30seconds
    def sendtopy(self):
        if not(sendpermission): #if not permitted to send, do nothing
            time.sleep(30)
            self.sendtopy()
        global pysend, pyclient
        x = pyclient
        #TODO:PYSENDTOGGLE
        ips.getConnectionForIp(x).sendMessage('PYMESG'+pysend)
        #print "sending to pyclient:",pysend
        time.sleep(30)
        self.sendtopy()
    
    #method called when clicked on button "START"
    def clickstart(self,events):
        thread.start_new_thread(self.countdown,(0,10)) #initializes and starts countdown
        global pyclient,pysend,pysend2
        x = pyclient
        #TODO:PYSENDTOGGLE
        #ips.getConnectionForIp(x).sendMessage('PYMESG'+pysend) #sends top7 songs to pyclient
        #ips.getConnectionForIp(x).sendMessage('PYMESG'+pysend2) #sends top3 users to pyclient
        ips.getConnectionForIp(x).sendMessage("START") #sends start command to pyclient
        rcv.divstart.removeChild(self.textstart)
        rcv.divstart.removeChild(self.rectstart)
        rcv.rootNode.removeChild(self.divstart)
        #TODO:PYSENDTOGGLE
        thread.start_new_thread(self.sendtopy,()) #starts updating pyclient every 30 seconds
    
    #called when dj blocks a user or presses "top 3 played"
    #asks dj to confirm his action
    def confirm(self,x):
        global clicked
        if clicked:
            return 0
        clicked = True
        #changes lefthand buttons
        rcv.rectrej1.fillopacity=0
        rcv.rectrej1.opacity=0
        rcv.textrej1.opacity=0
        
        rcv.rectblockuser.fillopacity=0
        rcv.rectblockuser.opacity=0
        rcv.textblockuser.opacity=0
        
        self.divask = avg.DivNode(id = "ask",pos=(30,125),size=(250,150),parent=self.rootNode)
        self.divyes = avg.DivNode(id = "yes",pos=(30,215),size=(250,150),parent=self.rootNode)
        self.divno = avg.DivNode(id = "no",pos=(30,260),size=(250,150),parent=self.rootNode)
        
        self.rectask = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divask,color="2EFE2E",fillcolor="58FA58", fillopacity=1)
        self.rectyes = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divyes,color="FE642E",fillcolor="FA8258", fillopacity=1)
        self.rectno = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divno,color="FE2E2E",fillcolor="FA5858", fillopacity=1)
        
        self.textask = avg.WordsNode(pos=(10,5),parent=self.divask,color="088A08",text="Bist Du dir sicher?")
        self.textyes = avg.WordsNode(pos=(10,5),parent=self.divyes,color="8A2908",text="Ja")
        self.textno = avg.WordsNode(pos=(10,5),parent=self.divno,color="8A0808",text="Nein")
            
        self.divno.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.no)
        if x == 1: #if argument was 1, user gets blocked, when "yes" is clicked
            self.divyes.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click3s)
        if x == 0: #if argument was 0, top3 is played, when "yes" is clicked
            self.divyes.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click2s)
            
    #called when dj clicks on "User blockieren"
    def click3(self,events):
        if (rcv.rectadd.color=="A4A4A4"):   #checks if dj selected a songsuggest
                return 0
        self.confirm(1) #asks dj to confirm his action
    
    #cancels dj action, normalizes lefthand buttons
    def no(self,events):
        
            global clicked
            clicked = False
            
            rcv.rootNode.removeChild(self.divask)
            rcv.rootNode.removeChild(self.divno)
            rcv.rootNode.removeChild(self.divyes)

            rcv.rectrej1.fillopacity=1
            rcv.rectrej1.opacity=1
            rcv.textrej1.opacity=1
        
            rcv.rectblockuser.fillopacity=1
            rcv.rectblockuser.opacity=1
            rcv.textblockuser.opacity=1
    
    #blocks a user
    def click3s(self,events):
        
            global clicked
            clicked = False
            
            #normalizes lefthand buttons
            rcv.rootNode.removeChild(self.divask)
            rcv.rootNode.removeChild(self.divno)
            rcv.rootNode.removeChild(self.divyes)

            rcv.rectrej1.fillopacity=1
            rcv.rectrej1.opacity=1
            rcv.textrej1.opacity=1
        
            rcv.rectblockuser.fillopacity=1
            rcv.rectblockuser.opacity=1
            rcv.textblockuser.opacity=1
            
            text = requestlist.removEle() #removes song from requestlist
            newsong = text.split(' / ')
            interpret = newsong[1]
            songtitle = newsong[2]
            user = userdb.getUser(interpret,songtitle)
            receiver = user.userip
            print user.username, "blockiert."
            #blocks user's songs
            user.song1.interpret = "BLO##CKED"
            user.song1.songtitle = "BLO##CKED"
            user.song2.interpret = "BLO##CKED"
            user.song2.songtitle = "BLO##CKED"
            push = "SONGBLO"+interpret+" - "+songtitle
            ips.getConnectionForIp(receiver).sendMessage(str(push)) #tells user he was blocked for his suggestion
                
    #called when dj clicks "top 3 played"
    def click2(self,events):
        if (rcv.rectsongplayed.color=="A4A4A4"): #checks if dj is allowed to call "top 3 played"
                return 0
            
#        if songdb.getlen() == 0: #if songdb is empty, do nothing
#                rcv.rectsongplayed.fillcolor="BDBDBD"
#                rcv.rectsongplayed.color="A4A4A4"
#                rcv.textsongplayed.color="424242"
#                rcv.textsongplayed2.color="424242"
#                rcv.textsongplayed3.color="424242"
#                rcv.textsongplayed4.color="424242"
#                rcv.textsongplayed.text="Top 1"
#                rcv.textsongplayed2.text="Top 2"
#                rcv.textsongplayed3.text="Top 3"
#                return 0
        self.confirm(0) #asks dj to confirm his action
            
    #resets top3 songs, gives points to suggesters            
    def click2s(self,events):
            
            global clicked
            clicked = False
            
            #normalizes lefthand buttons
            rcv.rootNode.removeChild(self.divask)
            rcv.rootNode.removeChild(self.divno)
            rcv.rootNode.removeChild(self.divyes)

            rcv.rectrej1.fillopacity=1
            rcv.rectrej1.opacity=1
            rcv.textrej1.opacity=1
        
            rcv.rectblockuser.fillopacity=1
            rcv.rectblockuser.opacity=1
            rcv.textblockuser.opacity=1

            global pointgrow
            for user in pointgrow: #send every user who got points a message with his pointgrowth and total points
                userobj = userdb.getUserByName(user[2])
                if (userobj.song1.interpret=="BLO##CKED"): #doesn't send pointgrowth to blocked users
                    continue
                push = "POINTGR"+str(user[1]) #pointgrowth
                ips.getConnectionForIp(user[0]).sendMessage(push)
                ips.getConnectionForIp(user[0]).sendMessage('POINTCO'+str(user[3])) #current total points
            
            #sort users
            userdb.database = userdb.mergeSortc()
            
            #updates pysend2
            global pysend2
            pysend2 = ""
            i = 0
            while i < 3:
                if i >= userdb.getlen():
                    pysend2 += ' ##0!#!'
                else:
                    pysend2 += userdb[i].username+'##'+str(userdb[i].numberofpoints)+'!#!'
                i+=1
            pysend2 = pysend2[0:len(pysend2)-3]
            
            #updates topseven list on dj screen
            topseven.update(songdb.tolist(),5000)
            
            #update pysend
            x = songdb.tolist()
            global pysend
            pysend = ""
            for y in x:
                a = y.split(' / ')
                if len(a)==1:
                    pysend+=' ## ##0!#!'
                else:
                    pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'
            pysend = pysend[0:len(pysend)-3]
            
            #updates pyclient with top7 songs and top3 users
            global pyclient
            x = pyclient
            #TODO:uncomment to send to pyclient, PLAYED
            #TODO:PYSENDTOGGLE
            ips.getConnectionForIp(x).sendMessage("PLAYED"+pysend)
            ips.getConnectionForIp(x).sendMessage('PYMESG'+pysend2)
        
            #allow sendpermission again
            global sendpermission
            sendpermission = True
            
            #send new songdb to all users
            for user in userdb:
                ips.getConnectionForIp(user.userip).sendMessage('SONGDB1'+songdb.tostring());
            
            #changes button color back to grey
            rcv.rectsongplayed.fillcolor="BDBDBD"
            rcv.rectsongplayed.color="A4A4A4"
            rcv.textsongplayed.color="424242"
            rcv.textsongplayed2.color="424242"
            rcv.textsongplayed3.color="424242"
            rcv.textsongplayed4.color="424242"
            rcv.textsongplayed.text="Top 1"
            rcv.textsongplayed2.text="Top 2"
            rcv.textsongplayed3.text="Top 3"
    
    #called when dj clicks on "Annehmen", "Abgelehnt - ..."
    def click(self,events):
            
            if (rcv.rectadd.color=="A4A4A4"): #checks if dj selected a song
                return 0
            text = requestlist.removEle()
            eventid = (events.node.id)
            newsong = text.split(' / ')
            interpret = newsong[1]
            songtitle = newsong[2]
            user = userdb.getUser(interpret,songtitle) #gets user who suggested the song
            if user == 0: #checks if user is blocked
                pass
            else:
                receiver = user.userip
                
            if eventid == "add": #if dj clicked on "Annehmen"
                print('Hinzugefuegt: '+text)
                newsong = text.split(' / ')
                
                if not(user == 0): #if user isn't blocked, add song to his songs
                
                    if (user.song1.status == 0 and user.song1.interpret == interpret and user.song1.songtitle == songtitle):
                        user.song1.interpret = interpret
                        user.song1.songtitle = songtitle
                        user.song1.status = 1
                    elif (user.song2.status == 0 and user.song2.interpret == interpret and user.song2.songtitle == songtitle):
                        user.song2.interpret = interpret
                        user.song2.songtitle = songtitle
                        user.song2.status = 1
                    else:
                        return 0
                            
                topsevenold = []
                for song in topsevenold:
                    topsevenold.append(song)
                
                #add song to songdb
                if user == 0: #if user is blocked, set fromuser to -1
                    songdb.addSong(interpret,songtitle,0,-1)
                else:
                    songdb.addSong(interpret,songtitle,0,user.userid)
                
                #if top7 changed    
                if (songdb.checktopseven(topsevenold)):
                    topseven.update(songdb.tolist(),5000) #update top7 songs on dj screen
                    x = songdb.tolist()
                    
                    #update pysend
                    global pysend
                    pysend = ""
                    for y in x:
                        a = y.split(' / ')
                        if len(a)==1:
                            pysend+=' ## ##0!#!'
                        else:
                            pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'
                        
                    pysend = pysend[0:len(pysend)-3]
                                
                push = "SONGADD"+interpret+" - "+songtitle
                if not(user == 0): #if user isn't block, tell him his song has been added
                    ips.getConnectionForIp(receiver).sendMessage(str(push))
                    
                #send new songdb to all users            
                for user in userdb:
                    ips.getConnectionForIp(user.userip).sendMessage('SONGDB1'+songdb.tostring());
            
            #if dj clicked on "Ablehnen - doppelt"                
            elif eventid == "rej1":
                print('Abgelehnt (doppelt): '+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[1],usersong[2])
                
                if not(userrej == 0): #if user isn't blocked, reset one suggestion
                    if userrej.song1.interpret == usersong[1] and userrej.song1.songtitle == usersong[2] and userrej.song1.status == 0:
                        userrej.song1.interpret = 'LE##ER'
                        userrej.song1.songtitle = 'LE##ER'
                        if userrej.song2.interpret == 'LE##ER' and userrej.song2.songtitle == 'LE##ER':
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG2')
                        else:
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG1')
                    if userrej.song2.interpret == usersong[1] and userrej.song2.songtitle == usersong[2] and userrej.song2.status == 0:
                        userrej.song2.interpret = 'LE##ER'
                        userrej.song2.songtitle = 'LE##ER'
                        if userrej.song1.interpret == 'LE##ER' and userrej.song1.songtitle == 'LE##ER':
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG2')
                        else:
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG1')
    
                    push = "SONGRE1"+interpret+" - "+songtitle
                    ips.getConnectionForIp(receiver).sendMessage(str(push)) #tell user his song has been rejected because it already is in songdb
                rejdb.addSong(interpret,songtitle,0,-1) #add song to rejected songs
                
            #if dj clicked on "Ablehnen - hab' ich nicht"
            elif eventid == "rej2":
                print("Abgelehnt (hab' ich nicht): "+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[1],usersong[2])
                
                if not(userrej == 0): #if user isn't blocked, reset one suggestion
                    if userrej.song1.interpret == usersong[1] and userrej.song1.songtitle == usersong[2] and userrej.song1.status == 0:
                        userrej.song1.interpret = 'LE##ER'
                        userrej.song1.songtitle = 'LE##ER'
                        if userrej.song2.interpret == 'LE##ER' and userrej.song2.songtitle == 'LE##ER':
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG2')
                        else:
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG1')
                    if userrej.song2.interpret == usersong[1] and userrej.song2.songtitle == usersong[2] and userrej.song2.status == 0:
                        userrej.song2.interpret = 'LE##ER'
                        userrej.song2.songtitle = 'LE##ER'
                        if userrej.song1.interpret == 'LE##ER' and userrej.song1.songtitle == 'LE##ER':
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG2')
                        else:
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG1')
                    
                    push = "SONGRE2"+interpret+" - "+songtitle
                    ips.getConnectionForIp(receiver).sendMessage(str(push)) #tell user his song has been rejected, because dj doesn't have it
                rejdb.addSong(interpret,songtitle,0,-1) #add song to rejected songs
            
            #if dj clicked on "Ablehnen - passt nicht"
            elif eventid == "rej3":
                print('Abgelehnt (unpassend): '+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[1],usersong[2])
                
                if not(user==0): #if user isn't blocked, reset one suggestion
                    if userrej.song1.interpret == usersong[1] and userrej.song1.songtitle == usersong[2] and userrej.song1.status == 0:
                        userrej.song1.interpret = 'LE##ER'
                        userrej.song1.songtitle = 'LE##ER'
                        if userrej.song2.interpret == 'LE##ER' and userrej.song2.songtitle == 'LE##ER':
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG2')
                        else:
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG1')
                    if userrej.song2.interpret == usersong[1] and userrej.song2.songtitle == usersong[2] and userrej.song2.status == 0:
                        userrej.song2.interpret = 'LE##ER'
                        userrej.song2.songtitle = 'LE##ER'
                        if userrej.song1.interpret == 'LE##ER' and userrej.song1.songtitle == 'LE##ER':
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG2')
                        else:
                            ips.getConnectionForIp(userrej.userip).sendMessage('ACTSUGG1')
                
                    push = "SONGRE3"+interpret+" - "+songtitle
                    ips.getConnectionForIp(receiver).sendMessage(str(push)) #tell user his song has been rejected, because dj thinks it doesn't match the theme of the evening
                
                rejdb.addSong(interpret,songtitle,0, -1) #adds song to rejected songs
    
    #initializes interface
    def __init__(self): 
        self.player=avg.Player.get()
        self.canvas=self.player.createMainCanvas(size=(620,350))
        self.rootNode=self.canvas.getRootNode()

        #RectNodes for "Annehmen", "Ablehnen - ..." and "User blockieren"
        self.rectadd = avg.RectNode(size=(250,30),pos=(30,125),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej1 = avg.RectNode(size=(250,30),pos=(30,170),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej2 = avg.RectNode(size=(250,30),pos=(30,215),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej3 = avg.RectNode(size=(250,30),pos=(30,260),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectblockuser = avg.RectNode(size=(250,30),pos=(30,305),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)

        #DivNodes for "Annehmen", "Ablehnen - ..." and "User blockieren"
        self.divadd = avg.DivNode(id = "add",pos=(30,125),size=(250,30),parent=self.rootNode)
        self.divrej1 = avg.DivNode(id = "rej1",pos=(30,170),size=(250,30),parent=self.rootNode)
        self.divrej2 = avg.DivNode(id = "rej2",pos=(30,215),size=(250,30),parent=self.rootNode)
        self.divrej3 = avg.DivNode(id = "rej3",pos=(30,260),size=(250,30),parent=self.rootNode)
        self.divblockuser = avg.DivNode(id = "blockuser",pos=(30,305),size=(250,30),parent=self.rootNode)
        
        #EventHandlers for "Annehmen", "Ablehnen - ..." and "User blockieren"
        self.divadd.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej1.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej2.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej3.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divblockuser.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click3)
        
        #WordsNodes for "Annehmen", "Ablehnen - ..." and "User blockieren"
        self.textadd =avg.WordsNode(pos=(10,5),parent=self.divadd,color="424242",text="Annehmen")
        self.textrej1 = avg.WordsNode(pos=(10,5),parent=self.divrej1,color="424242",text="Ablehnen - doppelt")
        self.textrej2 = avg.WordsNode(pos=(10,5),parent=self.divrej2,color="424242",text="Ablehnen - hab' ich nicht")
        self.textrej3 = avg.WordsNode(pos=(10,5),parent=self.divrej3,color="424242",text="Ablehnen - passt nicht")
        self.textblockuser = avg.WordsNode(pos=(10,5),parent=self.divblockuser,color="424242",text="User blockieren")

        #button "top 3 played"
        self.divsongplayed = avg.DivNode(id = "songplayed",pos=(340,160),size=(250,120),parent=self.rootNode)
        self.rectsongplayed = avg.RectNode(size=(250,120),pos=(0,0),parent=self.divsongplayed,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.textsongplayed =avg.WordsNode(pos=(10,5),parent=self.divsongplayed,color="424242",text="Top 1")
        self.textsongplayed2 =avg.WordsNode(pos=(10,35),parent=self.divsongplayed,color="424242",text="Top 2")
        self.textsongplayed3 =avg.WordsNode(pos=(10,65),parent=self.divsongplayed,color="424242",text="Top 3")
        self.textsongplayed4 =avg.WordsNode(pos=(10,95),parent=self.divsongplayed,color="424242",text="gespielt.")
        self.divsongplayed.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click2)
        
        #timer
        self.timer=avg.WordsNode (pos=(414,290), color="FFFFFF", font="arial", variant="Bold", text="60:00", fontsize=40, parent=self.rootNode)
        
        
        #start button
        self.divstart = avg.DivNode(id = "start",pos=(340,160),size=(250,120),parent=self.rootNode)
        self.rectstart = avg.RectNode(size=(250,120),pos=(0,0),parent=self.divstart,color="FF0000",fillcolor="FE2E2E", fillopacity=1)
        self.textstart =avg.WordsNode(fontsize=35, pos=(70,34),parent=self.divstart,color="8A0808",text="Start")
        self.divstart.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.clickstart)

        self.divabschnitt = avg.DivNode(id = "cuttingdiv", pos=(590,160), size=(200,120), parent=self.rootNode)
        self.rectabschnitt = avg.RectNode (id = "cuttingrect", size =(200,120), parent = self.divabschnitt, color="000000", fillcolor="000000", fillopacity=1)
        
        #starts the websocket in new thread
        thread.start_new_thread(self.initializeWebSocket, ())
                      
        #log.startLogging(sys.stdout)##Create a logfile (not necessary)
         
    #starts websocket       
    def initializeWebSocket(self):
        self.factory = WebSocketServerFactory(hostip, debug = False)
        self.factory.protocol = EchoServerProtocol ##assign protocol to send/receive messages
        listenWS(self.factory)
        
        reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading
    
    #creates countdown with m minutes, s seconds
    def countdown(self,m,s):
            
        def MsToSecs(m,s):
            return m*60 + s

        def secsToMs(secs):
            mins = secs//60
            secs -= mins*60
            mins = str(mins)
            secs = str(secs)
            return mins,secs
            
        seconds = MsToSecs(m,s)
        while seconds >= 0:
            (mint,sect)=secsToMs(seconds)
            if int(mint) == 0 and int(sect) == 30:
                global sendpermission
                sendpermission = False
                
            
            if int(mint) == 0 and int(sect) == 0:
                #no sendpermission until top3 played
                #TODO: pyclient send top3
                
                global pysend,pysend2, pyclient
                x = pyclient
                #TODO:PYSENDTOGGLE
                ips.getConnectionForIp(x).sendMessage('FINAL'+pysend)
        
                rcv.rectsongplayed.fillcolor="FE2E2E"
                rcv.rectsongplayed.color="FF0000"
                rcv.textsongplayed.color="8A0808"
                rcv.textsongplayed2.color="8A0808"
                rcv.textsongplayed3.color="8A0808"
                rcv.textsongplayed4.color="8A0808"
                
                top3 = []   #top3 songs
                i = 0
                if songdb.getlen() < 3: #check if top3 possible (3 songs in songdb)
                    k = songdb.getlen()
                else:
                    k = 3
                while i < k:    #add songs to top3
                    songele = []
                    interpret = songdb[i].interpret
                    songtitle = songdb[i].songtitle
                    numberofvotes = songdb[i].numberofvotes
                    fromuser = songdb[i].fromuser
                    song = interpret+'##'+songtitle
                    songele.append(interpret)
                    songele.append(songtitle)
                    songele.append(numberofvotes)
                    songele.append(fromuser)
                    songele.append(song)
                    top3.append(songele)
                    i+=1
                
                if len(top3) == 1:
                    rcv.textsongplayed.text = "1. "+top3[0][0] + " - " + top3[0][1]
                    rcv.textsongplayed2.text = ""
                    rcv.textsongplayed3.text = ""
                if len(top3) == 2:
                    rcv.textsongplayed.text = "1. "+top3[0][0] + " - " + top3[0][1]
                    rcv.textsongplayed2.text = "2. "+top3[1][0] + " - " + top3[1][1]
                    rcv.textsongplayed3.text = ""
                if len(top3) == 3:
                    rcv.textsongplayed.text = "1. "+top3[0][0] + " - " + top3[0][1]
                    rcv.textsongplayed2.text = "2. "+top3[1][0] + " - " + top3[1][1]
                    rcv.textsongplayed3.text = "3. "+top3[2][0] + " - " + top3[2][1]
                i = 0
                global pointgrow
                pointgrow = []
                while i < k:    #iterate over top k songs (k <= 3)
                #resets song
                    songdb.database.remove(songdb[0])
                    songdb.addSong(top3[i][0],top3[i][1],0,top3[i][3])
                
                
                    for user in userdb:
                        c = 0
                        if top3[i][3] == -1: #check if fromuser == -1 (means user who suggested this has been blocked)
                            pass
                        else:
                            if top3[i][3] == user.userid:
                                c = top3[i][2] * 10 #c = numberofvotes*10
                                user.numberofpoints += c    #add numberofpoints to userpoints
                                z = True
                                for x in pointgrow:
                                    if x[0] == user.userip and x[2] == user.username:   #checks if user already in pointgrow
                                        x[1] += c   #add points to pointgrowth
                                        x[3] += c   #add points to userpoints
                                        z = False
                    
                                if z:       #if user not already in pointgrowth, append him
                                    pointgrow.append([user.userip,c,user.username,user.numberofpoints])
                        
                        while True:
                            z = True
                            if top3[i][4] in user.votedfor: #if user voted for song
                                user.votedfor.remove(top3[i][4])    #remove song element once from votedfor
                                user.numberofpoints += 10   #add 10 points to userpoints
                                for x in pointgrow:
                                    if x[0] == user.userip and x[2] == user.username: #check if user already in pointgrow
                                        x[1] += 10  #add 10 points to pointgrowth
                                        x[3] += 10  #add 10 points to userpoints
                                        z = False
                                if z:    #check if user not already in pointgrow
                                    pointgrow.append([user.userip,10,user.username,user.numberofpoints])
                            else:
                                break
                    i+=1    #add 1 for looping
                userdb.database = userdb.mergeSortc()
            
                print "Der Countdown ist abgelaufen.\nSpiele nun bitte die Top 3 Crowd-Songs.\nDanach bestaetige, dass du die Songs gespielt hast."
                print "Nach der Bestaetigung werden die Top 3 User aktualisiert wie folgt:"
                i = userdb.getlen()
                if (i > 3):
                    i = 3
                c = 3
                pushy = ""
                while (i > 0):
                    pushy = str(i)+". "+userdb[i-1].username +"\n"+ pushy
                    i -= 1
                    c -= 1
                #fills empty slots (if less than 3 users)
                while (c > 0):
                    pushy = pushy + str(4-c) + ".\n"
                    c -= 1
                print pushy[:-1]
                print "Sollte einer der Namen anstoessig sein, blockiere den Nutzer mit 'block <username>'."
                
                for user in userdb:
                    user.numberofvotes = 3
                    ips.getConnectionForIp(user.userip).sendMessage('ACTVOT3'+str(user.numberofvotes))
            
            #sets timertext, adds zeros to singlenumber mins, secs
            if int(sect) < 10 and int(mint) < 10:
                self.timer.text="0"+mint + ":" + "0"+sect
            elif int(sect) < 10:
                self.timer.text=mint+":"+"0"+sect
            elif int(mint) < 10:
                self.timer.text="0"+mint+":"+sect
            else:
                self.timer.text=mint + ":" +sect
            
            #decrements timer by 1 sec
            time.sleep(1)
            seconds -= 1
            if seconds ==-1: #resets timer at 0:00
                seconds = 119
    
    def toallusers(self):
        time.sleep(2)
        for user in userdb:
                ips.getConnectionForIp(user.userip).sendMessage('SONGDB1'+songdb.tostring());
        self.toallusers()
        
    #console input for dj
    def input(self):
        while True: #always accept input
            x = raw_input()
            
            #prints console guide for dj
            if x[:4] == "help":
                print "Du hast folgende Moeglichkeiten:\n1. Mit 'change' gefolgt von dem Index eines Songs in der Vorschlagsliste\n   kannst Du Interpret und Songtitle des entsprechenden Songs abaendern.\n2. Mit 'block' gefolgt von einem Nutzernamen kannst Du einen Nutzer blockieren.\n   ACHTUNG!: Blockierst Du einen Nutzer auf diese Art, werden seine Punkte auf -1000 gesetzt!\n3. Mit 'songdb' kannst Du Dir die aktuelle Crowd-List mit allen Votes anzeigen lassen.\n4. Mit 'userdb' kannst Du Dir die aktuelle Nutzer-Datenbank anzeigen lassen.\nACHTUNG!: Die ersten beiden Operationen sind endgueltig und koennen nicht wieder rueckgaengig gemacht werden!"
            
            if x[:4] == "info":
                print "Auf der linken Seite siehst Du eine Liste mit den Liedvorschlaegen der Clubbesucher. \nZum Bearbeiten der Liedvorschlaege (Anklicken) hast du folgende Moeglichkeinten:"
                print "- 'Annnehmen': der Liedvorschlag wird zur Crowd-Liste hinzugefuegt und die Clubbesucher koennen dafuer voten."
                print "- 'Ablehnen - doppelt': das Lied wird nicht zur Song-Datenbank hinzugefuegt, weil es sich bereits in der Crowd-Liste befindet."
                print "- 'Ablehnen - hab' ich nicht': das Lied wird abgelehnt, da es sich nicht in Deiner Playliste befindet."
                print "- 'Ablehnen - passt nicht':  das Lied wird nicht uebernommen, da es nicht passt."
                print "- 'User blockieren': der User, der das Lied vorgeschlagen hat, wird blockiert. Er kann anschliessend keine Lieder mehr vorschlagen."
                print "Auf der rechten Seite siehst Du die sieben Songs der Crowd-Liste mit den aktuell meisten Votes."
                print "- 'Start': laeuft der grosse Screen, kann hier der Abend mit DjCrowd gestartet werden."
                print "Ist Dein Countdown abgelaufen, so werden die Top 3 Lieder auf dem 'Start'-Button antezeigt und Du bist gebeten, diese Lieder zu spielen."
                print "- 'Top 3 gespielt': bestaetige, dass Du die Top 3 gespielt hast."
            
            #debughelp for developers
            if x[:9] == "debughelp":
                print "songdb - Gibt Song-Datenbank aus.\nadds - Fuegt Song hinzu.\nvote - Votet fuer einen Song.\nuserdb - Gibt User-Datenbank aus.\naddu - Fuegt User hinzu.\npoints - Gibt Punkte an User.\npysend - Printet pysend\npysend2 - Printet pysend2"
            
            #fakes a vote
            if x[:4] == "vote":
                print "Fuer welches Lied moechtest du voten?"
                print "Interpret eingeben."
                interpret = raw_input()
                print "Songtitel eingeben."
                songtitle = raw_input()
                songdblen = songdb.getlen()
                for i in range(0,songdblen):
                    if (songtitle == songdb[i].songtitle and interpret == songdb[i].interpret):
                        songdb[i].numberofvotes += 1
                        j = i-1
                        k = i
                        while j>=0: ##sorts songarray!
                            if (songdb[k].numberofvotes <= songdb[j].numberofvotes):
                                break
                            songdb[j].interpret,songdb[k].interpret = songdb[k].interpret,songdb[j].interpret
                            songdb[j].songtitle,songdb[k].songtitle = songdb[k].songtitle,songdb[j].songtitle
                            songdb[j].numberofvotes,songdb[k].numberofvotes = songdb[k].numberofvotes,songdb[j].numberofvotes
                            songdb[j].fromuser,songdb[k].fromuser = songdb[k].fromuser,songdb[j].fromuser
                        
                            j -= 1
                            k -= 1
                        break;
                print "Fuer "+interpret+" - "+songtitle +" gevotet."
                
                x = songdb.tolist()
                global pysend
                pysend = ""
                for y in x:
                    a = y.split(' / ')
                    if len(a)==1:
                        pysend+=' ## ##0!#!'
                    else:
                        pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'        
                pysend = pysend[0:len(pysend)-3]
                
            #fakes user addition
            if x[:4] == "addu":
                print "Welchen User moechtest du hinzufuegen?"
                print "Name eingeben."
                user = raw_input()
                userdb.addUser(userdb.getlen(),"127.0.0.1",user,0,3)
                print "User "+user+" hinzugefuegt."
                
            #grants given user points
            if x[:6] == "points":
                print "Wem moechtest du Punkte geben?"
                print "Name eingeben."
                usern = raw_input()
                print "Punktzahl eingeben."
                points = raw_input()
                check = True
                for user in userdb:
                    if user.username == usern:
                        user.numberofpoints += int(points)
                        print "User "+usern +" hat "+points+" Punkte erhalten."
                        check = False
                if check:
                    print "User nicht gefunden."
            
            #fakes song addition
            if x[:4] == "adds":
                print "Welches Lied moechtest du hinzufuegen?"
                print "Interpret eingeben."
                interpret = raw_input()
                print "Songtitel eingeben."
                songtitle = raw_input()
                songdb.addSong(interpret,songtitle,0,-1)
                print interpret+" - "+songtitle+" hinzugefuegt."
                
                x = songdb.tolist()
                pysend = ""
                for y in x:
                    a = y.split(' / ')
                    if len(a)==1:
                        pysend+=' ## ##0!#!'
                    else:
                        pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'        
                pysend = pysend[0:len(pysend)-3]
            
            
            #prints songdb
            if x[:6] == "songdb":
                songdblen = songdb.getlen()
                if songdblen == 0:
                    print "Die Crowd-List ist momentan noch leer."
                for i in range(0,songdblen):
                    print "Interpret: "+songdb[i].interpret+", Songtitel: "+songdb[i].songtitle+", Votes: "+str(songdb[i].numberofvotes)
            
            #prints userdb
            if x[:6] == "userdb":
                userdblen = userdb.getlen()
                if userdblen == 0:
                    print "Die Nutzer-Datenbank ist momentan noch leer."
                for i in range(0,userdblen):
                    print "User: "+userdb[i].username+", Punkte: "+str(userdb[i].numberofpoints)
            
                
            #blocks user followed after whitespace
            if x[:5] == "block":
                usertoblock = userdb.getUserByName(x[6:])
                if usertoblock == 0:
                    print "Nutzer konnte nicht gefunden werden."
                else:
                    usertoblock.song1.interpret = "BLO##CKED"
                    usertoblock.song1.songtitle = "BLO##CKED"
                    usertoblock.song2.interpret = "BLO##CKED"
                    usertoblock.song2.songtitle = "BLO##CKED"
                    usertoblock.numberofpoints = -1000 #sets points to -1000 so the user disappears from the top 3 for sure (if more than 3 users are in userdb)
                    for song in songdb: #change fromuser of all songs the user suggested to -1
                        if song.fromuser == usertoblock.userid:
                            song.fromuser = -1
                    ips.getConnectionForIp(usertoblock.userip).sendMessage("USERBLC") #tells user he has been blocked by the dj
                    ips.getConnectionForIp(usertoblock.userip).sendMessage("POINTCO"+str(usertoblock.numberofpoints)) #updates user's points
                    print usertoblock.username,"blockiert"
                    userdb.database = userdb.mergeSortc() #sorts userdb
                    
                    #updates pysend2
                    global pyclient
                    pysend2 = ""
                    i = 0
                    while i < 3:
                        if i >= userdb.getlen():
                            pysend2 += ' ##0!#!'
                        else:
                            pysend2 += userdb[i].username+'##'+str(userdb[i].numberofpoints)+'!#!'
                        i+=1
                    pysend2 = pysend2[0:len(pysend2)-3]
                    
            #prints pysend
            if x[:6] == "pysend":
                print pysend
            
            #prints pysend2
            if x[:7] == "pysend2":
                print pysend2
            
            #allows dj to change a song in requestlist (to correct writing mistakes)
            if x[:6] == "change":
                y = int(x[7:]) #dj inputs 'change ' plus the number of the song in requestlist he wants to change
                if y > len(requestlist.node) or y < 1:
                    print "Songindex existiert nicht."
                    continue
                data = requestlist.node[y-1].text.split(' / ')
                print "Bearbeite Song:",data[1],"/",data[2] #tell dj which song he is editing
                print "Interpret", data[1],"aendern zu:" #asks dj for new interpret
                interpret = raw_input()
                print "Songtitle", data[2],"aendern zu:" #asks dj for new songtitle
                songtitle = raw_input()
                
                #adjust user's song
                user = userdb.getUser(data[1],data[2])
                if user.song1.interpret == data[1] and user.song1.songtitle == data[2]:
                    songnumber = 1
                if user.song2.interpret == data[1] and user.song2.songtitle == data[2]:
                    songnumber = 2
                if songnumber == 1:
                    user.song1.interpret = interpret
                    user.song1.songtitle = songtitle
                if songnumber == 2:
                    user.song2.interpret = interpret
                    user.song2.songtitle = songtitle
                
                #update requestlist
                requestlist.node[y-1].text = str(y)+" / "+interpret+" / "+songtitle
                requestlist.slist[y-1] = str(y)+" / "+interpret+" / "+songtitle
                print "Aenderte",data[1],"/",data[2],"zu",interpret,"/",songtitle
                         
if __name__ == '__main__':
    
    rcv=libAvgAppWithRect()
    ips=IPStorage()
    songdb = databases.SongDatabase()
    userdb = databases.UserDatabase()
    rejdb = databases.SongDatabase()
    
    #initializes requestlist
    listwindowid = "window"
    requestlist = ListNode(0, [], 2, size=(300, 100), pos=(5, 5), crop=True, elementoutlinecolor="333333", parent=rcv.player.getRootNode())
    
    #initializes top7 list
    listwindowid = "window2"
    topseven = ListNode(5000, ["1."], 2, size=(300, 140), pos=(315, 5), crop=True, elementoutlinecolor="333333", parent=rcv.player.getRootNode())
    topseven.addEle("2.")
    topseven.addEle("3.")
    topseven.addEle("4.")
    topseven.addEle("5.")
    topseven.addEle("6.")
    topseven.addEle("7.")      
    
    #initializes pysend, pysend2 and pyclient
    pysend = " ## ##0!#! ## ##0!#! ## ##0!#! ## ##0!#! ## ##0!#! ## ##0!#! ## ##0"
    pysend2 = " ##0!#! ##0!#! ##0"
    pyclient = 0
    sendpermission = True
    
    #starts listening to console
    thread.start_new_thread(rcv.input,())
    
    thread.start_new_thread(rcv.toallusers,())
    print "Herzlich Willkommen bei DjCrowd!"
    print "Gib 'help' ein, um eine Uebersicht deiner Befehle zu erhalten."
    print "Gib 'info' ein, um zusaetzliche Informationen zu DjCrowd zu erhalten."
    
    rcv.player.play()