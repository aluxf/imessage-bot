from datetime import datetime
from collections import Counter

def stats_to_string(total_messages, total_words, top_words):
    string = f"Total messages: {total_messages}\n"
    string += f"Total words: {total_words}\n"
    string += f"Top words:\n"
    for word in top_words:
        string += f"\t {word} ({top_words[word]})\n"
    return string

def stats(bot, args):
    """
    Get the daily chat statistics for a person.
    Usage: !stats <name>
    """
    #TODO: Implement based on nicknames in db
    #TODO: Filter boring words from top words.

    try:
        name = args[0].lower()
    except:
        bot.imessage.send_message(f"Missing name argument given in !stats.", bot.chat)
        return
    
    if name not in [contact.lower() for contact in bot.contacts.values()]:
        bot.imessage.send_message(f"Name is not defined in !stats.", bot.chat)
        return

    date = datetime.now().date()

    messages = bot.get_messages(n=1000)

    total_messages = 0
    total_words = 0
    words = []

    for message in messages:
        if not message["date"].date() == date:
            break

        if bot.contacts[message['phone_number']].lower() != name:
            continue

        total_messages += 1
        total_words += len(message['body'].split())
        words += message['body'].split()

    top_words = dict(Counter(words).most_common(5))

    bot.imessage.send_message(stats_to_string(total_messages, total_words, top_words), bot.chat)