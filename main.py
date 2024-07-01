import telebot
import random
from telebot import types
from ExchangeRateApi import *
import requests
from bs4 import BeautifulSoup
import time

bot = telebot.TeleBot('7459337661:AAGB37AI_7e4pYz943iJKC63699MBYhtGuQ')
api  = ExchangeRateApi("d10bb83f31daf59c5678869e")
global _help
global amount
new_post_url = None
_help = True

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Начать обучение🚀', callback_data='start_learning')
    btn2 = types.InlineKeyboardButton('Продолжить обучение⏳', callback_data='continue_learning')
    btn3 = types.InlineKeyboardButton('Инструменты🛠', callback_data='tools_fenance')
    btn4 = types.InlineKeyboardButton('Новости о рынке⚡️',callback_data='news')
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    hello_message =  random.choice(['Привет!\nВыбери, что тебя интересует:',
                                    "Ликуют акции!\nВыбери, что тебя интересует:",
                                    "Акции есть? А если найду?\nВыбери, что тебя интересует:",
                                    "И снова здравствуй!\nЧто тебя интересует?",
                                    f"Привет, {message.from_user.first_name}!\nЧто тебя интересует?",
                                    "Oh.. Here we go again.. \nВыбери, что тебя интересует:",
                                    f"Это ведь ты, {message.from_user.first_name}? Ну привет!\nЧто тебя интересует?",
                                    f"Здравствуй, {message.from_user.first_name}.\nЧто тебя интересует?",
                                    f"Подсчитывай прибыль, грусти по убыткам.\nЧто тебя интересует, {message.from_user.first_name}? "])
    bot.send_message(message.chat.id, hello_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global amount
    global _help
    if callback.data == 'start_learning':
        bot.send_message(callback.message.chat.id, "Отлично! Начнем наше обучение! План состоит из 7 модулей:"
                        "\n<b>1. Основы финансов</b>"
                         "\n<b>2. Финансовые рынки</b>"
                         "\n<b>3. Финансовые инструменты</b>"
                         "\n<b>4. Основы инвестирования</b>"
                         "\n<b>5. Основные финансовые показатели</b>"
                         "\n<b>6. Личные финансы</b>"
                         "\n<b>7. Экономические понятия</b>"
                        '\n\n Начнем с первого модуля "Основы финансов"', parse_mode= "HTML")
        bot.send_message(callback.message.chat.id, "Обучение будет проходить в следующем формате по частям:"
                                                   "\n<b>1 часть</b> - теоретический материал"
                                                   "\n<b>2 часть</b> - тест, на проверку усвоенного материала (тест всегда можно пропустить при желании)"
                                                   "\n\nНу чтож, начнем! (ураа напиши начнем! вухуу)", parse_mode= "HTML")
        bot.register_next_step_handler(callback.message,Lesson_1)

    if callback.data == "skip_test_1":
        markup = types.ReplyKeyboardMarkup()
        btn_con = types.KeyboardButton("Продолжить")
        markup.add(btn_con)
        bot.send_message(callback.message.chat.id, "Тогда переходим к следующему модулю!",reply_markup=markup)

        bot.register_next_step_handler(callback.message,Lesson_2)
    if callback.data == "start_test_1":
        Test_1(callback.message)

    if callback.data == "tools_fenance":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Конвертация валют", callback_data= "converter")
        btn2 = types.InlineKeyboardButton("Акции", callback_data= "stock")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(callback.message.chat.id, "Что тебе нужно?", reply_markup= markup)

    if callback.data == "converter":
        if  _help:
            bot.send_message(callback.message.chat.id, 'Как работать с инструментом "Конвертации валют"?'
                                                   '\nДля начала тебе необходимо ввести определённую сумму, которая в последующем будет конвертироваться из одной валюты в другую, например "100".\n'
                                                   '\nПосле, через слэш (это вот такой знак "/") введите буквенный код нужной валюты (RUB/EUR, RUB/USD).'
                                                    '\n\nТакже есть быстрая конвертация валют: USD/RUB и EUR/RUB.')
            _help = False
        bot.send_message(callback.message.chat.id, "Введите сумму:")
        bot.register_next_step_handler(callback.message, summa)
    if callback.data == "another":
        markup_ant = types.InlineKeyboardMarkup()
        btn_view = types.InlineKeyboardButton("Посмотреть коды валют", url="https://www.exchangerate-api.com/docs/supported-currencies")
        markup_ant.add(btn_view)
        bot.send_message(callback.message.chat.id, "Введите пару значений (коды валют) через слэш:",reply_markup=markup_ant)
        bot.register_next_step_handler(callback.message, owncurrency)

    if callback.data == 'usd/rub':
        text = api.get_pair_conversion("USD", "RUB", 1)
        values = callback.data.upper().split('/')
        num = 0
        for i in text:
            num += 1
            if i == "B":
                res = text[:num]
                break
        course = res.split("\n")
        res_text = res.split()
        revers_text = " ".join(res_text[::-1])
        num_probels = 0
        finaly_text = ""
        for i in revers_text:
            if i == " ":
                num_probels += 1
            if num_probels == 1:
                finaly_text = finaly_text + i
            if num_probels == 2:
                break
        finaly_text = finaly_text.strip()
        bot.send_message(callback.message.chat.id, f"Текущий курс {values[0]} к {values[1]}: {course[2]}"
                                                   f"\nРезультат конвертации по текущему курсу: {round(float(finaly_text), 2) * amount}")
    if callback.data == 'eur/rub':
        text = api.get_pair_conversion("EUR", "RUB", 1)
        values = callback.data.upper().split('/')
        num = 0
        for i in text:
            num += 1
            if i == "B":
                res = text[:num]
                break
        course = res.split("\n")
        res_text = res.split()
        revers_text = " ".join(res_text[::-1])
        num_probels = 0
        finaly_text = ""
        for i in revers_text:
            if i == " ":
                num_probels += 1
            if num_probels == 1:
                finaly_text = finaly_text + i
            if num_probels == 2:
                break
        finaly_text = finaly_text.strip()
        bot.send_message(callback.message.chat.id, f"Текущий курс {values[0]} к {values[1]}: {course[2]}"
                                                   f"\nРезультат конвертации по текущему курсу: {round(float(finaly_text),2)*amount}")

    if callback.data == "stock":
        bot.send_message(callback.message.chat.id, "Акции")
    if callback.data == "news":
        News(callback.message)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат.")
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup_con = types.InlineKeyboardMarkup()
        btn_USD_RUB = types.InlineKeyboardButton("USD/RUB", callback_data='usd/rub')
        btn_EUR_RUB = types.InlineKeyboardButton("EUR/RUB", callback_data='eur/rub')
        btn_another = types.InlineKeyboardButton("Другое значение", callback_data='another')
        markup_con.add(btn_USD_RUB, btn_EUR_RUB)
        markup_con.row(btn_another)
        bot.send_message(message.chat.id, "Выберите предложенные варианты", reply_markup=markup_con)

    else:
        bot.send_message(message.chat.id,"Вы ввели сумму меньше нуля")
        bot.register_next_step_handler(message, summa)

def owncurrency(message):
    try:
        values = str(message.text).upper().split('/')
        text = api.get_pair_conversion(values[0], values[1], 1)
        num = 0
        for i in text:
            num += 1
            if i == values[1][0] and text[num] == values[1][1] and text[num+1] == values[1][-1]:
                res = text[:num]
                break
        course = text.split("\n")
        res_text = res.split()
        revers_text = " ".join(res_text[::-1])
        num_probels = 0
        finaly_text = ""
        for i in revers_text:
            if i == " ":
                num_probels += 1
            if num_probels == 1:
                finaly_text = finaly_text + i
            if num_probels == 2:
                break
        finaly_text = finaly_text.strip()
        bot.send_message(message.chat.id, f"Текущий курс {values[0]} к {values[1]}: {course[2]}"
                                                   f"\nРезультат конвертации по текущему курсу: {round(float(finaly_text), 2)*amount}")

    except Exception:
        bot.send_message(message.chat.id,"Что-то не так, возможно вы ввели некорректное значение.\nВведите пару значений через слэш:")
        bot.register_next_step_handler(message, owncurrency)

def News(message):
    global new_post_url
    URL = "https://bcs-express.ru/category"
    response = requests.get(URL)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    newest_post = soup.find('div', class_='TjB6 KSLV Ncpb E6j8')

    title = soup.find('a', class_='iKzE').text.strip()
    description = soup.find('p', class_="OIgY").text.strip()
    url = soup.find('a', class_='iKzE', href=True)['href'].strip()

    if url != new_post_url:
        new_post_url = url
        bot.send_message(message.chat.id, f"❗️<b>{str(title).upper()}</b>❗️\n\n<i>{description}</i>\n\nСсылка на пост: {url}",parse_mode='HTML')
    time.sleep(60)
    News(message)
def Lesson_1(message):
    bot.send_message(message.chat.id, "Это твой первый урок! Здесь тебе дается статья и краткая вЫжимка этой статьи.\n\nТакже можешь посмотреть видеоролик на ютубе про <b>ФИНАНСОВУЮ ГРАМОТНОСТЬ!</b>",parse_mode="HTML")
    bot.send_message(message.chat.id,"https://telegra.ph/Osnovy-finansov-06-30-2")
    bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=S88HZWjuVZg")
    bot.send_message(message.chat.id,"""<b>Главное о финансах в 5 пунктах:</b>\n
1 - Финансы представляют собой все деньги, которые находятся в обращении и используются государством, бизнесом и физическими лицами для увеличения богатства и достижения финансовой стабильности.\n
2 - Существуют различные виды финансов: личные финансы, корпоративные финансы, государственные финансы, общественные финансы и международные финансы. Каждый вид финансов имеет свои особенности и характеристики.\n
3 - Функции финансов — формирование, контроль, регулирование, стабилизация, распределение и стимулирование.\n
4 - Управление финансами включает планирование, оперативное управление и контроль. Планирование позволяет определить финансовые цели и стратегии, оперативное управление обеспечивает эффективное использование ресурсов, а контроль помогает оценить результаты и корректировать действия.\n
5 - Знание основ управления финансами имеет важное значение для финансовой устойчивости, принятия обоснованных решений о распределении средств, инвестировании и достижении финансовых целей как для физических лиц, так и для бизнеса и государства."""
                     ,parse_mode="HTML")
    markup = types.InlineKeyboardMarkup()
    btn_skip = types.InlineKeyboardButton("Пропустить тест",callback_data="skip_test_1")
    btn_start = types.InlineKeyboardButton("Начать тест",callback_data="start_test_1")
    markup.add(btn_start,btn_skip)
    bot.send_message(message.chat.id,"Готов к тесту?",reply_markup=markup)

def Test_1(message):
    markup = types.ReplyKeyboardMarkup()
    a = types.KeyboardButton('a')
    b = types.KeyboardButton('b')
    c = types.KeyboardButton('c')
    coin = 0
    markup.row(a,b,c)
    bot.send_photo(message.chat.id,"https://1drv.ms/i/c/d59c6f998f225afd/IQMVAjrglX9yToDT5vvL_hnbAci3TqZ-HF57MgBreqwj7wA?width=936&height=682", caption="<b>Что такое финансы?</b>"
                                               "\n\na) Совокупность денег, активов и ресурсов, которыми располагают только физические лица. "
                                               "\n\nb) Совокупность денег, активов и ресурсов, которыми располагают государства, компании и физические лица."
                                               "\n\nc) Наличные деньги и банковские счета.", parse_mode="HTML",reply_markup=markup)
    bot.register_next_step_handler(message,t1a1)


def t1a1(message):
    if message.text == "b":
        bot.send_message(message.chat.id,"Правильный ответ!✅")
        bot.delete_message(message.chat.id,message.message_id-1)
        time.sleep(2)
        bot.delete_message(message.chat.id,message.message_id+1)
        t1q2(message)

    else:
        bot.send_message(message.chat.id, "Неправильный овтет ❌"
                                          "\n\nПравильый ответ - Совокупность денег, активов и ресурсов, которыми располагают государства, компании и физические лица.")
        time.sleep(5)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id+1)
        t1q2(message)
