import time
from imessage import iMessage
from datetime import datetime, timedelta
import re
import os
from openai import OpenAI
from dotenv import load_dotenv
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

    def start(self):
        while True:
            messages = self.get_messages(1)
            print(messages)
            if not messages:
                continue
            latest_message = messages[0]
            text = latest_message['body']

            # Not a command
            if not text.startswith("!"):
                continue

            for command in self.commands:
                print(text.split())
                if not text.split()[0] == command:
                    continue
                try:
                    args = text.split()[1:]
                except:
                    args = []
                # TODO: Spawn new process to run command
                # TODO: Support for arguments
                self.commands[command](self, args)
            time.sleep(1)

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