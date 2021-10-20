from kivy import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '300')
Config.set('graphics', 'minimum_height', '400')

import sqlite3
from kivy.app import App
from kivy.core import text
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from random import randint
from functools import partial
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
import time
from datetime import date, datetime

class SoloWindow(Screen):
    game = 0 #wybrana gra:
    """
    0 - 180
    1 - 301
    2 - 501
    3 - 701
    4 - min
    5 - max
    6 - trening
    7- trening losowy
    """
    def choose(self,index): #wybór gry, parametr index przekazywany z .kv
        if index >=0 and index <=3:
            if index == 0:
                self.manager.get_screen('solo180701').leftLabel.text = "180"
                self.manager.get_screen('solo180701').playerPoints = 180
                self.game = index
            elif index == 1:
                self.manager.get_screen('solo180701').leftLabel.text = "301"
                self.game = index
                self.manager.get_screen('solo180701').playerPoints = 301
            elif index == 2:
                self.manager.get_screen('solo180701').leftLabel.text = "501"
                self.game = index
                self.manager.get_screen('solo180701').playerPoints = 501
            elif index == 3:
                self.manager.get_screen('solo180701').leftLabel.text = "701"
                self.game = index
                self.manager.get_screen('solo180701').playerPoints = 701

            App.get_running_app().root.transition.direction = "left"  
            App.get_running_app().root.current = "solo180701"
            return
        elif index >=4 and index <=5:
            self.game = index
            App.get_running_app().root.transition.direction = "left"  
            App.get_running_app().root.current = "minmaxwindow"

class MinmaxWindow(Screen):
    multiplierList = [] #
    navbarList = [] #0-leftLabel, 1-avgLabel, 2-sumLabel
    throwSum = 0
    left = rounds = 20
    throwCount = 0
    bindbtn = 0 #parametr blokujący podwójne przypisanie funkcji do buttons
    ones = 0
    twenties = 0
    avg = 0
    scores = {} #wynik końcowy

    def bindButton(self,j):
        multiplier = 1 
        if self.multiplierList[1].active:
            multiplier = 2
        if self.multiplierList[2].active:
            multiplier = 3

        if int(j) == 25 or int(j) == 50: #25 oraz 50 nie maja mnożnika
            multiplier = 1
        if self.left > 1: #dopóki zostaną rzuty
            self.throwSum += int(j) * multiplier
            self.navbarList[2].text = str(self.throwSum)
            if int(j) == 0: #nietrafienie w tarczę w grzę min oznacza kare 70 punktów 
                if self.manager.get_screen('solo').game == 4: #gra min
                    self.throwSum += 70
                    self.navbarList[2].text = str(self.throwSum)  
            self.throwCount += 1
            self.navbarList[1].text = str(round(float(self.throwSum)/float(self.throwCount),2))
            self.left -= 1
            self.navbarList[0].text = str(self.left)

            x = Label()
            x.text = str (int(j) * multiplier)
            self.thrownGrid.add_widget(x) #dopisywanie do listy rzutów
            if int(j) == 1:
                self.ones += 1
            elif int(j) == 20:
                self.twenties += 1
        else:
            """dopisywanie ostatnich rzutów"""
            self.throwSum += int(j)*multiplier
            self.throwCount += 1
            self.avg = round(float(self.throwSum)/float(self.throwCount),2)
            if int(j) == 1:
                self.ones += 1
            elif int(j) == 20:
                self.twenties += 1 

            if self.manager.get_screen('solo').game == 4:
                self.scores['Gra'] = 'Min'
            elif self.manager.get_screen('solo').game == 5:
                self.scores['Gra'] = 'Max'
            self.scores['Liczba rzutów'] = self.throwCount
            self.scores['Średnia rzutów'] = self.avg
            self.scores['Suma'] = self.throwSum
            self.scores['Liczba 1'] = self.ones
            self.scores['Liczba 20'] = self.twenties

            App.get_running_app().root.transition.direction = "left"  
            App.get_running_app().root.current = "soloscoreboard"

    def create(self):
        for i in self.children:
            if (hasattr(i, 'buttonsGrid')): #dopisywanie mnożników do listy
                self.multiplierList.append(i.boxx1)
                self.multiplierList.append(i.boxx2)
                self.multiplierList.append(i.boxx3)
                break
        self.navbarList.append(self.leftLabel) #dopisywanie wartości wyświetlanych
        self.navbarList.append(self.avgLabel)
        self.navbarList.append(self.sumLabel)

        if self.bindbtn == 0: #bindowanie buttonow tylko raz
            self.bindbtn = 1
            for i in self.children:
                if (hasattr(i, 'buttonsGrid')):
                    temp = []
                    for j in range (0,21):
                        temp.append(getattr(i, 'button'+str(j))) 
                        temp[j].bind(on_release = lambda x: self.bindButton(x.text))
                    temp.append(getattr(i, 'button25')) 
                    temp[21].bind(on_release = lambda x: self.bindButton(x.text))
                    temp.append(getattr(i, 'button50')) 
                    temp[22].bind(on_release = lambda x: self.bindButton(x.text))

