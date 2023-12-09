

def example(bot, args):
    """
    Example command.
    Usage: !example
    """

    bot.imessage.send_message("Example command", bot.chat)

def pong(bot, args):
    """
    Ping Pong :)
    Usage: !ping
    """
    bot.imessage.send_message(f"pong!", bot.chat)

def help(bot, args):
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