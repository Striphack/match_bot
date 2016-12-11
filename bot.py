import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from actresses_list import *
from random import randint

# def start(bot, update):
#     update.message.reply_text('Hello World!')

# def hello(bot, update):
#     update.message.reply_text(
#         'Hello {}'.format(update.message.from_user.first_name))

# def hello(bot, update):
#     update.message.reply_text(bot.to_dict())
#
#     bot.sendPhoto(chat_id=update.message.chat.id, photo=open('../training-images/Olivia_Wilde/2.jpg', 'rb'))
#     # update.message.reply_photo(photo=open('../training-images/Olivia_Wilde/2.jpg', 'rb'))

class GoldenGirlsMatchBot:

    def __init__(self):
        self.updater = Updater('204027574:AAGCbWdYdGObSwuWlirH9NJq8OblIEdgXtg')
        self.actressesSuggestCounter = {}
        self.setupHandlers()

    def setupHandlers(self):

        def start(bot, update):
            self.actressesSuggestCounter[update.message.chat.id] = 0

            update.message.reply_text("Привет. Выбери девочку, похожую на актрис:")
            self.suggestSomeAction(bot, update, 'start')

        def actressResponseOk(bot, update):
            self.suggestSomeAction(bot, update, 'ok')

        def actressResponseCrap(bot, update):
            self.suggestSomeAction(bot, update, 'crap')

        def incomingMessage(bot, update):
            self.randomReply(bot, update)

        def incomingPhoto(bot, update):
            self.photoReply(bot, update)

        self.updater.dispatcher.add_handler(CommandHandler('start', start))
        # updater.dispatcher.add_handler(CommandHandler('hello', hello))
        self.updater.dispatcher.add_handler(CommandHandler('норм', actressResponseOk))
        self.updater.dispatcher.add_handler(CommandHandler('тлен', actressResponseCrap))

        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, incomingMessage))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.photo, incomingPhoto))

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def displayActressResponseKeyboard(self, bot, update, message):
        custom_keyboard = [['/норм', '/тлен']]
        reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, one_time_keyboard=True)
        bot.sendMessage(chat_id=update.message.chat.id, text=message, reply_markup=reply_markup, resize_keyboard=True)

    def suggestSomeAction(self, bot, update, action=None):
        if self.actressesSuggestCounter[update.message.chat.id] > 2:
            self.sendGirlPhoto(bot, update)
            self.finishRound(bot, update)
            self.actressesSuggestCounter[update.message.chat.id] = 0

        else:
            message = None
            if action == 'ok':
                message = "Классная, да. А эта?"
            elif action == 'crap':
                message = "Уродка. Может эта ничо?"
            elif action == 'start':
                message = "Как тебе?"

            if message != None:
                self.displayActressResponseKeyboard(bot, update, message)

            self.sendRandomActress(bot, update)

            self.actressesSuggestCounter[update.message.chat.id] += 1

    def sendRandomActress(self, bot, update):
        # bot.sendMessage(chat_id=update.message.chat.id, text=suggestActressPhotoPath())
        bot.sendPhoto(chat_id=update.message.chat.id, photo=open(self.suggestActressPhotoPath(), 'rb'))

    def suggestActress(self):
        actress = actresses_list[randint(0, len(actresses_list)-1)]
        return actress

    def suggestActressPhotoPath(self):
        actress = self.suggestActress()
        photo_id = randint(1,100)
        return '../training-images/'+actress+'/'+str(photo_id)+'.jpg'

    def sendGirlPhoto(self, bot, update):
        photo_id = randint(1, 18)
        bot.sendPhoto(chat_id=update.message.chat.id, photo=open('../golden-girls/gallery'+str(photo_id)+'.jpg', 'rb'))

    def finishRound(self, bot, update):
        update.message.reply_text(text="Эта девочка будет ждать тебя на приват "+telegram.Emoji.KISS_MARK, reply_keyboard_markup=telegram.ReplyKeyboardHide, resize_keyboard=True)


    def randomReply(self, bot, update):
        update.message.reply_text(text="Этот бот глуп и стеснителен, но фоток у меня вагон. На. "+telegram.Emoji.KISS_MARK, reply_keyboard_markup=telegram.ReplyKeyboardHide, resize_keyboard=True)
        self.sendGirlPhoto(bot, update)

    def photoReply(self, bot, update):
        update.message.reply_text(text="Я, кажется, знаю, кто тебе по вкусу!", reply_keyboard_markup=telegram.ReplyKeyboardHide, resize_keyboard=True)
        self.sendGirlPhoto(bot, update)

bot = GoldenGirlsMatchBot()
bot.start()