class Solo180701(Screen):
    multiplierList = []
    navbarList = [] #0-leftLabel, 1-countLabel, 2-avgLabel
    playerPoints = 0
    throwCount = 0
    throwSum = 0
    bindbtn = 0
    sixties = 0
    fiftysevens = 0
    scores = {}
    avg = 0
    game = '' #gra wpisywana w create do przekazani na screen wyniku

    def bindButton(self,j):
        multiplier = 1 
        if self.multiplierList[1].active:
            multiplier = 2
        if self.multiplierList[2].active:
            multiplier = 3

        if int(j) == 25 or int(j) == 50: #25 oraz 50 nie maja mnożnika
            multiplier = 1

        if self.playerPoints - int(j)*multiplier > 0:
            self.playerPoints -= int(j)*multiplier
            self.throwSum += int(j)*multiplier
            self.navbarList[0].text = str(self.playerPoints)
            self.throwCount +=1
            self.navbarList[1].text = str(self.throwCount)
            self.navbarList[2].text = str(round(float(self.throwSum)/float(self.throwCount),2))

            if int(j) * multiplier == 57:
                self.fiftysevens += 1

            if int(j) * multiplier == 60:
                self.sixties += 1

        elif self.playerPoints - int(j)*multiplier == 0: #zakończenie rozgrywki
            self.throwSum += int(j)*multiplier
            self.throwCount += 1
            self.avg = round(float(self.throwSum)/float(self.throwCount),2)

            self.scores['Gra'] = self.game
            self.scores['Liczba rzutów'] = self.throwCount
            self.scores['Średnia rzutów'] = self.avg
            self.scores['Liczba 60'] = self.sixties
            self.scores['Liczba 57'] = self.fiftysevens

            App.get_running_app().root.transition.direction = "left"  
            App.get_running_app().root.current = "soloscoreboard"
            
        else: #przypadek gdy gracz przekroczy wartośc docelową
            pass

    def create(self):
        for i in self.children:
            if (hasattr(i, 'buttonsGrid')):
                self.multiplierList.append(i.boxx1)
                self.multiplierList.append(i.boxx2)
                self.multiplierList.append(i.boxx3)
                break
        self.navbarList.append(self.leftLabel)           
        self.navbarList.append(self.countLabel)
        self.navbarList.append(self.avgLabel)

        if self.bindbtn == 0:
            self.bindbtn = 1
            for i in self.children:
                if (hasattr(i, 'buttonsGrid')):
                    temp = []
                    for j in range (0,21):
                        temp.append(getattr(i, 'button'+str(j))) 
                        temp[j].bind(on_release = lambda x: self.bindButton(x.text))
                    temp.append(getattr(i, 'button25')) 
                    temp[21].bind(on_release = lambda x: self.bindButton(x.text))
                    temp.append(getattr(i, 'button50')) 
                    temp[22].bind(on_release = lambda x: self.bindButton(x.text))
        self.game = str(self.leftLabel.text)


class Records(Screen):
    pass

