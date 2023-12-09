import time
from imessage import iMessage
import re
import os
from dotenv import load_dotenv
from multiprocessing import Process
load_dotenv()

imessage = iMessage(os.getenv("MAC_USER"), os.getenv("PHONE_NUMBER"))

class iMessageBot:
    def __init__(self, name, commands, schedule, contacts, chat) -> None:
        self.name = name
        self.commands = commands
        self.schedule = schedule
        self.contacts = contacts
        self.chat = chat
        self.imessage = imessage
        #TODO: Move to database
        self.processed_chats = []

    def start(self):
        while True:
            time.sleep(0.5)
            messages = self.get_messages(1)
            if not messages:
                continue
            latest_message = messages[0]
            print(latest_message)
            text = latest_message['body']

            # Not a command or already processed
            if not text.startswith("!") or latest_message['rowid'] in self.processed_chats:
                continue

            cmd_str = text.split()[0]
            print(cmd_str)
            try:
                cmd = self.commands[cmd_str]
            except:
                continue

            try:
                args = text.split()[1:]
            except:
                args = []

            command_process = Process(target=cmd, args=(self, args))
            command_process.start()
            self.processed_chats.append(latest_message['rowid'])

    def get_messages(self, n):
        messages = imessage.read_messages(n=n, human_readable_date=True)
        messages = list(filter(
            lambda message: 
            re.search('[a-zA-Z0-9]', message['body']) 
            and message['group_chat_name'] == self.chat
            or (message['phone_number'] == self.chat
                and not message["group_chat_name"]),
            messages))
        return messages

    def stop(self):
        pass



#recap()

#imessage.send_message("TEST: Skickat va BOT som kör på Alex MAC", chat, True)