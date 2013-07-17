'''
Created on 10 Jun 2013

@author: Alex
'''

###Userdatabase###
class UserDatabase(object):

    def __init__(self):
        self.database = []
        self.topthree = self.database[0:2]
        
    def __getitem__(self, index):
        return self.database[index]
    
    def getlen(self):
        return len(self.database)
        
    def addUser(self, userid, userip,username, numberofpoints, numberofvotes):
        user = User(userid, userip, username, SuggestedSong("LE##ER","LE##ER"), SuggestedSong("LE##ER","LE##ER"),numberofpoints, numberofvotes,[])
        self.database.append(user)
        
    #gets user by interpret and songtitle
    def getUser(self, interpret, songtitle):
        for user in self.database:
            if user.song1.songtitle == songtitle and user.song1.interpret == interpret:
                return user
            if user.song2.songtitle == songtitle and user.song2.interpret == interpret:
                return user
        return 0
    
    #gets user by username
    def getUserByName(self,name):
        for user in self.database:
            if user.username == name:
                return user
        return 0
    
    #sorts userdb
    def mergeSortc(self):
        x = self.mergeSort(self.database)
        return x
    
    def mergeSort(self,toSort):
        if len(toSort) <= 1:
            return toSort
 
        mIndex = len(toSort) / 2
        left = self.mergeSort(toSort[:mIndex])
        right = self.mergeSort(toSort[mIndex:])
        
        result = []
        while len(left) > 0 and len(right) > 0:
            if ((left[0]).numberofpoints) < ((right[0]).numberofpoints):  
                result.append(right.pop(0))
            else:
                result.append(left.pop(0))
        
        
        if len(left) > 0:
            result.extend(self.mergeSort(left))
        else:
            result.extend(self.mergeSort(right))
        return result
    
###User###
class User(object):
    def __init__(self, userid, userip, username, song1, song2, numberofpoints, numberofvotes, votedfor):
        self.userid = userid
        self.username = username
        self.userip = userip
        self.numberofpoints = numberofpoints
        self.numberofvotes = numberofvotes
        self.song1 = song1
        self.song2 = song2
        self.votedfor = votedfor
        
class SuggestedSong(object):
    def __init__(self,interpret,songtitle):
        self.interpret = interpret
        self.songtitle = songtitle
        self.status = 0

###Songdatabase###
class SongDatabase(object):

    def __init__(self):
        self.database = []
        self.topseven = self.database[0:6]
        
    def __getitem__(self, index):
        return self.database[index]

    def getlen(self):
        return len(self.database)
    
    def addSong(self, interpret, songtitle, numberofvotes, fromuser):
        song = Song(interpret, songtitle, numberofvotes, fromuser)
        self.database.append(song)

        if len(self.topseven) < 7:
            self.topseven.append(song)
    
    #checks if topseven has changed
    def checktopseven (self,oldtopseven):
        if len(oldtopseven) != len(self.topseven):
            return True
        for song in oldtopseven:
            for pong in self.topseven:
                if song.interpret != pong.interpret or song.songtitle != pong.songtitle or song.numberofvotes != pong.numberofvotes:
                    return True              
        return False
    
    #parses top7 songs to a stringlist
    def tolist (self):
        strlist = []
        i = 0
        while i < 7:
            if i >= len(self.database):
                strlist.append(str(i+1)+". ")
                i+=1
            else:
                strlist.append(str(i+1)+". "+str(self.database[i].interpret)+" / "+str(self.database[i].songtitle)+" / V:"+str(self.database[i].numberofvotes))
                i+=1
        return strlist
    
    #parses songdb to a string
    def tostring (self):
        tostring = ""
        i = 0
        while i < len(self.database):
            tostring += (str(self.database[i].interpret)+'##'+str(self.database[i].songtitle)+'##'+str(self.database[i].numberofvotes)+'!#!')
            i += 1
        return tostring[:-3]
    
    #gets user by interpret and songtitle
    def getUser(self, interpret, songtitle):
        for song in self.database:
            if song.songtitle == songtitle and song.interpret == interpret:
                return song.fromuser
            
###Song###
class Song(object):
    def __init__(self, interpret, songtitle, numberofvotes, fromuser):
        self.interpret = interpret
        self.songtitle = songtitle
        self.numberofvotes = numberofvotes
        self.fromuser = fromuser
        
    def toStr(self):
        return self.interpret+"##"+self.songtitle+"##"+self.numberofvotes