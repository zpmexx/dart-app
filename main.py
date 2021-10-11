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
    eliminator = 0 #czy gra to eliminator, 1 to eliminator, 2 to min-max
    round = 1
    left = 3
    def bindButton(self,j):
        multiplier = 1 
        if self.multiplierList[1].active:
            multiplier = 2
        if self.multiplierList[2].active:
            multiplier = 3
        self.left -= 1
        
        if self.eliminator == 0: #gra klasyczna
            if self.left == 2:
                self.navbarList[0].text = '0'
                self.navbarList[0].color = (1, 1, 1, 1)
                self.playersNamesList[self.currentPlayer].color = (1,0,0,1)
            if self.left != 0:
                    self.navbarList[2].text = str(self.left)
                    if int(self.playersPointsList[self.currentPlayer].text) - int(j)*multiplier > 0: #czy rzut nie przekracza 0
                        self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                        self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
                    elif int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier) == 0: #konczymy gre po koncu rundy
                        pass#koniec gry
                    else: #przekroczylo 0
                        self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                        self.left = 0

            if self.left == 0:
                self.left = 3
                if self.currentPlayer >= self.playersCount-1:
                    self.round += 1
                self.navbarList[0].text = str(int(self.navbarList[0].text)+(int(j)*multiplier))
                
                if int(self.playersPointsList[self.currentPlayer].text) - int(j)*multiplier > 0:
                    self.playersPointsList[self.currentPlayer].text = str(int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier))
                elif int(self.playersPointsList[self.currentPlayer].text) - (int(j)*multiplier) == 0:
                    pass#koniec gry
                else:
                    self.playersPointsList[self.currentPlayer].text = str(self.playersPointsListTemp[self.currentPlayer])
                
                self.playersPointsListTemp[self.currentPlayer] = int(self.playersPointsList[self.currentPlayer].text)
                
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

            
            
                
    def sayHi(self):
        print('hi')
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
        game = 0 #ktora gra
        if self.manager.get_screen('chooseplayers').cb180.active:
            game = 180
        elif self.manager.get_screen('chooseplayers').cb301.active:
            game = 301
        elif self.manager.get_screen('chooseplayers').cb501.active:
            game = 501
        elif self.manager.get_screen('chooseplayers').cb180e.active:
            game = 180
            self.eliminator = 1
        elif self.manager.get_screen('chooseplayers').cb301e.active:
            game = 301
            self.eliminator = 1
        elif self.manager.get_screen('chooseplayers').cb501e.active:
            game = 501
            self.eliminator = 1    
        elif self.manager.get_screen('chooseplayers').cbmax.active:
            game = 0
            self.eliminator = 2 
        elif self.manager.get_screen('chooseplayers').cbmin.active:
            game = 0
            self.eliminator = 2      
        
        for i in range (count-1,0,-2):
            #print(self.manager.get_screen('chooseplayers').gamesGrid.children)
            # for i in self.manager.get_screen('chooseplayers').gamesGrid.children:
            #     if (hasattr(i, '301')):
            #         print('witam')
            x = Label()
            x.text = self.manager.get_screen('chooseplayers').playerGrid.children[i-1].text
            self.usersGrid.add_widget(x)
            x.id = i
            self.playersNamesList.append(x)
            x = Label()
            if self.eliminator == 0:
                x.text = str(game)
            else:
                x.text = '0'
            self.usersGrid.add_widget(x)
            x.id = i+1
            self.playersPointsList.append(x)
            if self.eliminator == 0:
                self.playersPointsListTemp.append(game)
            else:
                self.playersPointsListTemp.append(0)
        self.playersCount = len(self.playersNamesList)
        # self.children[2].roundLabel.text = '10' #tutaj dobieramy sie do konretniej wartosci
        for i in self.children:
            if (hasattr(i, 'buttonsGrid')):
                # i.button1.bind(on_release = lambda x: self.bindButton(10))
                temp = []
                for j in range (0,21):
                    temp.append(getattr(i, 'button'+str(j))) 
                    temp[j].bind(on_release = lambda x: self.bindButton(x.text))
        self.playersNamesList[0].color = (1,0,0,1)
                # i.button0.text = 'WITAM W '
                # i.button0.bind(on_release = lambda x: self.sayHi())
                # print(i)
                # print(i.button0.text)
                # self.buttonList.append(i.button0)
                # self.buttonList[0].text = 'Strzala'
                # print(self.buttonList[0].name)
                
                

            
    # testlab = ObjectProperty(None)
    # def __init__(self, **kwargs):
    #     super(GameWindow, self).__init__(**kwargs)
    #     self.lbl = self.ids['testlab']
    # def getplayers(self):
    #     print(self.manager.get_screen('chooseplayers').playerGrid.children)
    #     for i in range (0,len(self.manager.get_screen('chooseplayers').playerGrid.children),2):
    #         print (self.manager.get_screen('chooseplayers').playerGrid.children[i].text)
    #     print(f'dlugosc to: ',len(self.manager.get_screen('chooseplayers').playerGrid.children) )
    #     self.manager.get_screen('chooseplayers').playerGrid.clear_widgets()
    #     self.manager.get_screen('chooseplayers').playersInput.text = ''
    #     self.manager.get_screen('chooseplayers').playersButton.disabled = False
    #     # self.testlab.clear_screen()
    #     # self.ids.testlab.text = 'Elo'
    #     x =( Label(
    #     name = 'testlab',
    #     size_hint = (0.2, 0.2),
    #     pos_hint ={'x':0.4 , 'y':0.8 }))
    #     self.add_widget(x)
    #     x.id = 'testlab'

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
    
    def create(self):
        self.chooseGrid.clear_widgets()
        for i in range(2,9):
            x = Button()
            x.text = str(i)
            x.id = i
            self.chooseGrid.add_widget(x)
            x.bind(on_release = lambda x :(self.buttonclicked(x.id)))
        

    # def clear(self):
    #     self.playerGrid.clear_widgets()
    #     self.playersInput.text = ''
    #     self.playersButton.disabled = False


        


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
