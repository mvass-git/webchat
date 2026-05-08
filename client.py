from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.lang import Builder
from kivy.clock import Clock

from kivy.graphics import Color, Rectangle

import socket
import threading
import json
import traceback

class Connector:
    HOST, PORT = "127.0.0.1", 8005
    def __init__(self, fun_handler):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.respond_handler = fun_handler
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
                print(f'[RECEIVED] {msg}')
                self.respond_handler(json.loads(msg))
                print(msg)
            except Exception as e:
                print(f"[ERROR] {traceback.format_exc()}")
                break
    
    def send_msg(self, msg:dict):
        self.sock.sendall(json.dumps(msg).encode())



Builder.load_file("ui.kv")

class ChatScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.conn = App.get_running_app().conn
    
    def send_chat_msg(self):
        t = self.ids.text_field.text
        self.ids.text_field.text = ""

        msg = {
            "type":"send_chat_msg",
            "msg":t
        }
        self.conn.send_msg(msg)

        self.show_msg(t)
    
    def show_msg(self, text):
        self.ids.box_messages.add_widget(
            Label(text=text, color=(1,1,1,1),size_hint_y=None, height=40)
        )
        for ch in self.ids.box_messages.children:
            print(ch.pos)

class ChatApp(App):

    def __init__(self):
        super().__init__()
        self.conn = Connector(self.msg_handler)

    def build(self):
        sm = ScreenManager()

        self.chat = ChatScreen(name="chat")
        sm.add_widget(self.chat)
        return sm
    
    def msg_handler(self, msg):
        if msg.get("type") == "chat_msg":
            if msg.get("msg"):
                t = msg.get("msg")
                Clock.schedule_once( lambda dt: self.chat.show_msg(t))

ChatApp().run()

        