'''
Created on 10 Jun 2013

@author: Alex
'''
##USERDATABASE

class UserDatabase(object):

    def __init__(self):
        self.database = []

    def __getitem__(self, index):
        return self.database[index]
    
    def getlen(self):
        return len(self.database)
        
    def addUser(self, u_id, u_ip, username):
        user = User(u_id, u_ip, username, [], "", [], 0 ,0)
        self.database.append(user)

    
    def getUser(self, username):
        for user in self.database:
            if username == user.username:
                return user
        return 0
    
    def getUserByIP(self,u_ip):
        for user in self.database:
            if u_ip == user.u_ip:
                return user
        return 0
            
    #def getUser(self, interpret, songtitle):
    #    for user in self.database:
    #        if user.song1.songtitle == songtitle and user.song1.interpret == interpret:
    #            return user
    #        if user.song2.songtitle == songtitle and user.song2.interpret == interpret:
    #            return user
        
class User(object):
    def __init__(self, u_id, u_ip, username, groups, answer, guesses, score, stars):
        self.u_id = u_id
        self.u_ip = u_ip
        self.username = username
        self.groups = groups
        self.answer = answer
        self.guesses = guesses
        self.stars = stars
        self.score = score
        
    def addGroup(self,group):
        self.groups.append(group)
        
    
    def toStr(self):    
        print self.u_id, self.u_ip, self.username, self.groups
  
##GROUPDATABASE

class GroupDatabase(object):

    def __init__(self):
        self.database = []
        
    def __getitem__(self, index):
        return self.database[index]

    def getlen(self):
        return len(self.database)
    
    def addGroup(self, g_id, name, master, users):
        group = Group(g_id, name, master, users)
        self.database.append(group)
        
    def getGroupByID(self,id):
        for group in self.database:
            if id == group.g_id:
                return group
        return 0
    
    def getGroup(self,name):
        for group in self.database:
            if name == group.name:
                return group
        return 0
    
    def removeGroup(self,name):
        
        print self.database
        if not(self.getGroup(name) == 0):
            self.database.remove(self.getGroup(name))
        print self.database
        
class Group(object):
    def __init__(self, g_id, name, master, users):
        self.g_id = g_id
        self.name = name
        self.master = master
        self.users = users
        self.round = Round([])
        
    def toStr(self):    
        print self.g_id, self.name, self.master, self.users, self.round

    def validUser(self,u_id):
        for user in self.users:
            if user.u_id == u_id:
                return True
        return False

##ROUND

class Round(object):
    def __init__(self, users):
        self.users = users
        for user in users:
            user.answer = ""
            user.guesses = []