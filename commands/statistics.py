from datetime import datetime
from collections import Counter
from nltk.corpus import stopwords
from nltk import download

# Download the stopwords package if it's not already downloaded
download('stopwords')

# TODO: When packaging the bot, the path to the data packages needs to be set.
# nltk.data.path.append('/path/to/your/data/packages')

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
    # Get the list of Swedish stop words
    stop_words = set(stopwords.words('swedish'))

    for message in messages:
        if not message["date"].date() == date:
            break

        if bot.contacts[message['phone_number']].lower() != name:
            continue

        total_messages += 1
        words_in_message = message['body'].split()
        total_words += len(words_in_message)
        #filter words
        words += [word.lower() for word in words_in_message if word.lower() not in stop_words]

    top_words = dict(Counter(words).most_common(10))

    bot.imessage.send_message(stats_to_string(total_messages, total_words, top_words), bot.chat)