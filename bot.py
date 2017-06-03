from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultPhoto
import ConfigParser
import logging

CONFIG_FILE_RELATIVE_PATH = "irouva.cfg"
CONFIG_TELEGRAM_SECTION = "TELEGRAM"
CONFIG_IMAGES_SECTION = "IMAGES"
CONFIG_TELEGRAM_TOKEN_API_KEY = "token_api"

config_parser = ConfigParser.ConfigParser()
config_parser.readfp(open(CONFIG_FILE_RELATIVE_PATH))

token_api = config_parser.get(CONFIG_TELEGRAM_SECTION, CONFIG_TELEGRAM_TOKEN_API_KEY)


def irouva_handler(bot, update):

    results = list()

    photo_dict = dict(config_parser.items(CONFIG_IMAGES_SECTION))

    for key, value in photo_dict.iteritems():

        results.append(InlineQueryResultPhoto(
                        type='photo',
                        id=key,
                        photo_url=value,
                        thumb_url=value
                   ))

    update.inline_query.answer(results)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def enable_logging():
    global logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)


enable_logging()

updater = Updater(token_api)
dp = updater.dispatcher
dp.add_error_handler(error)
dp.add_handler(InlineQueryHandler(irouva_handler))

updater.start_polling()
updater.idle()
