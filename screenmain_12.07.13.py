'''
Created on 03.07.2013

@author: Kirstin Buchholz, Norine Coenen, Stefanie Lehmann
'''

from libavg import *
import time
import thread
import sys
import ctypes
 
from twisted.internet import *
from twisted.python import *
from autobahn.websocket import *

from copy import deepcopy

global serverip

class screen(AVGApp):
    def __init__(self, parentNode):
        
        player = avg.Player.get()   #player
        global a,b,z
        
        #Initialisierung des Countdowns
        zeit = (0,10)
       
        #Variablen fuer die Animationsdauer
        timeFade = 1
        timeAnim = timeFade *1000
        
        #Wert fuer die maximale Animationsdauer des Rankings, sodass die einzelnen Aenderungen animiert werden (in Sekunden)
        maxAnimationDauer = 15 
        
        (a,b) = parentNode.size     #aufloesung
        #Startet im Fullscreen-Modus
        player.setResolution(True,int(a),int(b),32)
        canvas = player.createMainCanvas(size=(a,b)) #canvas kreieren
        self.rootNode = canvas.getRootNode()
        self.back = avg.RectNode (pos=(0,0), size=(a,b), parent=self.rootNode, color="000000", fillcolor="3D4163", fillopacity=1)
        if int(a)<=1024:
            self.z= int (a-(a/2.5))
        else:
            self.z = int (a-(a/3.0)) #(3.5 bei 1440 x 900) #(3.0 bei 1280x800)
        self.title=avg.WordsNode (pos=(a/30,15),font="marketing script", variant="Bold", text="DjCrowd", color="E9EBFF", fontsize=55, alignment="left", parent=self.rootNode) 
        self.logog=avg.ImageNode (href="logodj100pxpng.png", pos=(((a/2)-100),15),parent=self.rootNode)
        self.timer=avg.WordsNode (pos=(200,15),font="marketing script", variant="Bold", text="Countdown 60:00", color="E9EBFF", fontsize=55, indent=self.z, parent=self.rootNode)
        
        
        #Initialisiert die linke Haelfte des Bildschirms
        def left():
            
            #Initaialisierung des Vergleichsarrays fuer das Ranking
            self.alteOrdnung = [] 
            self.alteOrdnung.append(["-1-", "-1-", "0"])
            self.alteOrdnung.append(["-2-", "-2-", "0"])
            self.alteOrdnung.append(["-3-", "-3-", "0"])
            self.alteOrdnung.append(["-4-", "-4-", "0"])
            self.alteOrdnung.append(["-5-", "-5-", "0"])
            self.alteOrdnung.append(["-6-", "-6-", "0"])
            self.alteOrdnung.append(["-7-", "-7-", "0"])
            
            middle=a/2.5+10
            #linkes Hauptdiv
            self.divNode=avg.DivNode(pos=(0,(b/11)), size=(3*(a/5),b-50),parent=self.rootNode) #b-50
            
            #Divs fuer das Ranking
            self.ranking1=avg.WordsNode (pos=(a/30,int(b/6)),font="arial", variant="Bold", width=40, height= (b-50),text="1.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking2=avg.WordsNode (pos=(a/30,int(b/3.5175)),font="arial", variant="Bold", width=40, height= (b-50),text="2.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking3=avg.WordsNode (pos=(a/30,int(b/2.495)),font="arial", variant="Bold", width=40, height= (b-50),text="3." , color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking4=avg.WordsNode (pos=(a/30,int(b/1.935)),font="arial", variant="Bold", width=40, height= (b-50),text="4.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking5=avg.WordsNode (pos=(a/30,int(b/1.58)),font="arial", variant="Bold", width=40, height= (b-50),text="5.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking6=avg.WordsNode (pos=(a/30,int(b/1.335)),font="arial", variant="Bold", width=40, height= (b-50),text="6.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking7=avg.WordsNode (pos=(a/30,int(b/1.155)),font="arial", variant="Bold", width=40, height= (b-50),text="7.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            
            #Grundgeruest fuer die linke Seite /Titel
            self.leftr=avg.RectNode (pos=(0,0), size=(3*(a/5), b-50), parent=self.divNode, color="000000", fillcolor="46464B",fillopacity=1)
            self.title=avg.WordsNode (pos=(int(a/5.5),5),font="marketing script", variant="Bold", text=" Top 7 Songs ", color="E9EBFF", fontsize=40, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(int(a/2-80-20),5),font="marketing script", variant="Bold", text="Votes", color="E9EBFF", fontsize=40, parent=self.divNode)
            
            #Initialisierung der sieben Divs fuer die Plaetze mit ihren zugehoehrigen Wordsnodes 
            #(in platzXa steht der Titel des Liedes, in platzXb der Interpret und in platzXc die Anzahl der Votes)
            self.div1=avg.DivNode(pos=(a/18,b/6), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz1a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[0][1], color="FFD700", fontsize=30, parent=self.div1)
            self.platz1b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[0][0], color="FFD700", fontsize=20, parent=self.div1)
            self.platz1c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[0][2], color="FFD700", fontsize=30, parent=self.div1)
            
            self.div2=avg.DivNode(pos=(a/18,b/3.5175), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz2a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[1][1], color="FFEC6A", fontsize=30, parent=self.div2)
            self.platz2b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[1][0], color="FFEC6A", fontsize=20, parent=self.div2)
            self.platz2c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[1][2], color="FFEC6A", fontsize=30, parent=self.div2)
            
            self.div3=avg.DivNode(pos=(a/18,b/2.495), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz3a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[2][1], color="FFFFCD", fontsize=30, parent=self.div3)
            self.platz3b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[2][0], color="FFFFCD", fontsize=20, parent=self.div3)
            self.platz3c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[2][2], color="FFFFCD", fontsize=30, parent=self.div3)
           
            self.div4=avg.DivNode(pos=(a/18,b/1.935), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz4a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[3][1], color="D0D1E2", fontsize=30, parent=self.div4)
            self.platz4b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[3][0], color="D0D1E2", fontsize=20, parent=self.div4)
            self.platz4c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[3][2], color="D0D1E2", fontsize=30, parent=self.div4)
            
            self.div5=avg.DivNode(pos=(a/18,b/1.58), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz5a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[4][1], color="D0D1E2", fontsize=30, parent=self.div5)
            self.platz5b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[4][0], color="D0D1E2", fontsize=20, parent=self.div5)
            self.platz5c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[4][2], color="D0D1E2", fontsize=30, parent=self.div5)
            
            self.div6=avg.DivNode(pos=(a/18,b/1.335), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz6a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[5][1], color="D0D1E2", fontsize=30, parent=self.div6)
            self.platz6b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[5][0], color="D0D1E2", fontsize=20, parent=self.div6)
            self.platz6c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[5][2], color="D0D1E2", fontsize=30, parent=self.div6)
            
            self.div7=avg.DivNode(pos=(a/18,b/1.155), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz7a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[6][1], color="D0D1E2", fontsize=30, parent=self.div7)
            self.platz7b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[6][0], color="D0D1E2", fontsize=20, parent=self.div7)
            self.platz7c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[6][2], color="D0D1E2", fontsize=30, parent=self.div7)
            
            
    #Deklaration aller noetigen Hilfsvariablen fuer die Animationen der linken Seite
        
        #sucht in der Vergleichsordnung, ob das gegebene Lied (Titel und Interpret) dort schon enthalten ist. 
        #Falls dies der Fall ist, wird die Position in der alten Ordnung zurueckgegeben, falls nicht, so wird 7 zurueckgegeben.
        def schonda (alteOrdnung, titel, interpret):
            i = 0
            while i < 7 :
                if alteOrdnung[i][1] == titel and alteOrdnung[i][0] == interpret:
                    return i
                i += 1
            return 7
        
        #Tauscht die Positionen der beiden uebergebenen Objekte (Divs aus dem Ranking) als Animation
        def swap (a, b, posa, posb): 
            def startAnim():
                animObj.start()
                
            animObj = ParallelAnim([LinearAnim(a, "pos", timeAnim, posa, posb),  
                                    LinearAnim(b, "pos", timeAnim, posb, posa)])
            player.setTimeout(0, startAnim)
            time.sleep(timeFade)
            
        #Tauscht die Farben der Wordsnodes von zwie Divs 
        def colswap (w1a, w1b, w1c, w2a, w2b, w2c): 
            col1 = w1a.color
            col2 = w2a.color
            w1a.color = col2
            w1b.color = col2
            w1c.color = col2
            w2a.color = col1
            w2b.color = col1
            w2c.color = col1
           
        #Tauscht die Divs der Songs wieder zurueck, damit anschliessend wieder mit den alten Bezeichnungen gearbeitet werden kann
        def TauschenSongDivs(div1, div2, arrayposition1, arrayposition2, platz1a, platz1b, platz1c, platz2a, platz2b, platz2c, pos1, pos2):
            #vertauscht die Positionen der beiden Divs
            div1.pos = pos1
            div2.pos = pos2
            
            #passt den Inhalt der Wordsnodes entsprechend des Tausches an
            platz1a.text = self.alteOrdnung[arrayposition1][1]
            platz1b.text = self.alteOrdnung[arrayposition1][0]
            platz1c.text = self.alteOrdnung[arrayposition1][2]
            
            platz2a.text = self.alteOrdnung[arrayposition2][1]
            platz2b.text = self.alteOrdnung[arrayposition2][0]
            platz2c.text = self.alteOrdnung[arrayposition2][2]
            
            #tauscht die Farben der Wordsnodes, sodass alles optisch aussieht, wie vor dem Tausch
            colswap(platz1a, platz1b, platz1c, platz2a, platz2b, platz2c)
           
        #Tauschen von Elementen im Array
        def TauschenArray(array, position1, position2):
            #speichert die Werte an der erten Position im Array zwischen
            interpret1 = array[position1][0]
            song1 = array[position1][1]
            votes1 = array[position1][2]
            
            #ueberschreibt die Werte an der ersten Position im Array mit denen an der zweiten Position
            array[position1][0] = array[position2][0]
            array[position1][1] = array[position2][1]
            array[position1][2] = array[position2][2]
            
            #ueberschreibt die Werte an der zweiten Position im Array mit den vorher zwischengespeicherten Werten von Position 1
            array[position2][0] = interpret1
            array[position2][1] = song1
            array[position2][2] = votes1
     
        #Animiert das Ersetzen des ersten Platzes und passt das Vergleichsarray an
        def div7setzen(neueOrdnung0, neueOrdnung1, neueOrdnung2):
            #blendet das aktuel letzte Lied aus
            fadeOut(self.platz7a, timeAnim)
            fadeOut(self.platz7b, timeAnim)
            fadeOut(self.platz7c, timeAnim)
            time.sleep(timeFade)
            
            #ueberschreibt den Text in den Wordsnodes von Div 7
            self.platz7a.text = neueOrdnung1
            self.platz7b.text = neueOrdnung0
            self.platz7c.text = neueOrdnung2
            
            #blendet das neue Lied wieder ganz unten ein
            fadeIn(self.platz7a, timeAnim)
            fadeIn(self.platz7b, timeAnim)
            fadeIn(self.platz7c, timeAnim)
            time.sleep(timeFade)
            
            #aktualisiert auch die Informationen im Vergleichsarray
            self.alteOrdnung[6][0] = neueOrdnung0
            self.alteOrdnung[6][1] = neueOrdnung1
            self.alteOrdnung[6][2] = neueOrdnung2
     
        #Tauscht das letzte mit dem vorletzen Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)
        def sevenSix():
            swap(self.div7, self.div6, (a/18,b/1.155), (a/18,b/1.335))
            colswap(self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 5, 6)
            time.sleep(0.1)
            TauschenSongDivs(self.div6, self.div7, 5, 6, self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c, (a/18,b/1.335), (a/18,b/1.155))
           
        #Tauscht das sechste mit dem fuenften Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)  
        def sixFive():
            swap(self.div6, self.div5, (a/18,b/1.335), (a/18,b/1.58))
            colswap(self.platz5a, self.platz5b, self.platz5c, self.platz6a, self.platz6b, self.platz6c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 4, 5)
            time.sleep(0.1)
            TauschenSongDivs(self.div5, self.div6, 4, 5, self.platz5a, self.platz5b, self.platz5c, self.platz6a, self.platz6b, self.platz6c, (a/18,b/1.58), (a/18,b/1.335))
            
        #Tauscht das fuenfte mit dem vierten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)  
        def fiveFour(): 
            swap(self.div5, self.div4, (a/18,b/1.58), (a/18,b/1.935))
            colswap(self.platz4a, self.platz4b, self.platz4c, self.platz5a, self.platz5b, self.platz5c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 3, 4)
            time.sleep(0.1)
            TauschenSongDivs(self.div4, self.div5, 3, 4, self.platz4a, self.platz4b, self.platz4c, self.platz5a, self.platz5b, self.platz5c, (a/18,b/1.935), (a/18,b/1.58))
          
        #Tauscht das vierte mit dem dritten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht) 
        def fourThree():
            swap(self.div4, self.div3, (a/18,b/1.935), (a/18,b/2.495))
            colswap(self.platz3a, self.platz3b, self.platz3c, self.platz4a, self.platz4b, self.platz4c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 2, 3)
            time.sleep(0.1)
            TauschenSongDivs(self.div3, self.div4, 2, 3, self.platz3a, self.platz3b, self.platz3c, self.platz4a, self.platz4b, self.platz4c, (a/18,b/2.495), (a/18,b/1.935))
            
        #Tauscht das dritte mit dem zweiten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)
        def threeTwo():
            swap(self.div3, self.div2, (a/18,b/2.495), (a/18,b/3.5175))
            colswap(self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 1, 2)
            time.sleep(0.1)
            TauschenSongDivs(self.div2, self.div3, 1, 2, self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c, (a/18,b/3.5175), (a/18,b/2.495))
            
        #Tauscht das zweite mit dem ersten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)
        def twoOne():
            swap(self.div2, self.div1, (a/18,b/3.5175), (a/18,b/6))
            colswap(self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 0, 1)
            time.sleep(0.1)
            TauschenSongDivs(self.div1, self.div2, 0, 1, self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c, (a/18,b/6), (a/18,b/3.5175))
        
        #aktualisiert die Votezahl am uebergebenen Platz als Animation im Wordsnode und zusaetzlich im Vergliechsarray
        def aktualisiereVotes(position, wordsnode, neueVotes):
            #Animation auf dem Screen
            fadeOut(wordsnode, timeAnim)
            time.sleep(timeFade)
            wordsnode.text = neueVotes
            fadeIn(wordsnode, timeAnim)
            time.sleep(timeFade)
            
            #Anpassen des Vergleichsarrays
            self.alteOrdnung[position][2] = neueVotes
            time.sleep(0.1)
            
        #Funktion, die die Animation der Rankingaenderungen implementiert
        def updateRanking (neueOrdnung, null):  
            #verzoegert den Start der Animation, um Threadingprobleme zu verhindern                         
            time.sleep(0.5)
            
        #zuerst wird der erste Platz des Rankings animiert
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7
            where = schonda(self.alteOrdnung, neueOrdnung[0][1], neueOrdnung[0][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[0][0], neueOrdnung[0][1], neueOrdnung[0][2])
                #und animiert dies dann bis an die erste Stelle
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
                twoOne()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert
            else:
                #Lied befindet sich an letzer Stelle
                if where == 6: 
                    #aktualisert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der sechsten Stelle
                elif where == 5:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der fuenften Stelle
                elif where == 4:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der vierten Stelle
                elif where == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der dritten Stelle
                elif where == 2:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz3c.text != neueOrdnung[0][2]: 
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der zweiten Stelle
                elif where == 1:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz2c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(1, self.platz2c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    twoOne()
                #Lied befindet sich bereits an der ersten Stelle
                elif where == 0:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz1c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(0, self.platz1c, neueOrdnung[0][2])
            
        #Nun wird der zweite Platz gesetzt
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where2 = schonda(self.alteOrdnung, neueOrdnung[1][1], neueOrdnung[1][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where2 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[1][0], neueOrdnung[1][1], neueOrdnung[1][2])
                #und animiert dies dann bis an die zweite Stelle
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where2 == 6:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                #Lied befindet sich an der sechsten Stelle
                elif where2 == 5:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                #Lied befindet sich an fuenfter Stelle
                elif where2 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    fiveFour()
                    fourThree()
                    threeTwo()
                #Lied befindet sich an der vierten Stelle
                elif where2 == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    fourThree()
                    threeTwo()
                #Lied befindet sich an der dritten Stelle
                elif where2 == 2:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz3c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    threeTwo()
                #Lied befindet sich bereits an der zweiten Stelle
                elif where2 == 1:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz2c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(1, self.platz2c, neueOrdnung[1][2])
                        
        #Als naechstes folgt Platz 3
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where3 = schonda(self.alteOrdnung, neueOrdnung[2][1], neueOrdnung[2][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where3 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[2][0], neueOrdnung[2][1], neueOrdnung[2][2])
                #und animiert dies dann bis an die dritte Stelle
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where3 == 6: 
                    #aktualisert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                #Lied befindet sich an der sechsten Stelle
                elif where3 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    sixFive()
                    fiveFour()
                    fourThree()
                #Lied befindet sich an der fuenften Stelle
                elif where3 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    fiveFour()
                    fourThree()
                #Lied befindet sich an der vierten Stelle
                elif where3 == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    fourThree()
                #Lied befindet sich bereits an der dritten Stelle
                elif where3 == 2:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz3c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[2][2])
                        
        #Nun betrachten wir den vierten Platz
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where4 = schonda(self.alteOrdnung, neueOrdnung[3][1], neueOrdnung[3][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where4 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[3][0], neueOrdnung[3][1], neueOrdnung[3][2])
                #und animiert dies dann bis an die vierte Stelle
                sevenSix()
                sixFive()
                fiveFour()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where4 == 6:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[3][2])
                    #und animiert das Lied an die vierte Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                #Lied befindet sich an der sechsten Stelle
                elif where4 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[3][2])
                    #und animiert das Lied an die vierte Stelle
                    sixFive()
                    fiveFour()
                #Lied befindet sich an der fuenften Stelle
                elif where4 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[3][2])
                    #und animiert das Lied an die vierte Stelle
                    fiveFour()
                #Lied befindet sich bereits an der vierten Stelle
                elif where4 == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[3][2])
          
        #Es folgt die Animation fuer den fuenften Platz
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where5 = schonda(self.alteOrdnung, neueOrdnung[4][1], neueOrdnung[4][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where5 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[4][0], neueOrdnung[4][1], neueOrdnung[4][2])
                #und animiert dies dann bis an die fuenfte Stelle
                sevenSix()
                sixFive()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where5 == 6: #testen ob interpret gleich und votes aktualisiern
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[4][2])
                    #und animiert dies dann bis an die fuenfte Stelle
                    sevenSix()
                    sixFive()
                #Lied befindet sich an der sechsten Stelle
                elif where5 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[4][2])
                    #und animiert dies dann bis an die fuenfte Stelle
                    sixFive()
                #Lied befindet sich bereits an der fuenften Stelle
                elif where5 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[4][2])
            
        #Nun betrachten wir die Animation, die den sechsten Platz aktualisiert
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where6 = schonda(self.alteOrdnung, neueOrdnung[5][1], neueOrdnung[5][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where6 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[5][0], neueOrdnung[5][1], neueOrdnung[5][2])
                #und animiert dies dann bis an die sechste Stelle
                sevenSix()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where6 == 6: 
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[5][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[5][2])
                    #und animiert dies dann bis an die fuenfte Stelle
                    sevenSix()
                #Lied befindet sich bereits an der sechsten Stelle
                elif where6 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[5][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[5][2])
                        
        #Es fehlt noch die Animation fuer den letzten Platz
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where7 = schonda(self.alteOrdnung, neueOrdnung[6][1], neueOrdnung[6][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where7 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[6][0], neueOrdnung[6][1], neueOrdnung[6][2])
                #hier muss nichts animiert werden, da sich das Lied nach der Initaialisierung bereits an der richtigen Stelle befindet
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich bereits an letzer Stelle
                if where7 == 6: 
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[6][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[6][2])
            
            #stellt sicher, dass das Tauschen funktioniert hat
            self.div1.pos = (a/18,b/6)
            self.div2.pos = (a/18,b/3.5175)
            self.div3.pos = (a/18,b/2.495)
            self.div4.pos = (a/18,b/1.935)
            self.div5.pos = (a/18,b/1.58)
            self.div6.pos = (a/18,b/1.335)
            self.div7.pos = (a/18,b/1.155)
            
            
        #Falls die Animation der Lieder zu lange dauert, wird diese Funktion aufgerufen. 
        #Es werden alle sieben Lieder ausgefadet und mit der neuen Liste initialisiert wieder eingeblendet.  
        def fadeAnimSongsNormal (neueOrdnung, null):
            time.sleep(0.1)
            
        #Abfangen von Randfaellen
            #Es wurde noch nichts hinzugefuegt
            if neueOrdnung[0][0] == " " and neueOrdnung[0][1] == " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung = deepcopy(self.alteOrdnung)
            #Es befindet sich nur ein Lied in der Liste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[1][0] = "-1-"
                neueOrdnung[1][1] = "-1-"
                neueOrdnung[1][2] = "0"
                neueOrdnung[2][0] = "-2-"
                neueOrdnung[2][1] = "-2-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-3-"
                neueOrdnung[3][1] = "-3-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-4-"
                neueOrdnung[4][1] = "-4-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-5-"
                neueOrdnung[5][1] = "-5-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-6-"
                neueOrdnung[6][1] = "-6-"
                neueOrdnung[6][2] = "0"
            #Es wurden zwei Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[2][0] = "-1-"
                neueOrdnung[2][1] = "-1-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-2-"
                neueOrdnung[3][1] = "-2-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-3-"
                neueOrdnung[4][1] = "-3-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-4-"
                neueOrdnung[5][1] = "-4-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-5-"
                neueOrdnung[6][1] = "-5-"
                neueOrdnung[6][2] = "0"
            #Drei Lieder wurden uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[3][0] = "-1-"
                neueOrdnung[3][1] = "-1-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-2-"
                neueOrdnung[4][1] = "-2-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-3-"
                neueOrdnung[5][1] = "-3-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-4-"
                neueOrdnung[6][1] = "-4-"
                neueOrdnung[6][2] = "0"
            #Es befinden sich vier Lieder in der Argumentliste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[4][0] = "-1-"
                neueOrdnung[4][1] = "-1-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-2-"
                neueOrdnung[5][1] = "-2-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-3-"
                neueOrdnung[6][1] = "-3-"
                neueOrdnung[6][2] = "0"
            #fuenf Lieder als Eingabe
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[5][0] = "-1-"
                neueOrdnung[5][1] = "-1-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-2-"
                neueOrdnung[6][1] = "-2-"
                neueOrdnung[6][2] = "0"
            #Es wurden sechs Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[6][0] = "-1-"
                neueOrdnung[6][1] = "-1-"
                neueOrdnung[6][2] = "0"
            #Es wurde ein komplett volles Array uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] != " " and neueOrdnung[6][1] != " ":
                pass
            
            if neueOrdnung == self.alteOrdnung:
                pass
            else:
                #Ausblenden der sieben Lied-Divs
                fadeOut(self.div1, timeAnim)
                fadeOut(self.div2, timeAnim)
                fadeOut(self.div3, timeAnim)
                fadeOut(self.div4, timeAnim)
                fadeOut(self.div5, timeAnim)
                fadeOut(self.div6, timeAnim)
                fadeOut(self.div7, timeAnim)
                time.sleep(timeFade)
                
                #Ueberschreiben der Informationen in den Wordsnodes der sieben Lied-Divs mit den Werten der neuen Rangliste
                #Setzen der neuen Titel
                self.platz1a.text= neueOrdnung[0][1]
                self.platz2a.text= neueOrdnung[1][1]
                self.platz3a.text= neueOrdnung[2][1]
                self.platz4a.text= neueOrdnung[3][1]
                self.platz5a.text= neueOrdnung[4][1]
                self.platz6a.text= neueOrdnung[5][1]
                self.platz7a.text= neueOrdnung[6][1]
                #Setzen der neuen Interpreten
                self.platz1b.text= neueOrdnung[0][0]
                self.platz2b.text= neueOrdnung[1][0]
                self.platz3b.text= neueOrdnung[2][0]
                self.platz4b.text= neueOrdnung[3][0]
                self.platz5b.text= neueOrdnung[4][0]
                self.platz6b.text= neueOrdnung[5][0]
                self.platz7b.text= neueOrdnung[6][0]
                #Setzen der neuen Votes
                self.platz1c.text= neueOrdnung[0][2]
                self.platz2c.text= neueOrdnung[1][2]
                self.platz3c.text= neueOrdnung[2][2]
                self.platz4c.text= neueOrdnung[3][2]
                self.platz5c.text= neueOrdnung[4][2]
                self.platz6c.text= neueOrdnung[5][2]
                self.platz7c.text= neueOrdnung[6][2]
                
                #Ueberschreiben des Vergleichsarrays mit dem neuen aktuellen Ranking
                self.alteOrdnung = deepcopy(neueOrdnung)
                
                #Erneutes Einblenden der aktualisierten Divs
                fadeIn(self.div1, timeAnim)
                fadeIn(self.div2, timeAnim)
                fadeIn(self.div3, timeAnim)
                fadeIn(self.div4, timeAnim)
                fadeIn(self.div5, timeAnim)
                fadeIn(self.div6, timeAnim)
                fadeIn(self.div7, timeAnim)
            
        #Simuliert die Animation der Liste und berechnet, wie lange die Animation dauern wuerde. Anschliessend waehlt es auf dieser Basis aus, 
        #ob die neue Liste animiert (updateRanking) oder eingeblendet (fadeAnimSongsNormal) wird 
        def animationUpdate (neueOrdnung):
        #Abfangen von Randfaellen
            #Es wurde noch nichts hinzugefuegt
            if neueOrdnung[0][0] == " " and neueOrdnung[0][1] == " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung = deepcopy(self.alteOrdnung)
            #Es befindet sich nur ein Lied in der Liste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[1][0] = "-1-"
                neueOrdnung[1][1] = "-1-"
                neueOrdnung[1][2] = "0"
                neueOrdnung[2][0] = "-2-"
                neueOrdnung[2][1] = "-2-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-3-"
                neueOrdnung[3][1] = "-3-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-4-"
                neueOrdnung[4][1] = "-4-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-5-"
                neueOrdnung[5][1] = "-5-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-6-"
                neueOrdnung[6][1] = "-6-"
                neueOrdnung[6][2] = "0"
            #Es wurden zwei Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[2][0] = "-1-"
                neueOrdnung[2][1] = "-1-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-2-"
                neueOrdnung[3][1] = "-2-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-3-"
                neueOrdnung[4][1] = "-3-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-4-"
                neueOrdnung[5][1] = "-4-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-5-"
                neueOrdnung[6][1] = "-5-"
                neueOrdnung[6][2] = "0"
            #Drei Lieder wurden uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[3][0] = "-1-"
                neueOrdnung[3][1] = "-1-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-2-"
                neueOrdnung[4][1] = "-2-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-3-"
                neueOrdnung[5][1] = "-3-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-4-"
                neueOrdnung[6][1] = "-4-"
                neueOrdnung[6][2] = "0"
            #Es befinden sich vier Lieder in der Argumentliste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[4][0] = "-1-"
                neueOrdnung[4][1] = "-1-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-2-"
                neueOrdnung[5][1] = "-2-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-3-"
                neueOrdnung[6][1] = "-3-"
                neueOrdnung[6][2] = "0"
            #fuenf Lieder als Eingabe
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[5][0] = "-1-"
                neueOrdnung[5][1] = "-1-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-2-"
                neueOrdnung[6][1] = "-2-"
                neueOrdnung[6][2] = "0"
            #Es wurden sechs Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[6][0] = "-1-"
                neueOrdnung[6][1] = "-1-"
                neueOrdnung[6][2] = "0"
            #Es wurde ein komplett volles Array uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] != " " and neueOrdnung[6][1] != " ":
                pass
                
            #Initialisierung der Animationsdauer, um anfaengliche Verzoegerungen auszugleichen         
            animationDauer = 3
            
            #Erstellung einer unabhaengig veraenderlichen Kopie der alten Vergleichsordnung, um die Animation zu simulieren und deren Dauer abschaetzen zu koennen
            kopie = deepcopy(self.alteOrdnung)
            
    #berechnet die Animationsdauer grob
        #Simulation der Animation fuer den ersten Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim1 = schonda(kopie, neueOrdnung[0][1], neueOrdnung[0][0]) 
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim1 + 1) * timeFade 
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim1 == 7: 
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[0][0]
                kopie[6][1] = neueOrdnung[0][1]
                kopie[6][2] = neueOrdnung[0][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade 
                # -> Es muessen sieben Animationen durchgefueht werden (auf Platz sieben einfaden und anschliessend auf Platz eins hochtauschen)
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            #das Lied befindet sich auf dem letzen Platz in der Rangliste
            elif anzAnim1 == 6: 
                # -> Es muessen sechs/sieben Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz eins hochtauschen)
                if kopie[6][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            #das Lied ist auf Platz sechs des Rankings zu finden
            elif anzAnim1 == 5:
                # -> Es muessen fuenf/sechs Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz eins hochtauschen)
                if kopie[5][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            #das Lied befindet sich auf Platz fuenf im Ranking
            elif anzAnim1 == 4: 
                # -> Es muessen vier/fuenf Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz eins hochtauschen)
                if kopie[4][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            #das Lied ist auf Platz vier
            elif anzAnim1 == 3: 
                # -> Es muessen drei/vier Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz eins hochtauschen)
                if kopie[3][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            #das Lied befindet sich aktuell auf dem dritten Platz des Rankings
            elif anzAnim1 == 2:
                # -> Es muessen zwei/drei Animationen durchgefueht werden (Votes aktualisieren und auf Platz eins hochtauschen)
                if kopie[2][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            #das Lied steht an zweiter Stelle im Ranking
            elif anzAnim1 == 1: 
                # -> Es muessen eine/zwei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz eins hochtauschen)
                if kopie[1][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 0, 1)
            #das Lied befindet sich bereits auf dem ersten Platz
            elif anzAnim1 == 0: #platz 1
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[0][2] == neueOrdnung[0][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade 
           
        #Simulation der Animation fuer den zweiten Platz  
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim2 = schonda(kopie, neueOrdnung[1][1], neueOrdnung[1][0]) #platz 2
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim2 - 0) * timeFade
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim2 == 7: #nich in liste
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[1][0]
                kopie[6][1] = neueOrdnung[1][1]
                kopie[6][2] = neueOrdnung[1][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade
                # -> Es muessen sechs Animationen durchgefueht werden (auf Platz sieben einfaden und anschliessend auf Platz zwei hochtauschen)
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            #das Lied befindet sich auf dem letzen Platz in der Rangliste
            elif anzAnim2 == 6: 
                # -> Es muessen fuenf/sechs Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz zwei hochtauschen)
                if kopie[6][2] == neueOrdnung[1][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            #das Lied ist auf Platz sechs des Rankings zu finden
            elif anzAnim2 == 5: 
                # -> Es muessen vier/fuenf Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz zwei hochtauschen)
                if kopie[5][2] == neueOrdnung[1][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            #das Lied befindet sich auf Platz fuenf im Ranking
            elif anzAnim2 == 4: 
                # -> Es muessen drei/vier Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz zwei hochtauschen)
                if kopie[4][2] == neueOrdnung[1][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            #das Lied ist auf Platz vier
            elif anzAnim2 == 3: 
                # -> Es muessen zwei/drei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz zwei hochtauschen)
                if kopie[3][2] == neueOrdnung[1][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            #das Lied befindet sich aktuell auf dem dritten Platz des Rankings
            elif anzAnim2 == 2: 
                # -> Es muessen eine/zwei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz zwei hochtauschen)
                if kopie[2][2] == neueOrdnung[1][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 1, 2)
            #das Lied steht bereits an zweiter Stelle im Ranking
            elif anzAnim2 == 1: 
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[1][2] == neueOrdnung[1][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
           
        #Simulation der Animation fuer den dritten Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim3 = schonda(kopie, neueOrdnung[2][1], neueOrdnung[2][0]) 
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim3 - 1) * timeFade
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim3 == 7: #nich in liste
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[2][0]
                kopie[6][1] = neueOrdnung[2][1]
                kopie[6][2] = neueOrdnung[2][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade
                # -> Es muessen fuenf Animationen durchgefueht werden (auf Platz sieben einfaden und anschliessend auf Platz drei hochtauschen)
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            #das Lied befindet sich auf dem letzen Platz in der Rangliste
            elif anzAnim3 == 6: 
                # -> Es muessen vier/funf Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz drei hochtauschen)
                if kopie[6][2] == neueOrdnung[2][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            #das Lied ist auf Platz sechs des Rankings zu finden
            elif anzAnim3 == 5:  
                # -> Es muessen drei/vier Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz drei hochtauschen)
                if kopie[5][2] == neueOrdnung[2][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            #das Lied befindet sich auf Platz fuenf im Ranking
            elif anzAnim3 == 4:  
                # -> Es muessen zwei/drei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz drei hochtauschen)
                if kopie[4][2] == neueOrdnung[2][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            #das Lied ist auf Platz vier
            elif anzAnim3 == 3:  
                # -> Es muessen eine/zwei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz drei hochtauschen)
                if kopie[3][2] == neueOrdnung[2][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 2, 3)
            #das Lied befindet sich bereits auf dem dritten Platz des Rankings
            elif anzAnim3 == 2:
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[2][2] == neueOrdnung[2][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                    
        #Simulation der Animation fuer den vierten Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim4 = schonda(kopie, neueOrdnung[3][1], neueOrdnung[3][0]) #platz 4
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim4 - 2) * timeFade
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim4 == 7: #nich in liste
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[3][0]
                kopie[6][1] = neueOrdnung[3][1]
                kopie[6][2] = neueOrdnung[3][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade
                # -> Es muessen vier Animationen durchgefueht werden (auf Platz sieben einfaden und anschliessend auf Platz vier hochtauschen)
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
            #das Lied befindet sich auf dem letzen Platz in der Rangliste
            elif anzAnim4 == 6:  
                # -> Es muessen drei/vier Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz vier hochtauschen)
                if kopie[6][2] == neueOrdnung[3][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
            #das Lied ist auf Platz sechs des Rankings zu finden
            elif anzAnim4 == 5:   
                # -> Es muessen zwei/drei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz vier hochtauschen)
                if kopie[5][2] == neueOrdnung[3][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
            #das Lied befindet sich auf Platz fuenf im Ranking
            elif anzAnim4 == 4:   
                # -> Es muessen eine/zwei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz vier hochtauschen)
                if kopie[4][2] == neueOrdnung[3][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 3, 4)
            #das Lied ist bereits auf Platz vier
            elif anzAnim4 == 3: #platz 4
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[3][2] == neueOrdnung[3][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
            
        #Simulation der Animation fuer den fuenften Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim5 = schonda(kopie, neueOrdnung[4][1], neueOrdnung[4][0]) #platz 5
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim5 - 3) * timeFade
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim5 == 7: #nich in liste
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[4][0]
                kopie[6][1] = neueOrdnung[4][1]
                kopie[6][2] = neueOrdnung[4][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade
                # -> Es muessen drei Animationen durchgefueht werden (auf Platz sieben einfaden und anschliessend auf Platz fuenf hochtauschen)
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
            #das Lied befindet sich auf dem letzen Platz in der Rangliste
            elif anzAnim5 == 6:   
                # -> Es muessen zwei/drei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz fuenf hochtauschen)
                if kopie[6][2] == neueOrdnung[4][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
            #das Lied ist auf Platz sechs des Rankings zu finden
            elif anzAnim5 == 5:    
                # -> Es muessen eine/zwei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz fuenf hochtauschen)
                if kopie[5][2] == neueOrdnung[4][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 4, 5)
            #das Lied befindet sich bereits auf Platz fuenf im Ranking
            elif anzAnim5 == 4: 
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[4][2] == neueOrdnung[4][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade            
            
        #Simulation der Animation fuer den sechsten Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim6 = schonda(kopie, neueOrdnung[5][1], neueOrdnung[5][0]) #platz 6
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim6 - 4) * timeFade
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim6 == 7: #nich in liste
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[5][0]
                kopie[6][1] = neueOrdnung[5][1]
                kopie[6][2] = neueOrdnung[5][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade
                # -> Es muessen zwei Animationen durchgefueht werden (auf Platz sieben einfaden und anschliessend auf Platz sechs hochtauschen)
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
            #das Lied befindet sich auf dem letzen Platz in der Rangliste
            elif anzAnim6 == 6:    
                # -> Es muessen eine/zwei Animationen durchgefueht werden (Votes gegebenenfalls aktualisieren und auf Platz sechs hochtauschen)
                if kopie[6][2] == neueOrdnung[5][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
                #Die Veraenderung des Arrays waehrend des Tauschens wird simuliert
                TauschenArray (kopie, 5, 6)
            #das Lied ist bereits auf Platz sechs des Rankings zu finden
            elif anzAnim6 == 5: 
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[5][2] == neueOrdnung[5][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
            
        #Simulation der Animation fuer den siebten Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim7 = schonda(kopie, neueOrdnung[6][1], neueOrdnung[6][0]) #platz 7
            #erster grober Wert fuer die Dauer der Animationen ermittelt aus der Anzahl der noetigen Tauschanimationen plus der Animation zum aktualisieren der Votes
            animationDauer += (anzAnim7 - 5) * timeFade
            #befindet sich das Lied noch nicht in der Liste, wird es unten eingeblendet und an seinen Platz getauscht
            if anzAnim7 == 7: #nich in liste
                #in die Kopie des Vergleichsarrays die neuen Daten an Platz sieben einfuegen
                kopie[6][0] = neueOrdnung[6][0]
                kopie[6][1] = neueOrdnung[6][1]
                kopie[6][2] = neueOrdnung[6][2]
                #hier hat man eine Animation weniger als oben berechnet wurde, da das Aktualisieren der Votes schon mit dem Einblenden des Liedes geschehen ist.
                animationDauer -= 1 * timeFade
                # -> Es muss eine Animatione durchgefueht werden (auf Platz sieben einfaden)
                #Die Veraenderung des Arrays ist bereits oben beim Ueberschreiben der Daten gemacht worden
            #das Lied befindet sich bereits auf dem letzen Platz in der Rangliste
            elif anzAnim7 == 6: 
                # -> Es muss eine Animatione durchgefueht werden, falls sich die Votes veraendert haben, ansonsten keine.
                if kopie[6][2] == neueOrdnung[6][2]:
                    #es ist eine Animation weniger durchzufuehren, da die Votes nicht mehr extra aktualisiert werden muessen
                    animationDauer -= 1 * timeFade
        #Animationsdauer wurde grob berechnet
            #falls die Animationsdauer groesser ist, als der oben angegebene Wert, wird die komplette Rangliste aus- und aktualisiert wieder eingeblendet,
            #sonst wird die schrittweise Animation durchgefuehrt
            if (animationDauer > maxAnimationDauer):
                thread.start_new_thread(fadeAnimSongsNormal, (neueOrdnung, 0)) 
            else:
                thread.start_new_thread(updateRanking, (neueOrdnung, 0)) 
  
        #Animation, die die ersten drei Lieder vergroessert, sobald der Countdown auf 0 gesprungen ist     
        def Top3Anim ():
                def topthreeanim():
                    animObj.start()
                       
                animObj = ParallelAnim ([#Relative Anpassung der Positionen der ersten drei Lied-Divs
                                        LinearAnim(self.div1, "pos", 2000, self.div1.pos, (75, a/10)),
                                        LinearAnim(self.div2, "pos", 2000, self.div2.pos, (75, a/4)),
                                        LinearAnim(self.div3, "pos", 2000, self.div3.pos, (75, 2*a/5)),
                                        
                                        #Anpassung der Positionen des Interpreten innerhalb der Song-Divs
                                        LinearAnim(self.platz1b, "pos", 2000, self.platz1b.pos, (33, 70)),
                                        LinearAnim(self.platz2b, "pos", 2000, self.platz2b.pos, (33, 70)),
                                        LinearAnim(self.platz3b, "pos", 2000, self.platz3b.pos, (33, 70)),
                                                                                
                                        #Vergroessern der Schrift der Interpreten
                                        LinearAnim(self.platz1b, "fontsize", 2000, self.platz1b.fontsize, self.platz1b.fontsize + 20),
                                        LinearAnim(self.platz2b, "fontsize", 2000, self.platz2b.fontsize, self.platz2b.fontsize + 20),
                                        LinearAnim(self.platz3b, "fontsize", 2000, self.platz3b.fontsize, self.platz3b.fontsize + 20),
                                                                                
                                        #Vergroessern der Schrift der Songtitel
                                        LinearAnim(self.platz1a, "fontsize", 2000, self.platz1a.fontsize, self.platz1a.fontsize + 30),
                                        LinearAnim(self.platz2a, "fontsize", 2000, self.platz2a.fontsize, self.platz2a.fontsize + 30),
                                        LinearAnim(self.platz3a, "fontsize", 2000, self.platz3a.fontsize, self.platz3a.fontsize + 30),
                                        
                                        #Ausblenden der Spaltenueberschriften 
                                        LinearAnim(self.title, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.votes, "opacity", 2*timeAnim, 1, 0),
                                        
                                        #Ausblenden des Rankings an der linken Bildschirmseite
                                        LinearAnim(self.ranking1, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.ranking2, "opacity", 2*timeAnim, 1, 0), 
                                        LinearAnim(self.ranking3, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.ranking4, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.ranking5, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.ranking6, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.ranking7, "opacity", 2*timeAnim, 1, 0),
                                        
                                        #Ausblenden der Votes der Top 3
                                        LinearAnim(self.platz1c, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.platz2c, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.platz3c, "opacity", 2*timeAnim, 1, 0),
                                        
                                        #Ausblenden der Plaetze vier bis sieben des Rankings
                                        LinearAnim(self.div4, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.div5, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.div6, "opacity", 2*timeAnim, 1, 0),
                                        LinearAnim(self.div7, "opacity", 2*timeAnim, 1, 0)])
                                        
                player.setTimeout(0, topthreeanim)
       
        #Macht die Top3Anim-Animation wieder rueckgaengig, d.h. die ersten drei Lider werden wieder auf eine normale Groesse gebracht und der Rest wird wieder eingeblendet
        def fadeAnimSongsTop3 (neueOrdnung, null):
            time.sleep(0.1)
        #Abfangen von Randfaellen
            #Es wurde noch nichts hinzugefuegt
            if neueOrdnung[0][0] == " " and neueOrdnung[0][1] == " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung = deepcopy(self.alteOrdnung)
            #Es befindet sich nur ein Lied in der Liste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[1][0] = "-1-"
                neueOrdnung[1][1] = "-1-"
                neueOrdnung[1][2] = "0"
                neueOrdnung[2][0] = "-2-"
                neueOrdnung[2][1] = "-2-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-3-"
                neueOrdnung[3][1] = "-3-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-4-"
                neueOrdnung[4][1] = "-4-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-5-"
                neueOrdnung[5][1] = "-5-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-6-"
                neueOrdnung[6][1] = "-6-"
                neueOrdnung[6][2] = "0"
            #Es wurden zwei Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[2][0] = "-1-"
                neueOrdnung[2][1] = "-1-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-2-"
                neueOrdnung[3][1] = "-2-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-3-"
                neueOrdnung[4][1] = "-3-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-4-"
                neueOrdnung[5][1] = "-4-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-5-"
                neueOrdnung[6][1] = "-5-"
                neueOrdnung[6][2] = "0"
            #Drei Lieder wurden uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[3][0] = "-1-"
                neueOrdnung[3][1] = "-1-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-2-"
                neueOrdnung[4][1] = "-2-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-3-"
                neueOrdnung[5][1] = "-3-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-4-"
                neueOrdnung[6][1] = "-4-"
                neueOrdnung[6][2] = "0"
            #Es befinden sich vier Lieder in der Argumentliste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[4][0] = "-1-"
                neueOrdnung[4][1] = "-1-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-2-"
                neueOrdnung[5][1] = "-2-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-3-"
                neueOrdnung[6][1] = "-3-"
                neueOrdnung[6][2] = "0"
            #fuenf Lieder als Eingabe
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[5][0] = "-1-"
                neueOrdnung[5][1] = "-1-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-2-"
                neueOrdnung[6][1] = "-2-"
                neueOrdnung[6][2] = "0"
            #Es wurden sechs Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[6][0] = "-1-"
                neueOrdnung[6][1] = "-1-"
                neueOrdnung[6][2] = "0"
            #Es wurde ein komplett volles Array uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] != " " and neueOrdnung[6][1] != " ":
                pass
            
            #blendet die ersten drei Lieder wieder aus
            fadeOut(self.div1, timeAnim)
            fadeOut(self.div2, timeAnim)
            fadeOut(self.div3, timeAnim)
            time.sleep(timeFade)
            
        #Wiederherstellen der Ausgangswerte
            #setzt die Positionen der ersten drei Divs wieder zurueck
            self.div1.pos = (a/18,b/6)
            self.div2.pos = (a/18,b/3.5175)
            self.div3.pos = (a/18,b/2.495)
            self.div4.pos = (a/18,b/1.935)
            self.div5.pos = (a/18,b/1.58)
            self.div6.pos = (a/18,b/1.335)
            self.div7.pos = (a/18,b/1.155)
            
            #passt die Positionen der Interpreten innerhalb der Divs wieder an
            self.platz1b.pos = (33, 40) 
            self.platz2b.pos = (33, 40)
            self.platz3b.pos = (33, 40)
            
            #setzt die Schriftgroessen wieder auf die alten Werte
            self.platz1a.fontsize = 30 
            self.platz2a.fontsize = 30
            self.platz3a.fontsize = 30
            self.platz1b.fontsize = 20
            self.platz2b.fontsize = 20
            self.platz3b.fontsize = 20
            
            #Ueberschreibt die Inhalte der Wordsnodes aller sieben Lieder mit dem uebergebenen neuen Array
            self.platz1a.text= neueOrdnung[0][1]
            self.platz2a.text= neueOrdnung[1][1]
            self.platz3a.text= neueOrdnung[2][1]
            self.platz4a.text= neueOrdnung[3][1]
            self.platz5a.text= neueOrdnung[4][1]
            self.platz6a.text= neueOrdnung[5][1]
            self.platz7a.text= neueOrdnung[6][1]
                
            self.platz1b.text= neueOrdnung[0][0]
            self.platz2b.text= neueOrdnung[1][0]
            self.platz3b.text= neueOrdnung[2][0]
            self.platz4b.text= neueOrdnung[3][0]
            self.platz5b.text= neueOrdnung[4][0]
            self.platz6b.text= neueOrdnung[5][0]
            self.platz7b.text= neueOrdnung[6][0]
             
            self.platz1c.text= neueOrdnung[0][2]
            self.platz2c.text= neueOrdnung[1][2]
            self.platz3c.text= neueOrdnung[2][2]
            self.platz4c.text= neueOrdnung[3][2]
            self.platz5c.text= neueOrdnung[4][2]
            self.platz6c.text= neueOrdnung[5][2]
            self.platz7c.text= neueOrdnung[6][2]
            
            #aktualisiert das Vergleichsarray
            self.alteOrdnung = deepcopy(neueOrdnung)
           
            #blendet alle sieben Lied-Divs wieder ein
            fadeIn(self.div1, timeAnim)
            fadeIn(self.div2, timeAnim)
            fadeIn(self.div3, timeAnim)
            fadeIn(self.div4, timeAnim)
            fadeIn(self.div5, timeAnim)
            fadeIn(self.div6, timeAnim)
            fadeIn(self.div7, timeAnim)
            
            #blendet die Votes der Top 3 wieder ein
            fadeIn(self.platz1c, timeAnim)
            fadeIn(self.platz2c, timeAnim)
            fadeIn(self.platz3c, timeAnim)
            
            #blendet das Ranking wieder ein
            fadeIn(self.ranking1, timeAnim)
            fadeIn(self.ranking2, timeAnim)
            fadeIn(self.ranking3, timeAnim)
            fadeIn(self.ranking4, timeAnim)
            fadeIn(self.ranking5, timeAnim)
            fadeIn(self.ranking6, timeAnim)
            fadeIn(self.ranking7, timeAnim)
            
            #blendet die Spaltenueberschriften wieder ein
            fadeIn(self.title, 2*timeAnim),
            fadeIn(self.votes, 2*timeAnim),

    
    #Alle noetigen Definitionen fuer die Anzeige und Animation auf der rechten Seite
    
        #Initialisiert den rechten Teil des Bildschirms, auf dem die Baltenanimation laufen wird.
        def right():
            #Initialisert den Hintergrung der rechten Seite
            self.divNode=avg.DivNode(pos=(a-2*(a/4.25),(b/11)), size=(2*(a/4.25),b),parent=self.rootNode)
            self.rightr=avg.RectNode (pos=(0,0), size=(2*(a/4.25), b), parent=self.divNode, color="000000", fillcolor="46464B", fillopacity=1)
            self.ersterPunkte=avg.WordsNode(pos=(74,5), text="0000", parent=self.divNode, font='marketing script', color="E9EBFF", fontsize=40)
            breite = 2*(a/4.25)
            
            #Initialisert ein Vergleichsarray fuer die spaetere Animationen 
            self.leute=[]
            self.leute.append([" ", "0"])
            self.leute.append([" ", "0"])
            self.leute.append([" ", "0"])
            
            #Initialisert Name und Balken der drei angezeigten User im Ranking
            self.divNode1=avg.DivNode(pos=(50,0), size=((breite/3),b-50),parent=self.divNode)
            self.erster=avg.RectNode(pos=(50,50+(b-250)-5), size=(30,5), parent=self.divNode1, color="EDEDC1", fillcolor="FFFFCD", fillopacity=1)
            self.ersterName=avg.WordsNode(pos=(50,900), text=" " ,parent=self.divNode1, font='marketing script', color="E9EBFF", fontsize=35)
            self.ersterName.text=self.leute[0][0]
            
            self.divNode2=avg.DivNode(pos=((breite/2.5),0), size=((breite/2.5),b-50),parent=self.divNode)
            self.zweiter=avg.RectNode(pos=(50,50+(b-250)-5), size=(30,5), parent=self.divNode2, color="EDEDC1", fillcolor="FFFFCD", fillopacity=1)
            self.zweiterName=avg.WordsNode(pos=(50,900), text=" " ,parent=self.divNode2, font='marketing script', color="E9EBFF", fontsize=35)
            self.zweiterName.text=self.leute[1][0]
            
            self.divNode3=avg.DivNode(pos=((breite-(breite/3.5)),0), size=((breite/3.5),b-50),parent=self.divNode)
            self.dritter=avg.RectNode(pos=(50,50+(b-250)-5), size=(30,5), parent=self.divNode3, color="EDEDC1", fillcolor="FFFFCD",fillopacity=1)      
            self.dritterName=avg.WordsNode(pos=(50,900), text=" " ,parent=self.divNode3, font='marketing script', color="E9EBFF", fontsize=35)
            self.dritterName.text=self.leute[2][0]
          
        
       
        
        #Fuehrt bei der rechten Seite die Animation der Top 3 User aus
        def recievedpunkte(neueLeute, null):
            #Faengt Randfall ab, dass es noch keinen User gibt
            if neueLeute[0][0]==" " and neueLeute[1][0] == " " and neueLeute[2][0] == " ":
                return 0
            #Faengt Randfall ab, falls einer der User 0 Punkte hat wird er auf 5 gesetzt, um den Balken noch sichtbar zu machen
            if neueLeute[0][1] == "0":
                return 0
            if neueLeute[1][1] == "0":
                neueLeute[1][1] = "5"
                neueLeute[1][0] = " "
            if neueLeute[2][1] == "0":
                neueLeute[2][1] = "5"
                neueLeute[2][0] = " "
            #Die DivNodes um die Balken, sowie die Punkteanzahl des Ersten werden ausgeblendet    
            fadeOut(self.divNode1, 2000)
            fadeOut(self.divNode2, 2000)
            fadeOut(self.divNode3, 2000)
            fadeOut(self.ersterPunkte, 2000)
            time.sleep(2)
            
            #Die Werte werden eingelesen
            PunkteErster = neueLeute[0][1]
            PunkteErster = float(PunkteErster)
         
            PunkteZweiter = neueLeute[1][1]
            PunkteZweiter = float(PunkteZweiter)
         
            PunkteDritter = neueLeute[2][1]
            PunkteDritter = float(PunkteDritter)
        
            if PunkteErster ==0:
                PunkteErster=5
                balkenposy=b/1.3
                Hundertprozent = 5
                Punktezweiter = 5
                Punktedritter = 5
            #Hat mindestens der Erste Punkte erhalten, so wird die Hundertprozent angepasst und die Groessen und Positionen der anderen beiden Balken wird relativ dazu berechnet.
            else:
                balkenposy=50
                Hundertprozent=b-250
                Punktezweiter = (Hundertprozent/PunkteErster)*PunkteZweiter
                Punktedritter = (Hundertprozent/PunkteErster)*PunkteDritter
           
            
            #Der Balken und Name des Ersten wird aktualisert
            self.erster.pos = (50, balkenposy)
            self.erster.size = (30, Hundertprozent)
            self.ersterName.text = neueLeute[0][0]
            #Die Punkte des Ersten werden aktualisiert
            if PunkteErster > 999:
                self.ersterPunkte.text = str(int(PunkteErster))
            elif PunkteErster > 99:
                self.ersterPunkte.text = "0" + str(int(PunkteErster))
            elif PunkteErster > 9:
                self.ersterPunkte.text = "00" + str(int(PunkteErster))
            else:
                self.ersterPunkte.text = "000" + str(int(PunkteErster))
                
            #Die Balken des Zweiten und Drittens werden gebaut    
            if neueLeute[1][1] != "5":
                self.zweiter.pos = (50, 50+(b-250)-Punktezweiter)
                self.zweiter.size = (30, Punktezweiter)
                self.zweiterName.text = neueLeute[1][0]
                
            if neueLeute[2][1] != "5":
                self.dritter.pos = (50, 50+(b-250)-Punktedritter)
                self.dritter.size = (30, Punktedritter)
                self.dritterName.text = neueLeute[2][0]
            #Nacheinander wird das ganze eingeblendet
            time.sleep(2)
            
            fadeIn(self.divNode3, 2000)
            time.sleep(2)
            
            time.sleep(1)
            
            fadeIn(self.divNode2, 2000)
            time.sleep(2)
            
            time.sleep(1)
            
            fadeIn(self.divNode1, 2000)
            fadeIn(self.ersterPunkte, 2000)
            time.sleep(2)
            
       
                
    #Deklarationen der allgemeinen Methoden, u.a. zur Kommunikation ueber den WebSocket

        #Wandelt den Eingabestring in ein zweidimensionales Array um, indem er an den entsprechenden Zeichenfolgen gesplittet wird.
        def builtArrayOutOfString(rcvstring): 
            #Splittet zuerst an der Zeichenfolge "!#!".
            stringinput = rcvstring.split("!#!")
            #Berechnet die Laenge des ersten gesplitteten Stringarrays.
            ArrayLen = len(stringinput)
            #Erstellt ein leeren Array.
            stringarray=[]
            #Falls das Array die Laenge sieben hat, muss jeder neu entstandene String nach dem ersten Split in drei kleinere Strings zerlegt werden
            #und diese dann als zweite Dimension an das leere Array von oben angefuegt werden.
            if (ArrayLen ==7):
                #geht durch das Stringarray.
                for i in range(0,ArrayLen):
                    string = stringinput[i]
                    #Splittet jeden Teil an "##"
                    string2 = string.split("##")
                    #Fuegt dies dem neuen Array in der zweiten Dimension mit der Form "Interpret, Titel, Votes" hinzu.
                    stringarray.append([string2[0],string2[1],string2[2]]) 
                return stringarray
            #Falls das Array die Laenge drei hat, muss jeder neu entstandene String nach dem ersten Split in zwei kleinere Strings zerlegt werden
            #und diese dann als zweite Dimension an das leere Array von oben angefuegt werden.
            if (ArrayLen==3):
                #geht durch das Stringarray.
                for i in range(0,ArrayLen):
                    string = stringinput[i]
                    #Splittet jeden Teil an "##"
                    string2 = string.split("##")
                    #Fuegt dies dem neuen Array in der zweiten Dimension mit der Form "Username, Punkte" hinzu.
                    stringarray.append([string2[0],string2[1]])
                return stringarray
           
        #Funktion, die auf Grund der Laenge des uebergebenen Arrays die aufzurufende Methode bestimmt.   
        def checkLenArray(str_builtArrayOutofString):
            #Berechnet die Laenge des Arrays.
            ArrayLen=len(str_builtArrayOutofString)
            #Entscheidet, an welche Funktion das Array uebergeben werden soll. 
            if (ArrayLen == 7):
                #Ist die Laenge sieben, so handelt es sich um ein Update fuer das Lieder-Ranking und die Methode "animationUpdate" wird aufgerufen.
                animationUpdate(str_builtArrayOutofString)
            elif (ArrayLen==3):
                #Ist die Laenge drei, so handelt es sich um ein Update fuer das User-Ranking und die Methode "recievedpunkte" wird aufgerufen.
                thread.start_new_thread(recievedpunkte,(str_builtArrayOutofString,0))
            #Andernfalls wurde ein falsches Array uebergeben, das wir nicht weiter verarbeiten koennen.
            else: 
                pass
            
        #Initialisert den Countdown 
        def countdown(m,s):
            
            #Rechnet die Minuten und Sekunden in Sekunden um.
            def MsToSecs(m,s):
                return m*60 + s
            
            #Rechnet die Sekunden in Minuten und Sekunden um.
            def secsToMs(secs):
                mins = secs//60
                secs -= mins*60
                mins = str(mins)
                secs = str(secs)
                return mins,secs
            
            #Rechnet das Argument in Sekunden um.
            seconds = MsToSecs(m,s)
            #Startet eine Endlosschliefe (da wir unten sicher stellen, dass die Sekunden immer groesser als 0 sind), die den Countdown animiert.
            while seconds >= 0:
                #Wartet eine Sekunde.
                time.sleep(1)
                #Anschliessend wird der Sekundenwert um eins herabgesetzt.
                seconds -= 1
                #Sollte der Wert jetzt negativ werden, so wird der Countdown zurueckgesetzt.
                if seconds ==-1:
                    seconds = 119
                #Rechnet die Sekunden wieder in Minuten und Sekunden um.
                (mint,sect)=secsToMs(seconds)
                #Sorgt fuer eine korrekte Darstellung des Countdowns auf dem Screen.
                if int(sect) < 10 and int (mint)<10:
                    self.timer.text="Countdown "+"0"+mint+":" +"0"+sect 
                elif int(sect) <10:
                    self.timer.text="Countdown "+mint+":"+"0"+sect
                elif int(mint) <10:
                    self.timer.text="Countdown "+"0"+mint+":"+sect    
                else: 
                    self.timer.text="Countdown " + mint + ":" + sect
                  
        #Startet den WebSocket
        def initializeWebSocket():
            log.startLogging(sys.stdout)
            #Initialisert den WebSocket als neuen WebSocket, der mit dem Port 9034 auf dem Server kommunizieren soll.
            self.receiver = WebSocketClientFactory("ws://" + serverip + ":9034", debug = False)
            #Verbindet den WebSocket mit der WebSocket-Klasse, in der alle Methoden enthalten sind
            self.receiver.protocol=MessageBasedHashClientProtocol
            #Verbindet den Screen mit mit dem WebSocket
            connectWS(self.receiver)
            #Ermoeglicht Multithreading
            reactor.run(installSignalHandlers=0)
        
        #Ruft die Mehoden auf, die die linke und rechte Bildschirmseite initialisieren
        left()
        right()
        #testarray = [["Kirstin","100"],["Sabine","70"],["Alex", "30"]]
        #thread.start_new_thread(recievedpunkte,(testarray, 0))
        #Startet den WebSocket in einem neuen Tread
        thread.start_new_thread(initializeWebSocket,())

        #Klasse, die die Methoden zur Webkommunikation bereitstellt
        class MessageBasedHashClientProtocol(WebSocketClientProtocol):
            
            #Sendet bei Aufruf "PYCLIENT: " an den Server, damit dieser die IP des Screens von den Handy-IPs unterscheiden kann.
            def sendClientName(self):
                data = "PYCLIENT: "
                self.sendMessage(data, binary = True)
                
            #Ruft beim Start des Pyclients die Sende-Methode auf.
            def onOpen(self):
                self.sendClientName()
            
            #Verarbeitet die Nachrichten, die vom Server gesendet werden.
            def onMessage(self, message, binary):
                #Wird die Nachricht "START" gesendet, so wird der Countdown des Screens in einem neuen Thread geoeffnet
                if (message=="START"):
                    global countvar
                    countvar=thread.start_new_thread(countdown, zeit)
                #Wird eine Nachricht gesendet, deren erste fuenf Buchstaben "FINAL" sind, wird die Liste noch einmal mittels einer FadoOut-FadeIn-Animation
                #aktualisert und anschliessend die Top3-Animatino durchgefuehrt. Diese Funktion wird immer ausgefuehrt, wenn der Countdown des DJs auf 0:0 springt.
                elif (message[:5] == "FINAL"):
                    #Fuehrt die Aktualisierung des Rankings als Animation durch.
                    fadeAnimSongsNormal(builtArrayOutOfString(message[5:]), 0)
                    time.sleep(2*timeFade)
                    #Ruft die Animation auf, die die Top 3 vergroessert.
                    Top3Anim()
                #Enthaelt die Nachricht den Praefix "PLAYED", so wird die vorher ausgefuehrte Top3-Animation wieder rueckgaengig gemacht. Diese Nachricht
                #wird immer geschickt, wenn der DJ auf "Top 3 gespielt" klickt.
                elif (message[:6] == "PLAYED"):
                    fadeAnimSongsTop3(builtArrayOutOfString(message[6:]), 0) 
                #Der Praefix "PYMESG" signalisiert, dass kein besonderes Event vorliegt, sondern einfach nur das Song- oder User-Ranking ein Update erhaelt.
                #Es wird alle 30 Sekunden eine solche Nachricht geschickt, die dann in der aufgerufenen Methode weiter verarbeitet wird.
                elif (message[:6] == "PYMESG"):
                    checkLenArray(builtArrayOutOfString(message[6:]))
                  
#Funktion, die die Aufloesung des Bildschirms ausliest
if __name__=='__main__':
    print "Bitte IP des Servers eingeben:"
    while True:
            x = raw_input()
            serverip = x
            break
# die auskommentierten Methoden unten lesen unter Windows die Aufloesung aus dem Computer heraus und starten den Bildschirm mit der entsprehcenden Aufloesung
#         user32 = ctypes.windll.user32
#         screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#         screen.start(resolution=(screensize[0], screensize[1]))
    screen.start(resolution=(1920, 1080))