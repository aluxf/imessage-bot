#import models from database.py
from database import ChatRoom, ChatUser, db
from peewee import DoesNotExist

def example(bot, _):
    """
    Example command.
    Usage: !example
    """

    bot.imessage.send_message("Example command", bot.chat)

def pong(bot, _):
    """
    Ping Pong :)
    Usage: !ping
    """
    bot.imessage.send_message(f"pong!", bot.chat)

def help(bot, _):
    """
    Get list of commands.
    Usage: !help
    """
    string = "List of commands:\n\n"
    for command in bot.commands:
        string += f"{command}"
        doc = bot.commands[command].__doc__
        if not doc:
            doc = "No description."
        string += f"\t {doc}\n"
    bot.imessage.send_message(string, bot.chat)

def nick(bot, data):
    """
    Get and change your nickname.
    Usage: !nick <name> (optional)
    """
    args = data["args"]
    evoker = data["evoker"]
    
    db.connect()

    arg_len = len(args)
    chatroom = ChatRoom.get(ChatRoom.name == bot.chat)
    if arg_len > 1:
        bot.imessage.send_message("Too many arguments in !nick.", bot.chat)
        return
    
    try:
        user = ChatUser.get(ChatUser.phone_number == evoker and ChatUser.chatroom == chatroom)
    except DoesNotExist:
        user = None

    if arg_len == 0:
        if user:
            bot.imessage.send_message(f"Your current nickname is {user.name}.", bot.chat)
        else:
            bot.imessage.send_message("You don't have a nickname yet. Try !nick <name>.", bot.chat)
        return

    nickname = args[0]

    if not user:
        ChatUser.create(phone_number=evoker, name=nickname, chatroom=bot.chat)
        bot.imessage.send_message(f"Your nickname has been set to {nickname}.", bot.chat)
        return
    
    user.name = nickname
    user.save()
    bot.imessage.send_message(f"Your nickname has been changed to {nickname}.", bot.chat)
    db.close()
    return



