import telebot
import requests

API_TOKEN = '6743559323:AAH6fK-MtRyzf0m-utQg988qsDN1hI6earc'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🙌Привет! Я Ера и помогу тебе найти жанры музыки.Введи команду /search и укажи жанр музыки")

@bot.message_handler(commands=['search'])
def search(message):
    args = message.text.split('/search ', 1)

    if len(args) < 2:
        bot.send_message(message.chat.id, "напиши /search и жанр твоей музыки")
        return

    genre = args[1]

    music_url = get_music_by_genre(genre)

    if music_url:
        bot.send_message(message.chat.id, f'Вот музыка по поисковому жанру {genre}: {music_url}')
    else:
        bot.send_message(message.chat.id, f'К сожаленю я не нашел подхадящий вам жанр музыки🥲')

def get_music_by_genre(genre):

    lastfm_api_key = '3ab5303475ed03ec62514d841b8343bf'
    lastfm_api_url = f'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={genre}&api_key={lastfm_api_key}&format=json'
    response = requests.get(lastfm_api_url)

    if response.status_code == 200:
        data = response.json()
        if 'tracks' in data and 'track' in data['tracks'] and data['tracks']['track']:
            track = data['tracks']['track'][0]
            return track['url']

    return None

if __name__ == '__main__':
    bot.polling(none_stop=True)