from kivy.app import App
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

class SoloWindow(Screen):
    pass

class GameWindow(Screen):
    def getplayers(self):
        print(self.manager.get_screen('chooseplayers').playerGrid.children)
        for i in range (0,len(self.manager.get_screen('chooseplayers').playerGrid.children),2):
            print (self.manager.get_screen('chooseplayers').playerGrid.children[i].text)
        self.manager.get_screen('chooseplayers').playerGrid.clear_widgets()
        self.manager.get_screen('chooseplayers').playersInput.text = ''
        self.manager.get_screen('chooseplayers').playersButton.disabled = False

class ChoosePlayers(Screen):
    global players
    playersInput = ObjectProperty(None)
    playersButton = ObjectProperty(None)
    playersLabel = ObjectProperty(None)
    def checkPlayers(self):
        # if len(self.playersInput.text)== 0 or len(self.playersInput.text) > 1:
        #     return False,'err'
        # for i in self.playersInput.text:
        #     if i.isdigit() == True:
        #         if int(i) > 1 and int(i) < 9:
        #             return True,i
        #     else:
        #         return False,i
        # return False,i
        number = self.ids.playersInput.text
        for i in range (0,int(number)):
            self.playerGrid.add_widget(Label(text='Gracz '+str(i+1)))
            self.playerGrid.add_widget(TextInput(multiline = False,name = str(i+1)))
        self.playersButton.disabled = True

    def clear(self):
        self.playerGrid.clear_widgets()
        self.playersInput.text = ''
        self.playersButton.disabled = False

    def saveNames(self):
        players = [] 
        for i in range (0,len(self.playerGrid.children),2):
            players.append(self.playerGrid.children[i].text)
            print(self.playerGrid.children[i].text)
        print(players)
        return players 
        # print(self.manager.get_screen('main').solobutton.text)

        


class Buttons(Widget):
    Builder.load_file("buttons.kv")




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