class Database(Screen):
    
    def find(self):
        self.databaseGrid.clear_widgets()
        game = self.gameSpinner.text
        user = self.userInput.text
         
        connection = sqlite3.connect('dart.db') #otwarcie połaczenia z bazą
        cursor = connection.cursor()
        """wpisanie nagłówków oraz nazwy tabeli dla konkretnych gier"""
        if game in ('180','301','501','701'):
            databasetable = 'solo180701'
            headers = ['Numer','Data','Użytkownik','Gra','Liczba rzutów','Średnia rzutu','Liczba 60','Liczba 57',]
        elif game in ('Min','Max'):
            headers = ['Numer','Data','Użytkownik','Gra','Liczba rzutów','Średnia rzutu','Liczba 1','Liczba 20',]
            databasetable = 'minmax'
        
        try:
            if user == '':
                cursor.execute("SELECT * from "+databasetable+" WHERE game = ?", (game,))
            else:
                cursor.execute("SELECT * from "+databasetable+" WHERE game = ? and user = ?", (game,user,))
            result = cursor.fetchall()
            self.databaseGrid.cols = len(result[0]) #dynamiczne tworzenie liczby kolumn względem odpowiedniej tabeli z db
            for i in headers:
                x = Label()
                x.text = i
                self.databaseGrid.add_widget(x)
            for i in result:
                for j in i:
                    x = Label()
                    x.text = str(j)
                    self.databaseGrid.add_widget(x)
        except:
            self.databaseGrid.cols = 1
            x = Label()
            x.text = 'Brak danych w bazie na podane parametry'
            self.databaseGrid.add_widget(x)
                
           
    def backFunction(self):
        self.databaseGrid.clear_widgets()
        self.gameSpinner.text = 'Wybierz gre'
        self.userInput.text = ''
        App.get_running_app().root.current = "solo"
        App.get_running_app().root.transition.direction = "right" 


