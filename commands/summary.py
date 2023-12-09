from datetime import datetime, timedelta
from openai import OpenAI
import re
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_KEY"),
)

def gpt_summarize(conversation_history, date):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f""" 
                You are a chat summarizer that summarizes the Tour De Stud chat for a given date.
                
                - Summarize the most important and funniest parts of the conversation.
                - It should be a flowing text.
                - It should be exciting to read.
                - Make it as funny as possible but still realistic.
                - Reference the people in the chat by their name.
                - After the summary name out the following titles based on the conversation:
                    - The wisest person in the chat
                    - The funniest person in the chat
                    - The most annoying person in the chat
                    - The most helpful person in the chat
                    - The most active person in the chat
                """
            },
            {
                "role": "user",
                "content": f"""
                date: {date}

                CONVERSATION HISTORY: 
                {conversation_history}
                """,
            }
        ],
        model="gpt-4-1106-preview",
    )

    choice = chat_completion.choices[0]
    return choice.message.content

def summary(bot, args, evoker):
    """
    Get summary for a given date.
    Usage: !summary <yyyy-mm-dd>
    """
    n = None
    if not args:
        n = 1000
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(args[0], "%Y-%m-%d").date()
        except:
            bot.imessage.send_message("Invalid date argument in !summary.", bot.chat)
            return


    messages = bot.get_messages(n=n)
    conversation_history = ""
    
    found_date = False
    for message in messages:

        if not message["date"].date() == date:
            if found_date:
                break
            continue
        found_date = True

        identifier = message['phone_number']
        try:
            identifier = bot.contacts[identifier]
        except:
            pass
        
        conversation_history = f"{identifier}: {message['body']}" + "\n" + conversation_history

    summary = gpt_summarize(conversation_history, date)
    bot.imessage.send_message(summary, bot.chat)