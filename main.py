import telebot
from gpt_model import generate_joke

bot = telebot.TeleBot('bot-token')

def get_joke(text):
    if text == 'Joke':
        res = (generate_joke('Joke:')[5:]).capitalize()
    else:
        res = generate_joke(text)
    return res

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Suggest <b>the beginning</b> of a joke in English, I'll try my best to finish it. Or type \"Joke\" if you want joke from scratch", parse_mode='html')
    

@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, get_joke(message.text.lower().capitalize()).capitalize(), parse_mode='html')

    
bot.polling(non_stop=True)