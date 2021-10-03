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

class SoloWindow(Screen):
    pass

class GameWindow(Screen):
    def sayHi(self):
        print('hi')
    def create(self):
        self.usersGrid.clear_widgets()
        count = len(self.manager.get_screen('chooseplayers').playerGrid.children)
        for i in range (count-1,0,-2):
            x = Label()
            x.text = self.manager.get_screen('chooseplayers').playerGrid.children[i-1].text
            self.usersGrid.add_widget(x)
            x.id = i
            x = Label()
            x.text = str(501)
            self.usersGrid.add_widget(x)
            x.id = i+1
        # self.children[2].roundLabel.text = '10' #tutaj dobieramy sie do konretniej wartosci
        for i in self.children:
            if (hasattr(i, 'roundLabel')):
                i.roundLabel.text = '69'
            if (hasattr(i, 'buttonsGrid')):
                i.button0.text = 'WITAM W '
                i.button0.bind(on_release = lambda x: self.sayHi())
        
                

            
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
    #     self.testlab.text = 'witam'

    # def testm(self):
    #     self.testlab.text = 'chuj'
    
class ChoosePlayers(Screen):
    def buttonclicked(self,i):
        self.playerGrid.clear_widgets()
        for i in range (0,i):
            self.playerGrid.add_widget(Label(text='Gracz '+str(i+1)))
            self.playerGrid.add_widget(TextInput(multiline = False,name = str(i+1)))
    
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
