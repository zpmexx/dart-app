from kivy import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '300')
Config.set('graphics', 'minimum_height', '400')

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

class SoloWindow(Screen):
    pass

class GameWindow(Screen):

    navbarList = [] #0 - sumLabel, 1 - roundLabel, 2 - leftLabel
    playersNamesList = [] #lista graczy
    playersPointsList = []  #lista punktow graczy, id te same
    playersPointsListTemp = []
    multiplierList = []
    playersCount = 0
    currentPlayer = 0
    buttonList = []
    placeList = {} #lista miejsc graczy
    eliminator = 0 #czy gra to eliminator, 1 to eliminator, 2 to min-max
    game = 0 #ktora gra
    roundsCount = 0
    round = 1 
    finish = 0 #kontolna zmienna by nie powielać kroku gdy zakonczy sie runde przed trecim rzutem
    left = 3
    def bindButton(self,j):
        
        self.finish = 0
        multiplier = 1 
        if self.multiplierList[1].active:
            multiplier = 2
        if self.multiplierList[2].active:
            multiplier = 3
        self.left -= 1

        if int(j) == 25 or int(j) == 50:
            multiplier = 1
        
        if self.eliminator == 0: #gra klasyczna
            print(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
            if self.left == 2:
                self.navbarList[0].text = '0'
                self.navbarList[0].color = (1, 1, 1, 1)
                self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
            if self.left != 0:
                    self.navbarList[2].text = str(self.left)
                    if int(self.playersPointsList[self.currentPlayer].text) - int(j)*multiplier > 0: #czy rzut nie przekracza 0
                        print("> 0")
                        self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
                    elif int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier) == 0: #konczymy gre po koncu rundy
                        print("==0")
                        self.playersPointsList[self.currentPlayer].text = '0'
                        self.placeList[self.playersNamesList[self.currentPlayer].text] = self.playersPointsList[self.currentPlayer].text
                        self.left = 0
                        self.finish = 1
                    else: #przekroczylo 0
                        print('<0')
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                        self.left = 0

            if self.left == 0:
                self.left = 3

                self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                if self.finish == 0:
                    if int(self.playersPointsList[self.currentPlayer].text) - int(j)*multiplier > 0:
                        print('>0 v2')
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
                    elif int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier) == 0:
                        print('==0 v2')
                        self.playersPointsList[self.currentPlayer].text = '0'
                        self.placeList[self.playersNamesList[self.currentPlayer].text] = self.playersPointsList[self.currentPlayer].text
                    else:
                        print('<0 v2')
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                    
                    self.playersPointsListTemp[self.currentPlayer] = int(self.playersPointsList[self.currentPlayer].text)
                    

                if self.currentPlayer >= self.playersCount-1:
                    self.round += 1
                    if self.placeList: #koniec gry
                        print('koniec gry')
                        for i in range (0,len(self.playersNamesList)):
                            if self.playersNamesList[i].text not in self.placeList:
                                self.placeList[self.playersNamesList[i].text] = self.playersPointsList[i].text
                        print(self.placeList)
                        App.get_running_app().root.transition.direction = "left"  
                        App.get_running_app().root.current = "scoreboard"

                self.navbarList[0].color = (1,0,1,1)#zmiana koloru przy następnym graczu
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
            


        elif self.eliminator == 1: #eliminator
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
        else: #min - max
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
            self.eliminator = 2 
        elif self.manager.get_screen('chooseplayers').cbmin.active:
            self.game = 0
            self.eliminator = 2      
        
        for i in range (count-1,0,-2):
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
            self.roundsCount = 5
        elif self.playersCount >=4 and self.playersCount <=5:
            self.roundsCount = 15
        else:
            self.roundsCount = 10

        if self.eliminator == 2:
            self.navbarList[1].text = str(self.roundsCount)

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

    

class MaxLengthInput(TextInput):
    max_characters = NumericProperty(0)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)


class ChoosePlayers(Screen):
    def buttonclicked(self,i):
        self.playerGrid.clear_widgets()
        for i in range (0,i):
            self.playerGrid.add_widget(Label(text='Gracz '+str(i+1)))
            self.playerGrid.add_widget(MaxLengthInput(multiline = False,name = str(i+1),max_characters = 12)) #dlugosc nazwy gracza
        self.manager.get_screen('chooseplayers').confirmButton.disabled = False
    
    def create(self):
        self.chooseGrid.clear_widgets()
        for i in range(2,9):
            x = Button()
            x.text = str(i)
            x.id = i
            self.chooseGrid.add_widget(x)
            x.bind(on_release = lambda x :(self.buttonclicked(x.id)))

    def validatePlayers(self):
        result = 0
        nameslist = []
        for i in range (0,len(self.playerGrid.children),2):
            nameslist.append(self.playerGrid.children[i].text.lstrip())
        for i in range (0,len(self.playerGrid.children),2):
            if self.playerGrid.children[i].text.lstrip() == '':
              self.playerGrid.children[i+1].color = 1,0,0,1   
              result = 1
            else:
                self.playerGrid.children[i+1].color = 1,1,1,1  
        # for i in range (0,len(nameslist)):
        #     if nameslist.count(nameslist[i])>1:
        #         for j in range (0,len(nameslist)):
        #             if self.playerGrid.children[j].text == nameslist[i]:
        #                 self.playerGrid.children[j].color = 1,0,0,1 
        #                 result = 1
        #             else:
        #                 self.playerGrid.children[j].color = 1,1,1,1 
        if result == 1:
            pass
        else:
            App.get_running_app().root.transition.direction = "left"  
            App.get_running_app().root.current = "game"
            
            

             

    # def clear(self):
    #     self.playerGrid.clear_widgets()
    #     self.playersInput.text = ''
    #     self.playersButton.disabled = False

class ScoreBoard(Screen):
    
    def create(self):
        newDict = dict(sorted(self.manager.get_screen('game').placeList.items(), key=lambda item: int(item[1])))
        place = 1
        # for key, value in self.manager.get_screen('game').placeList.items():
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
            print(x)
            x+=1
            self.grid.add_widget(Label(text=str(i)))
    


class LoginWindow(Screen):
    errorLabel = ObjectProperty(None)
    passwordLabel = ObjectProperty(None)
    passwordInput = ObjectProperty(None)
    usernameInput = ObjectProperty(None)
    
    def badUsernameMessage(self):
        self.errorLabel.text = 'Zła nazwa użytkownika'
    
    def badPasswordMessage(self):
        self.errorLabel.text = "Złe hasło"

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