def t1q2(message):
    markup = types.ReplyKeyboardMarkup()
    a = types.KeyboardButton('a')
    b = types.KeyboardButton('b')
    c = types.KeyboardButton('c')
    coin = 0
    markup.row(a, b, c)
    bot.send_photo(message.chat.id,
                   "https://1drv.ms/i/c/d59c6f998f225afd/IQO_jvdKPTWXTba-a7nXuMgJAe9wgjvyKPIFz9qKeienNlw?width=1024",
                   caption="<b>Какую роль играют финансы в экономической системе?</b>"
                           "\n\na) Они не играют никакой роли."
                           "\n\nb) Они только уменьшают расходы и поддерживают международный рынок."
                           "\n\nc) Они обеспечивают потоки денежных средств и финансовые операции.", parse_mode="HTML", reply_markup=markup)
    bot.register_next_step_handler(message, t1a2)

def t1a2(message):
    if message.text == "c":
        bot.send_message(message.chat.id,"Правильный ответ!✅")
        bot.delete_message(message.chat.id,message.message_id-1)
        time.sleep(2)
        bot.delete_message(message.chat.id,message.message_id+1)
        t1q3(message)

    else:
        bot.send_message(message.chat.id, "Неправильный овтет ❌"
                                          "\n\nПравильый ответ - Они обеспечивают потоки денежных средств и финансовые операции.")
        time.sleep(5)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id+1)
        t1q3(message)
