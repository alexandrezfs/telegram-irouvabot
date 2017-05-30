from telegram.ext import Updater, CommandHandler
import ConfigParser
import logging

CONFIG_FILE_RELATIVE_PATH = "irouva.cfg"
CONFIG_TELEGRAM_SECTION = "TELEGRAM"
CONFIG_IMAGES_SECTION = "IMAGES"
CONFIG_TELEGRAM_TOKEN_API_KEY = "token_api"

MAIN_COMMAND_NAME = "irouva"

config_parser = ConfigParser.ConfigParser()
config_parser.readfp(open(CONFIG_FILE_RELATIVE_PATH))

token_api = config_parser.get(CONFIG_TELEGRAM_SECTION, CONFIG_TELEGRAM_TOKEN_API_KEY)


def irouva_handler(bot, update):
    user = update.message.from_user

    logger.info("Message sent from %s: %s" % (user.first_name, update.message.text))

    photo_dict = dict(config_parser.items(CONFIG_IMAGES_SECTION))
    photo_url = None

    for key, value in photo_dict.iteritems():

        if update.message.text.endswith(" " + key):
            photo_url = value
            break

    if photo_url is None:

        if update.message.text == "/" + MAIN_COMMAND_NAME:
            help_message = get_help_message(photo_dict)
            update.message.reply_text(help_message)
        else:
            update.message.reply_text(
                "Sorry {}, I don't have this irouva pic... yet :)".format(user.first_name))
    else:
        bot.sendPhoto(
            chat_id=update.message.chat_id,
            photo=photo_url
        )


def get_help_message(photo_dict):
    all_emots_codes = get_all_emots_codes(photo_dict)
    help_message = "Usage: /" + MAIN_COMMAND_NAME + "<emot-code> \nEmots available: " + all_emots_codes
    return help_message


def get_all_emots_codes(photo_dict):
    all_emots = "";
    for key in photo_dict.keys():
        all_emots += "{" + key + "}"

    return all_emots


def enable_logging():
    global logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)


enable_logging()

updater = Updater(token_api)
updater.dispatcher.add_handler(CommandHandler(MAIN_COMMAND_NAME, irouva_handler))

updater.start_polling()
updater.idle()