class GameWindow(Screen):

    navbarList = [] #0 - sumLabel, 1 - roundLabel, 2 - leftLabel
    playersNamesList = [] #lista graczy
    playersPointsList = []  #lista punktow graczy, id te same
    playersPointsListTemp = [] #czasowe przechowywanie punktów graczy na wypadek wyrzucenia zbyt dużej liczby punktów
    multiplierList = []
    playersCount = 0 #liczba graczy
    currentPlayer = 0 #id obecnego gracza
    placeList = {} #lista miejsc graczy
    eliminator = 0 #czy gra to eliminator, 1 to eliminator, 2 to min, 3 to max
    game = 0 #ktora gra
    roundsCount = 0 #liczba rund dla gier min-max
    round = 1 
    finish = 0 #kontolna zmienna by nie powielać kroku gdy zakonczy sie runde przed trecim rzutem
    left = 3
    bindbtn = 0 #by nie nadpisywac buttonow przy ponownej grze
    def bindButton(self,j):  
        self.finish = 0
        multiplier = 1 
        if self.multiplierList[1].active:
            multiplier = 2
        if self.multiplierList[2].active:
            multiplier = 3
        self.left -= 1

        if int(j) == 25 or int(j) == 50: #25 oraz 50 nie maja mnożnika
            multiplier = 1
        
        if self.eliminator == 0: #gra klasyczna 180-701
            if self.left == 2:
                self.navbarList[0].text = '0'
                self.navbarList[0].color = (1, 1, 1, 1)
                self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
            if self.left != 0: #dopóki gracz ma >1 rzut
                    self.navbarList[2].text = str(self.left)
                    if int(self.playersPointsList[self.currentPlayer].text) - int(j)*multiplier > 0: #czy rzut nie przekracza 0
                        self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
                    elif int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier) == 0: #konczymy gre po koncu rundy
                        self.playersPointsList[self.currentPlayer].text = '0'
                        self.placeList[self.playersNamesList[self.currentPlayer].text] = self.playersPointsList[self.currentPlayer].text
                        self.left = 0
                        self.finish = 1 #zaznaczenie, że gra skończy się po danej rundzie
                    else: #przekroczylo 0
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                        self.left = 0

            if self.left == 0: #ostatni rzut
                self.left = 3
                self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                if self.finish == 0:
                    if int(self.playersPointsList[self.currentPlayer].text) - int(j)*multiplier > 0:
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
                    elif int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier) == 0:
                        self.playersPointsList[self.currentPlayer].text = '0'
                        self.placeList[self.playersNamesList[self.currentPlayer].text] = self.playersPointsList[self.currentPlayer].text
                    else:
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                    
                    self.playersPointsListTemp[self.currentPlayer] = int(self.playersPointsList[self.currentPlayer].text)
                    
                if self.currentPlayer >= self.playersCount-1:
                    self.round += 1
                    if self.placeList: #koniec gry gdy przynajmniej jeden gracz zdobędzie wymaganą liczbę punktów
                        for i in range (0,len(self.playersNamesList)):
                            if self.playersNamesList[i].text not in self.placeList:
                                self.placeList[self.playersNamesList[i].text] = self.playersPointsList[i].text
                        print('koniec')
                        App.get_running_app().root.transition.direction = "left"  
                        App.get_running_app().root.current = "scoreboard"
                        self.navbarList[0].text = '0'
                        self.navbarList[1].text = '1'
                        self.navbarList[2].text = '3'#wartosci domyslne do nowej gry
                        return
                        
                self.navbarList[0].color = (1,0,1,1)#zmiana koloru przy następnym graczu
                self.navbarList[1].text = str(self.round)
                self.navbarList[2].text = str(self.left)

                if self.currentPlayer >= self.playersCount-1: #powrót do pierwszego gracza po rzutach ostatniego
                    self.currentPlayer = 0
                    self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
                    self.playersNamesList[self.playersCount-1].color = (1,1,1,1)
                else:
                    self.currentPlayer+=1
                    self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
                    self.playersNamesList[self.currentPlayer-1].color = (1,1,1,1)
            
        elif self.eliminator == 1: #eliminator 180701
            self.finish = 0
            if self.left == 2:
                self.navbarList[0].text = '0'
                self.navbarList[0].color = (1, 1, 1, 1)
                self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
            if self.left != 0:
                    self.navbarList[2].text = str(self.left)
                    if int(self.playersPointsList[self.currentPlayer].text) + int(j)*multiplier < self.game: #czy rzut nie przekracza maxa
                        self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) + (int(j)*multiplier))

                        for i in self.playersPointsList: #zerowanie graczy 
                            if i!= self.playersPointsList[self.currentPlayer]:
                                if int(self.playersPointsList[self.currentPlayer].text) == int(i.text):
                                    i.text = '0'

                    elif int(self.playersPointsList[self.currentPlayer].text) + (int(j)*multiplier) == self.game: #tutaj dodajemy do listy zwyciezce
                        self.playersPointsList[self.currentPlayer].text = str(self.game)
                        self.placeList[self.playersNamesList[self.currentPlayer].text] = self.playersPointsList[self.currentPlayer].text
                        self.left = 0
                        self.finish = 1
                    else: #przekroczylo 0
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                        self.left = 0

            if self.left == 0:
                self.left = 3

                self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                if self.finish == 0:    
                    if int(self.playersPointsList[self.currentPlayer].text) + int(j)*multiplier < self.game:
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) + (int(j)*multiplier))

                        for i in self.playersPointsList: #zerowanie graczy 
                            if i!= self.playersPointsList[self.currentPlayer]:
                                if int(self.playersPointsList[self.currentPlayer].text) == int(i.text):
                                    i.text = '0'

                    elif int(self.playersPointsList[self.currentPlayer].text) + (int(j)*multiplier) == self.game:
                        self.playersPointsList[self.currentPlayer].text = str(self.game)
                        self.placeList[self.playersNamesList[self.currentPlayer].text] = self.playersPointsList[self.currentPlayer].text
                    else:
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                    
                    self.playersPointsListTemp[self.currentPlayer] = int(self.playersPointsList[self.currentPlayer].text)
                

                if self.currentPlayer >= self.playersCount-1:
                    self.round += 1
                    if self.placeList: #zakonczenie gry
                        print('koniec gry')
                        for i in range (0,len(self.playersNamesList)):
                            if self.playersNamesList[i].text not in self.placeList:
                                self.placeList[self.playersNamesList[i].text] = self.playersPointsList[i].text
                        print(self.placeList)
                        App.get_running_app().root.transition.direction = "left"  
                        App.get_running_app().root.current = "scoreboard"


                self.navbarList[0].color = (1,0,1,1) #zmiana koloru przy następnym graczu
                self.navbarList[1].text = str(self.round)
                self.navbarList[2].text = str(self.left)

                if self.currentPlayer >= self.playersCount-1:
                    self.currentPlayer = 0
                    self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
                    self.playersNamesList[self.playersCount-1].color = (1,1,1,1)
                else:
                    self.currentPlayer+=1
                    self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
                    self.playersNamesList[self.currentPlayer-1].color = (1,1,1,1)
        else: #gra min - max
            if self.left == 2:
                self.navbarList[0].text = '0'
                self.navbarList[0].color = (1, 1, 1, 1)
                self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
            if self.left != 0:
                    self.navbarList[2].text = str(self.left)
                    self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                    self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) + (int(j)*multiplier))

            if self.left == 0:
                self.left = 3
                if self.currentPlayer >= self.playersCount-1:
                    self.roundsCount -= 1

                self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                
                self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) + (int(j)*multiplier))


                if self.roundsCount == 0: #koniec gry
                    print('koniec gry')
                    for i in range (0,len(self.playersNamesList)):
                        self.placeList[self.playersNamesList[i].text] = self.playersPointsList[i].text
                    print(self.placeList)
                    App.get_running_app().root.transition.direction = "left"  
                    App.get_running_app().root.current = "scoreboard"

                self.navbarList[0].color = (1,0,1,1)#zmiana koloru przy następnym graczu
                self.navbarList[1].text = str(self.roundsCount)
                self.navbarList[2].text = str(self.left)

                if self.currentPlayer >= self.playersCount-1:
                    self.currentPlayer = 0
                    self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
                    self.playersNamesList[self.playersCount-1].color = (1,1,1,1)
                else:
                    self.currentPlayer+=1
                    self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
                    self.playersNamesList[self.currentPlayer-1].color = (1,1,1,1)

            
    def create(self):
        for i in self.children:
            if (hasattr(i, 'buttonsGrid')):
                self.multiplierList.append(i.boxx1)
                self.multiplierList.append(i.boxx2)
                self.multiplierList.append(i.boxx3)
                break
        self.usersGrid.clear_widgets()
        count = len(self.manager.get_screen('chooseplayers').playerGrid.children)

        for i in self.children:
            if (hasattr(i, 'sumLabel')):
                self.navbarList.append(i.sumLabel)
                break
        for i in self.children:
            if (hasattr(i, 'roundLabel')):
                self.navbarList.append(i.roundLabel)
                break
        for i in self.children:   
            if (hasattr(i, 'leftLabel')):
                self.navbarList.append(i.leftLabel)
                break

        if self.manager.get_screen('chooseplayers').cb180.active:
            self.game = 180
        elif self.manager.get_screen('chooseplayers').cb301.active:
            self.game = 301
        elif self.manager.get_screen('chooseplayers').cb501.active:
            self.game = 501
        elif self.manager.get_screen('chooseplayers').cb180e.active:
            self.game = 180
            self.eliminator = 1
        elif self.manager.get_screen('chooseplayers').cb301e.active:
            self.game = 301
            self.eliminator = 1
        elif self.manager.get_screen('chooseplayers').cb501e.active:
            self.game = 501
            self.eliminator = 1    
        elif self.manager.get_screen('chooseplayers').cbmax.active:
            self.game = 0
            self.eliminator = 3 
        elif self.manager.get_screen('chooseplayers').cbmin.active:
            self.game = 0
            self.eliminator = 2    
        
        for i in range (count-1,0,-2): #wpisywanie wszystkich graczy na tablice
            x = Label()
            x.text = self.manager.get_screen('chooseplayers').playerGrid.children[i-1].text
            self.usersGrid.add_widget(x)
            x.id = i
            self.playersNamesList.append(x)
            x = Label()
            if self.eliminator == 0:
                x.text = str(self.game)
            else:
                x.text = '0'
            self.usersGrid.add_widget(x)
            x.id = i+1
            self.playersPointsList.append(x)
            if self.eliminator == 0:
                self.playersPointsListTemp.append(self.game)
            else:
                self.playersPointsListTemp.append(0)
        self.playersCount = len(self.playersNamesList)

        if self.playersCount >=2 and self.playersCount <=3: #ustalanie limitu rund dla min-max
            self.roundsCount = 20
        elif self.playersCount >=4 and self.playersCount <=5:
            self.roundsCount = 15
        else:
            self.roundsCount = 10

        if self.eliminator == 2 or self.eliminator == 3:
            self.navbarList[1].text = str(self.roundsCount)

        if self.bindbtn == 0:
            self.bindbtn = 1
            for i in self.children:
                if (hasattr(i, 'buttonsGrid')):
                    temp = []
                    for j in range (0,21):
                        temp.append(getattr(i, 'button'+str(j))) 
                        temp[j].bind(on_release = lambda x: self.bindButton(x.text))
                    temp.append(getattr(i, 'button25')) 
                    temp[21].bind(on_release = lambda x: self.bindButton(x.text))
                    temp.append(getattr(i, 'button50')) 
                    temp[22].bind(on_release = lambda x: self.bindButton(x.text))
                
        self.playersNamesList[0].color = (1,0,0,1)
        self.multiplierList[0].active = True