def t1q3(message):
    markup = types.ReplyKeyboardMarkup()
    a = types.KeyboardButton('a')
    b = types.KeyboardButton('b')
    c = types.KeyboardButton('c')
    coin = 0
    markup.row(a, b, c)
    bot.send_photo(message.chat.id,
                   "https://1drv.ms/i/c/d59c6f998f225afd/IQPOctGtBSvlRKp-YYFKeBc1ASUov30aELiCDGN69eki6dM?width=1024",
                   caption="<b>Что включают корпоративные финансы?</b>"
                           "\n\na) Управление государственным долгом и налоговой политикой."
                           "\n\nb) Управление финансами предприятий и компаний, включая планирование, капитал и инвестиции."
                           "\n\nc) Только управление доходами и расходами физических лиц.", parse_mode="HTML",
                   reply_markup=markup)
    bot.register_next_step_handler(message, t1a3)
def t1a3(message):
    if message.text == "b":
        bot.send_message(message.chat.id,"Правильный ответ!✅")
        bot.delete_message(message.chat.id,message.message_id-1)
        time.sleep(2)
        bot.delete_message(message.chat.id,message.message_id+1)
        t1q4(message)

    else:
        bot.send_message(message.chat.id, "Неправильный овтет ❌"
                                          "\n\nУправление финансами предприятий и компаний, включая планирование, капитал и инвестиции.")
        time.sleep(5)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id+1)
        t1q4(message)
