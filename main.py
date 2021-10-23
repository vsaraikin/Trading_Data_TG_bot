import telebot
from telebot import types
from config import token
import data_getter

bot = telebot.TeleBot(token)

user_dict = {}

class User:
    def __init__(self, ticker):
        self.ticker = ticker
        self.timeframe = None
        self.exchange = None

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, open('stickers/1.webp', 'rb'))
    msg = bot.send_message(message.chat.id, """\
        Hi there! Enter the ticker:
        """)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        ticker = message.text
        user = User(ticker)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Enter the timeframe: \n'
                                    'Now the following timeframes avaliable: \n'
                                    ' -1m \n'
                                    ' -15m\n'
                                    ' -1h \n'
                                    ' -1d \n')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        timeframe = message.text
        user = user_dict[chat_id]
        user.timeframe = timeframe
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('CME_MINI', 'BINANCE', 'NASDAQ') # You can add thatever exchange you want that has been on tradingview
        msg = bot.reply_to(message, 'What is your exchange', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        exchange = message.text
        user = user_dict[chat_id]
        if (exchange == u'CME_MINI') or (exchange == u'BINANCE') or (exchange == u'NASDAQ'):
            user.exchange = exchange
        else:
            raise Exception("Unknown exchange")
    
        bot.send_message(chat_id, 'Ticker:' + user.ticker + '\nTimeframe:' + str(user.timeframe) + '\nExchange:' + user.exchange)

        if user.timeframe == '1m':
            data_getter.plot_data_1_minute(user.ticker, user.exchange)
        elif user.timeframe == '15m':
            data_getter.plot_data_15_minute(user.ticker, user.exchange)
        elif user.timeframe == '1h':
            data_getter.plot_data_1_hour(user.ticker, user.exchange)
        elif user.timeframe == '1d':
            data_getter.plot_data_1_day(user.ticker, user.exchange)
        else:
            bot.send_message(message.chat.id, 'Invalid value :(')

        bot.send_photo(message.chat.id, open('proxy_image.png', 'rb'))
        bot.send_message(message.chat.id,
                        f'Price: {data_getter.last_price(user.ticker, user.exchange)[1]}\n'
                        f'Time: {data_getter.last_price(user.ticker, user.exchange)[0]}'
                        ) 
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()