#klasa zawierajaca funkcje ograniczającą wpisywanie ilości znaków
class MaxLengthInput(TextInput):
    max_characters = NumericProperty(0)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)

#klasa wyboru graczy
class ChoosePlayers(Screen):
    #funkcja tworząca pola do wpisania nazw graczy
    def buttonclicked(self,i):
        self.playerGrid.clear_widgets()
        for i in range (0,i):
            self.playerGrid.add_widget(Label(text='Gracz '+str(i+1)))
            self.playerGrid.add_widget(MaxLengthInput(multiline = False,name = str(i+1),max_characters = 12)) #dlugosc nazwy gracza
        self.manager.get_screen('chooseplayers').confirmButton.disabled = False
        
    #tworzenie przycisków z listą graczy
    def create(self):
        self.chooseGrid.clear_widgets()
        for i in range(2,9):
            x = Button()
            x.text = str(i)
            x.id = i
            self.chooseGrid.add_widget(x)
            x.bind(on_release = lambda x :(self.buttonclicked(x.id)))
    #funkcja weryfikująca czy nazwa któregoś z graczy nie jest pusta
    def validatePlayers(self):
        result = 0
        nameslist = []
        for i in range (0,len(self.playerGrid.children),2):
            nameslist.append(self.playerGrid.children[i].text.lstrip())
        for i in range (0,len(self.playerGrid.children),2):
            if self.playerGrid.children[i].text.lstrip() == '':
              self.playerGrid.children[i+1].color = 1,0,0,1   
              result = 1 #zmienna kontrola gdy któraś nazwa użytkownika jest pusta
            else:
                self.playerGrid.children[i+1].color = 1,1,1,1  
        if result == 1:
            pass
        else:
            self.chooseGrid.clear_widgets()
            App.get_running_app().root.transition.direction = "left"  
            App.get_running_app().root.current = "game"
    
    def backFunction(self):
        self.chooseGrid.clear_widgets()
        self.playerGrid.clear_widgets()
        self.confirmButton.disabled = True
        self.cb180.active = True
        App.get_running_app().root.current = "main"
        App.get_running_app().root.transition.direction = "right" 


