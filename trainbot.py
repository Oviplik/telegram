import telebot
import requests
import sqlite3

bot = telebot.TeleBot('')

conn = sqlite3.connect('fitness/db.sqlite3', check_same_thread=False)
cursor = conn.cursor()
name_client = ''
time_client = ''
type_trains = ''
treners = ''
phone_client = ''

def db_table_val(user_id_telegram: int, username_telegram: str, user_name_telegram: str, user_name_client: str, user_time_client: str, status: bool, user_phone_client: str, type_train: str, trener: str):
	cursor.execute('INSERT INTO web_telebot (user_id_telegram, username_telegram, user_name_telegram, user_name_client, user_time_client, status, user_phone_client, type_train, trener) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id_telegram, username_telegram, user_name_telegram, user_name_client, user_time_client, status, user_phone_client, type_train, trener))
	conn.commit()

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Добро пожаловать. Я помогу Вам записаться на тренировку в фитнес-клуб «Богатырь»')
	bot.send_message(message.chat.id, 'Скажите мне Вашу фамилию и имя для записи на тренировку')
	bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name_client
    name_client = message.text
    bot.send_message(message.from_user.id, 'Ваш номер телефона для связи')
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
	global phone_client
	phone_client = message.text
	keyword = telebot.types.InlineKeyboardMarkup(row_width=2)
	key_pers = telebot.types.InlineKeyboardButton(
		text='Персональная', callback_data='pers')
	key_group = telebot.types.InlineKeyboardButton(
		text='Групповая', callback_data='group')
	keyword.add(key_pers, key_group)
	question = f'На какую тренировку вы хотите записаться?'
	bot.send_message(message.chat.id, text=question, reply_markup=keyword)


@bot.callback_query_handler(func=lambda call: call.data == "pers")
def train_pers(call):
	global type_trains
	type_trains = 'Персональная'
	keyword = telebot.types.InlineKeyboardMarkup(row_width=1)
	key_murom = telebot.types.InlineKeyboardButton(
		text='Илья Муромец', callback_data='Ilya_Muromec')
	key_dobr = telebot.types.InlineKeyboardButton(
		text='Добрыня Никитич', callback_data='Dobrynya_Nikitich')
	key_pop = telebot.types.InlineKeyboardButton(
		text='Алёша Попович', callback_data='Alesha_Popovich')
	keyword.add(key_murom, key_dobr, key_pop)
	question = f'К какому тренеру вы хотите записаться на тренировку?'
	bot.send_message(call.message.chat.id, text=question, reply_markup=keyword)

@bot.callback_query_handler(func=lambda call: call.data == "group")
def train_group(call):
	global treners
	global type_trains
	treners = 'Василиса Прекрасная'
	type_trains = 'Групповая'
	keyword = telebot.types.InlineKeyboardMarkup(row_width=3)
	key_pn = telebot.types.InlineKeyboardButton(
		text='Пн 19:00', callback_data='Pn_19_00')
	key_sr = telebot.types.InlineKeyboardButton(
		text='Ср 20:00', callback_data='Sr_20_00')
	key_sb = telebot.types.InlineKeyboardButton(
		text='Сб 15:00', callback_data='Sb_15_00')
	keyword.add(key_pn, key_sr, key_sb)
	question = f'Групповые тренировки ведет Василиса Прекрасная. На какое время вы хотите записаться?'
	bot.send_message(call.message.chat.id, text=question, reply_markup=keyword)

@bot.callback_query_handler(func=lambda call: call.data == "Ilya_Muromec")
def get_trener_Ilya_Muromec(call):
	global treners
	treners = 'Ильмя Муромец'
	bot.send_message(call.message.chat.id, 'В какой день и на какое время вы хотите записаться (например, 11.11 в 15:30)')
	get_answer_time(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "Dobrynya_Nikitich")
def get_trener_Dobrynya_Nikitich(call):
	global treners
	treners = 'Добрыня Никитич'
	bot.send_message(call.message.chat.id, 'В какой день и на какое время вы хотите записаться (например, 11.11 в 15:30)')
	get_answer_time(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "Alesha_Popovich")
def get_trener_Alesha_Popovich(call):
	global treners
	treners = 'Алёша Попович'
	bot.send_message(call.message.chat.id, 'В какой день и на какое время вы хотите записаться (например, 11.11 в 15:30)')
	get_answer_time(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "Pn_19_00")
def get_Pn_19_00(call):
	global time_client
	time_client = 'Пн 19:00'
	keyword = telebot.types.InlineKeyboardMarkup(row_width=2)
	key_yes = telebot.types.InlineKeyboardButton(
		text='Да', callback_data='yes')
	key_no = telebot.types.InlineKeyboardButton(
		text='Нет', callback_data='no')
	keyword.add(key_yes, key_no)
	question = f'{name_client}, {type_trains} тренировка с {treners}. Дата и время: {time_client}. Номер для связи {phone_client}. Верно?'
	bot.send_message(call.message.chat.id, text=question, reply_markup=keyword)


@bot.callback_query_handler(func=lambda call: call.data == "Sr_20_00")
def get_Sr_20_00(call):
	global time_client
	time_client = 'Ср 20:00'
	keyword = telebot.types.InlineKeyboardMarkup(row_width=2)
	key_yes = telebot.types.InlineKeyboardButton(
		text='Да', callback_data='yes')
	key_no = telebot.types.InlineKeyboardButton(
		text='Нет', callback_data='no')
	keyword.add(key_yes, key_no)
	question = f'{name_client}, {type_trains} тренировка с {treners}. Дата и время: {time_client}. Номер для связи {phone_client}. Верно?'
	bot.send_message(call.message.chat.id, text=question, reply_markup=keyword)


@bot.callback_query_handler(func=lambda call: call.data == "Sb_15_00")
def get_Sb_15_00(call):
	global time_client
	time_client = 'Сб 15:00'
	keyword = telebot.types.InlineKeyboardMarkup(row_width=2)
	key_yes = telebot.types.InlineKeyboardButton(
		text='Да', callback_data='yes')
	key_no = telebot.types.InlineKeyboardButton(
		text='Нет', callback_data='no')
	keyword.add(key_yes, key_no)
	question = f'{name_client}, {type_trains} тренировка с {treners}. Дата и время: {time_client}. Номер для связи {phone_client}. Верно?'
	bot.send_message(call.message.chat.id, text=question, reply_markup=keyword)


@bot.message_handler(content_types = ["text"])
def get_answer_time(message):
    bot.register_next_step_handler(message, get_time)

def get_time(message):
	global time_client
	time_client = message.text
	keyword = telebot.types.InlineKeyboardMarkup(row_width=2)
	key_yes = telebot.types.InlineKeyboardButton(
		text='Да', callback_data='yes')
	key_no = telebot.types.InlineKeyboardButton(
		text='Нет', callback_data='no')
	keyword.add(key_yes, key_no)
	question = f'{name_client}, {type_trains} тренировка с {treners}. Дата и время: {time_client}. Номер для связи {phone_client}. Верно?'
	bot.send_message(message.chat.id, text=question, reply_markup=keyword)

@bot.callback_query_handler(func=lambda call: call.data == "yes")
def get_sign_up_yes(call):
	bot.send_message(call.message.chat.id, 'Ваша заявка успешно отправлена менеджеру! Ожидайте ответа')
	user_id_telegram = call.from_user.id
	username_telegram = call.from_user.username
	user_name_telegram = call.from_user.first_name
	user_name_client = name_client
	user_time_client = time_client
	user_phone_client = phone_client
	type_train = type_trains
	trener = treners


	db_table_val(user_id_telegram=user_id_telegram, username_telegram=username_telegram, user_name_telegram=user_name_telegram, user_name_client=name_client, user_time_client=time_client,
				 status=False, user_phone_client=phone_client, type_train=type_train, trener=trener)

@bot.callback_query_handler(func=lambda call: call.data == "no")
def get_sign_up_no(call):
	bot.send_message(call.message.chat.id, 'Предлагаю начать с начала /start')

bot.polling(none_stop=True,interval=0)
