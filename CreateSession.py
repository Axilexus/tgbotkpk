from telethon import TelegramClient, events
from telethon.tl.custom import Button

#This class was created a new telegram session. Its so easy for new bots
class CreateSession:
    def __init__(self, session_name):
        api_id = 28145862
        api_hash = "995293a44cca2422773b05208246d083"
        self.client = TelegramClient(session_name, api_id, api_hash)

    def start(self):
        self.client.start()
        self.client.run_until_disconnected()

class CreateButton:
    def __init__(self):
        self.menu = []

    def add_button(self, name, data):
        self.menu.append([Button.inline(name, bytes(data, encoding='utf-8'))])

    def add_two_button_in_line(self, name1, name2, data1, data2):
        self.menu.append(
            [
                Button.inline(name1, bytes(data1, encoding='utf-8')),
                Button.inline(name2, bytes(data2, encoding='utf-8'))
            ]
        )
    def add_three_button_in_line(self, name1, name2, name3, data1, data2, data3):
        self.menu.append(
            [
                Button.inline(name1, bytes(data1, encoding='utf-8')),
                Button.inline(name2, bytes(data2, encoding='utf-8')),
                Button.inline(name3, bytes(data3, encoding='utf-8'))
            ]
        )

    def return_buttons(self):
        return self.menu