class ScoreBoard(Screen):
    
    def create(self):
        game = self.manager.get_screen('solo').game
        """sortowanie wyników w zależności od gry"""
        if self.manager.get_screen('solo').eliminator == 0 or self.manager.get_screen('game').eliminator == 2:
            newDict = dict(sorted(self.manager.get_screen('game').placeList.items(), key=lambda item: int(item[1])))
        else:
            newDict = dict(sorted(self.manager.get_screen('game').placeList.items(), key=lambda item: int(item[1]),reverse=True))
        
        place = 1
        x = Label()
        x.text = 'Miejsce'
        self.scoreboardGrid.add_widget(x) 

        x = Label()
        x.text = 'Zawodnik'
        self.scoreboardGrid.add_widget(x) 

        x = Label()
        x.text = 'Punkty'
        self.scoreboardGrid.add_widget(x) 
        for key, value in newDict.items():
            x = Label()
            x.text = str(place)
            self.scoreboardGrid.add_widget(x) 

            x = Label()
            x.text = key
            self.scoreboardGrid.add_widget(x) 

            x = Label()
            x.text = value
            self.scoreboardGrid.add_widget(x) 
            place +=1

    def backFunction(self):

        self.manager.get_screen('game').navbarList = [] 
        self.manager.get_screen('game').playersNamesList = [] 
        self.manager.get_screen('game').playersPointsList = [] 
        self.manager.get_screen('game').playersPointsListTemp = []
        self.manager.get_screen('game').playersCount = 0
        self.manager.get_screen('game').currentPlayer = 0
        self.manager.get_screen('game').multiplierList = []
        self.manager.get_screen('game').placeList = {} 
        self.manager.get_screen('game').eliminator = 0 
        self.manager.get_screen('game').game = 0 
        self.manager.get_screen('game').roundsCount = 0
        self.manager.get_screen('game').round = 1 
        self.manager.get_screen('game').finish = 0 
        self.manager.get_screen('game').left = 3

        self.manager.get_screen('chooseplayers').chooseGrid.clear_widgets()
        self.manager.get_screen('chooseplayers').cb180.active = True
        self.manager.get_screen('chooseplayers').playerGrid.clear_widgets()
        self.manager.get_screen('game').usersGrid.clear_widgets()

        self.scoreboardGrid.clear_widgets()

        App.get_running_app().root.current = "main"
        App.get_running_app().root.transition.direction = "left" 