def t1q4(message):
    markup = types.ReplyKeyboardMarkup()
    a = types.KeyboardButton('a')
    b = types.KeyboardButton('b')
    c = types.KeyboardButton('c')
    coin = 0
    markup.row(a, b, c)
    bot.send_photo(message.chat.id,
                   "https://1drv.ms/i/c/d59c6f998f225afd/IQMUuxkgkqRGSqcTncWYKm58ASFzYoGMvV9OxBKZUEsCP2U?width=1024",
                   caption="<b>Что включают личные финансы?</b>"
                           "\n\na) Управление доходами, расходами, сбережениями и инвестициями."
                           "\n\nb) Только планирование пенсии."
                           "\n\nc) Управление государственным бюджетом.", parse_mode="HTML",
                   reply_markup=markup)
    bot.register_next_step_handler(message, t1a4)
def t1a4(message):
    if message.text == "a":
        bot.send_message(message.chat.id,"Правильный ответ!✅")
        bot.delete_message(message.chat.id,message.message_id-1)
        time.sleep(2)
        bot.delete_message(message.chat.id,message.message_id+1)
        t1q5(message)

    else:
        bot.send_message(message.chat.id, "Неправильный овтет ❌"
                                          "\n\nУправление доходами, расходами, сбережениями и инвестициями.")
        time.sleep(5)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id+1)
        t1q5(message)
