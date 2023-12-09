from bot import iMessageBot
from commands.command import example,pong, ScheduledCommand
from datetime import  time

example_commands = {
    "!help": help,
    "!example": example,
    "!ping": pong
}

contacts = {
    "+46123456789": "Example Name",
}

schedule = [
    ScheduledCommand(example, time(hour=0, minute=0), 60)
]

chat = "Example Chat"

example_bot = iMessageBot("Example Bot", example_commands, schedule, contacts, chat)
example_bot.start