class SoloScoreBoard(Screen):
    def create(self):
        if self.manager.get_screen('solo').game >= 0 and self.manager.get_screen('solo').game <=3:
            for i,j in self.manager.get_screen('solo180701').scores.items():
                x = Label()
                y = Label()
                x.text = str(i)
                y.text = str(j)
                self.soloscoreboardGrid.add_widget(x)
                self.soloscoreboardGrid.add_widget(y)
        elif self.manager.get_screen('solo').game >= 4 and self.manager.get_screen('solo').game <=5:
            for i,j in self.manager.get_screen('minmaxwindow').scores.items():
                x = Label()
                y = Label()
                x.text = str(i)
                y.text = str(j)
                self.soloscoreboardGrid.add_widget(x)
                self.soloscoreboardGrid.add_widget(y)

    def backFunction(self):
        if self.manager.get_screen('solo').game >= 0 and self.manager.get_screen('solo').game <=3:
            self.manager.get_screen('solo180701').multiplierList = []
            self.manager.get_screen('solo180701').navbarList = []
            self.manager.get_screen('solo180701').playerPoints = 0
            self.manager.get_screen('solo180701').throwCount = 0
            self.manager.get_screen('solo180701').throwSum = 0
            self.manager.get_screen('solo180701').sixties = 0
            self.manager.get_screen('solo180701').fiftysevens = 0
            self.manager.get_screen('solo180701').scores = {}
            self.manager.get_screen('solo180701').avg = 0
            self.manager.get_screen('solo180701').game = ''
            self.manager.get_screen('solo180701').countLabel.text = '0'
            self.manager.get_screen('solo180701').avgLabel.text = '0'
            
        elif self.manager.get_screen('solo').game >= 4 and self.manager.get_screen('solo').game <=5:
            self.manager.get_screen('minmaxwindow').multiplierList = []
            self.manager.get_screen('minmaxwindow').navbarList = [] #0-leftLabel, 1-avgLabel, 2-sumLabel
            self.manager.get_screen('minmaxwindow').throwSum = 0
            self.manager.get_screen('minmaxwindow').left = rounds = 20
            self.manager.get_screen('minmaxwindow').throwCount = 0
            self.manager.get_screen('minmaxwindow').ones = 0
            self.manager.get_screen('minmaxwindow').twenties = 0
            self.manager.get_screen('minmaxwindow').avg = 0
            self.manager.get_screen('minmaxwindow').scores = {}
            self.manager.get_screen('minmaxwindow').leftLabel.text = '20'
            self.manager.get_screen('minmaxwindow').avgLabel.text = '0'
            self.manager.get_screen('minmaxwindow').sumLabel.text = '0'
            self.manager.get_screen('minmaxwindow').thrownGrid.clear_widgets()
            
        self.soloscoreboardGrid.clear_widgets()
        App.get_running_app().root.current = "main"
        App.get_running_app().root.transition.direction = "left" 

    def saveFunction(self):
        data = datetime.now()
        connection = sqlite3.connect('dart.db')
        cursor = connection.cursor()
        if self.manager.get_screen('solo').game >= 0 and self.manager.get_screen('solo').game <=3:
            
            result = self.manager.get_screen('solo180701').scores
            game = result['Gra']
            throws = result['Liczba rzutów']
            avg = result['Średnia rzutów']
            sixties = result['Liczba 60']
            fiftysevens = result['Liczba 57']
            
                
            cursor.execute(""" CREATE TABLE IF NOT EXISTS solo180701 (
            id INTEGER PRIMARY KEY,
            date TEXT,
            user TEXT,
            game TEXT,
            throws INTEGER,
            avg REAL,
            sixties INTEGER,
            fiftysevens INTEGER
        ) """)
            cursor.execute("INSERT INTO solo180701 (date,user,game,throws,avg,sixties,fiftysevens) VALUES (?,?,?,?,?,?,?)", (data,'Ziemo',game,throws,avg,sixties,fiftysevens))
        
        if self.manager.get_screen('solo').game >= 4 and self.manager.get_screen('solo').game <=5:
            result = self.manager.get_screen('minmaxwindow').scores
            game = result['Gra']
            throws = result['Liczba rzutów']
            avg = result['Średnia rzutów']
            suma = result['Suma']
            ones = result['Liczba 1']
            twenties = result['Liczba 20']
                 
            cursor.execute(""" CREATE TABLE IF NOT EXISTS minmax (
            id INTEGER PRIMARY KEY,
            date TEXT,
            user TEXT,
            game TEXT,
            throws INTEGER,
            avg REAL,
            ones INTEGER,
            twenties INTEGER
        ) """)
            cursor.execute("INSERT INTO minmax (date,user,game,throws,avg,ones,twenties) VALUES (?,?,?,?,?,?,?)", (data,'Ziemo',game,throws,avg,ones,twenties))

        connection.commit()
        connection.close()
        self.backFunction() # na zakoczenie funkcji