def t1q5(message):
    markup = types.ReplyKeyboardMarkup()
    a = types.KeyboardButton('a')
    b = types.KeyboardButton('b')
    c = types.KeyboardButton('c')
    coin = 0
    markup.row(a, b, c)
    bot.send_photo(message.chat.id,
                   "https://1drv.ms/i/c/d59c6f998f225afd/IQN8ja6mJFZWSJyZuCAp2sSAAQNR6ULUfZJgfjfDrzz4QOs?width=1024",
                   caption="<b>Как финансовая грамотность помогает в жизни?</b>"
                           "\n\na) Мне ничем, я ведь ничего не знаю :("
                           "\n\nb) Помогает принимать обоснованные решения, минимизировать риски и достигать финансовых целей."
                           "\n\nc) Управление государственным бюджетом.", parse_mode="HTML",
                   reply_markup=markup)
    bot.register_next_step_handler(message, t1a5)
def t1a5(message):
    if message.text == "b":
        bot.send_message(message.chat.id,"Правильный ответ!✅")
        bot.delete_message(message.chat.id,message.message_id-1)
        time.sleep(2)
        bot.delete_message(message.chat.id,message.message_id+1)
        markup = types.ReplyKeyboardMarkup()
        btn_con = types.KeyboardButton("Продолжить")
        markup.add(btn_con)
        bot.send_
        bot.send_message(message.chat.id, "Ты справился с тестом! Перейдем к следующему модулю?", reply_markup=markup)
        bot.register_next_step_handler(message, Lesson_2)


    elif message.text == "c":
        bot.send_message(message.chat.id, "Неправильный овтет ❌"
                                          "\n\nПомогает принимать обоснованные решения, минимизировать риски и достигать финансовых целей.")
        time.sleep(5)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id+1)
        markup = types.ReplyKeyboardMarkup()
        btn_con = types.KeyboardButton("Продолжить")
        markup.add(btn_con)
        bot.send_message(message.chat.id, "Ты справился с тестом! Перейдем к следующему модулю?",reply_markup=markup)
        bot.register_next_step_handler(callback.message, Lesson_2)
    elif message.text == "a":
        bot.send_message(message.chat.id, "Ничего в этом страшного нет :)\n\nПосмотри следующий видеоролик про финансовую грамотность, чтобы быть осведомленным в этой теме!\n\n(псс правильным ответом был вариант под буквой b)"
                                          "https://youtu.be/a8kV0zVWRX4?si=n0xZxwZG8lrE0HyR")
        bot.delete_message(message.chat.id, message.message_id - 1)

        markup = types.ReplyKeyboardMarkup()
        btn_con = types.KeyboardButton("Продолжить")
        markup.add(btn_con)
        bot.send_message(message.chat.id, "Ты справился с тестом! Перейдем к следующему модулю?", reply_markup=markup)
        bot.register_next_step_handler(message, Lesson_2)

def Lesson_2(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "второй урок", reply_markup=markup)
@bot.message_handler()
def info(message):
    if any(word in message.text.lower() for word in ["хр","хрю","оньк","🐽"]):
        bot.send_message(message.chat.id, random.choice(["Хрю хрю!",
                                                         "Оньк хрррр оньк оньк",
                                                         "Ну и свинья....\nХрю оньк оньк!",
                                                         "Не увидел сразу в вас нетипичного пользователя телеграма! Ну чтож, хрю хрю!",
                                                         "хррр",
                                                         "👁🐽👁"]))
        bot.send_photo(message.chat.id,"https://1drv.ms/i/c/d59c6f998f225afd/IQN22fvhqKbmQrrqUrji3AtqAQ3w_GN-bbfUSmTGCt6qrsU?width=1024")
    else:
        bot.send_message(message.chat.id, random.choice(
            ["Да, это всё интересно, конечно.", "Понял тебя.. хотя может и не понял... в любом случае...", "Извольте.",
             "Хм, хорошо."]))
bot.polling(non_stop=True)