from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.lang import Builder

import socket
import threading

class Connector:
    HOST, PORT = "127.0.0.1", 8005
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.HOST, self.PORT))
            print("CONNECTED TO SERVER")
            receiver = threading.Thread(target=self.handler, daemon=True)
            receiver.start()
        except Exception as e:
            print(f'[ERROR] {e}')
        
    def handler(self):
        while True:
            try:
                package = self.sock.recv(1024)

                if not package:
                    break

                msg = package.decode()
                print(msg)
            except Exception as e:
                print(f"[ERROR] {e}")
                break




Builder.load_file("ui.kv")

class ChatScreen(Screen):
    pass

class ChatApp(App):

    def __init__(self):
        super().__init__()
        self.conn = Connector()

    def build(self):
        sm = ScreenManager()

        chat = ChatScreen(name="chat")
        sm.add_widget(chat)
        return sm

ChatApp().run()

        