class Buttons(Widget):
    Builder.load_file("buttons.kv")


class Navbar(Widget):
    roundLabel = ObjectProperty(None)
    Builder.load_file("navbar.kv")


def show_popup():
    popupInput = ObjectProperty(None)
    cancel = ObjectProperty(None)
    show = P()
    popupWindow = Popup(title =  'Wpisz liczbe graczy', content = show,  size_hint= (0.6,0.3),)
    show.ids.cancel.on_release = popupWindow.dismiss
    popupWindow.open()

    def checkempty():
        print(show.cancel)


class P(FloatLayout):
    pass


class GroupWindow(Screen):
    popupInput = ObjectProperty(None)

    def add_widgetz(self):
        x = 0
        for i in range (1,3):
            x+=1
            self.grid.add_widget(Label(text=str(i)))
    
    
# class LoginWindow(Screen):
#     errorLabel = ObjectProperty(None)
#     passwordLabel = ObjectProperty(None)
#     passwordInput = ObjectProperty(None)
#     usernameInput = ObjectProperty(None)
    
#     def badUsernameMessage(self):
#         self.errorLabel.text = 'Zła nazwa użytkownika'
    
#     def badPasswordMessage(self):
#         self.errorLabel.text = "Złe hasło"

class MainWindow(Screen):
    def btn(self):
        show_popup()


class WindowManager(ScreenManager):
    pass  


kv = Builder.load_file("kivy.kv")


class DartApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    DartApp().run()
