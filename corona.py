import requests
from bs4 import BeautifulSoup
import time ,os
import flask
from flask import Flask, request
import telebot
from telebot import types
import json
import newcaseincity

# نضع التوكن لبوت التلقرام
TOKEN = "token"
bot = telebot.TeleBot(TOKEN)


###############################
url = 'https://elaph.com/coronavirus-statistics-in-saudi-arabia.html'
response = requests.get(url)
page = response.content
soup = BeautifulSoup(page , 'html.parser')
#الحالات اليويمه
class_for_confirmed_today = soup.find_all(class_='col-lg-6 col-xl-6')
#الارقام
today_confirmed_number = [item.find(class_='mb-0 font-30 text-white').get_text() for item in class_for_confirmed_today]
lable_confirmed_today = [item.find(class_='card-title font-14 text-white').get_text() for item in class_for_confirmed_today]
#اجمالي الحالات
class_for_all_confirmed = soup.find_all(class_='col-lg-6 col-xl-4')
all_number_confirmed = [item.find(class_='card-title font-14 text-white').get_text() for item in class_for_all_confirmed]
lable_all_confirmed = [item.find(class_='mb-0 font-30 text-white').get_text() for item in class_for_all_confirmed]


################################
url2 = 'https://sehhty.com/sa-covid/'
response2 = requests.get(url2)
page2 = response2.content
soup2 = BeautifulSoup(page2 , 'html.parser')
citycard = soup2.find_all(class_='citycard')
#حالات اليوم
statscard = soup2.find_all(class_='statscard')

#المناطق اسماء
cardlabel = [item.find(class_='cardlabel').get_text(strip=True) for item in citycard ]
#الحالات اجمالي
cardcases = [item.find(class_='cardcases').get_text(strip=True) for item in citycard ]
#الحالات النشطة
cardactive = soup2.select('cardactive')
for cardactive in citycard:
    headline_text = cardactive.get_text(strip=True)
    #print(headline_text)

#التعافي
statsnum = [item.find(class_='statsnum').get('data-count') for item in statscard ]

#التعافي
cardcured = [item.find(class_='cardcured').get_text(strip=True) for item in citycard ]
#الوفيات
carddeath = [item.find(class_='carddeath').get_text(strip=True) for item in citycard ]


try:

    @bot.message_handler(commands=['start', 'الحالات','حالات اليوم','اصابات','اليوم','تقرير اليوم','حالات'])
    def todayconfirmed(message):
        chat_id = message.chat.id
        bot.send_message(chat_id,'الحالات اليوميه')
        index1 = 0
        index2 = 0
        # يعرض اصابات اليوم فقط
        for item in lable_confirmed_today:
            bot.send_message(chat_id,item)
            if item == lable_confirmed_today[0]:
                if today_confirmed_number[0] == "0":
                    bot.send_message(chat_id,"لم يتم التحديث بعد")
                else:
                    bot.send_message(chat_id,f'💔{today_confirmed_number[0]}')
            elif item == lable_confirmed_today[1]:
                if today_confirmed_number[1] == "0":
                    bot.send_message(chat_id,"لم يتم التحديث بعد")
                else:
                    bot.send_message(chat_id,f'😢{today_confirmed_number[1]}')
                    bot.send_message(chat_id,"التعافي 💚 ")
                    bot.send_message(chat_id,statsnum[4])
            elif item == lable_confirmed_today[2]:
                bot.send_message(chat_id,f'🌡‍️{today_confirmed_number[2]}')
            elif item == lable_confirmed_today[3]:
                bot.send_message(chat_id,f'💊{today_confirmed_number[3]}')
        index1 +=1
        bot.send_message(chat_id," اجمالي عدد الحالات📑 ")
        for item2 in all_number_confirmed:
            bot.send_message(chat_id,item2)
            if item2 == all_number_confirmed[0]:
                bot.send_message(chat_id,f'💔{lable_all_confirmed[0]}')
            elif item2 == all_number_confirmed[1]:
                bot.send_message(chat_id,f'💚{lable_all_confirmed[1]}')
            elif item2 == all_number_confirmed[2]:
                bot.send_message(chat_id,f'😢{lable_all_confirmed[2]}')
            elif item2 == all_number_confirmed[3]:
                bot.send_message(chat_id,f'{lable_all_confirmed[3]}')
        index2 +=1
        bot.send_message(chat_id,"بآمكانك الان البحث بآسم المدينة اكتب اسم المدينة فقط ")
except:
    print("werrr")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'هذي تحديثات اليوم {todayconfirmed}')

try:

    @bot.message_handler(func = lambda m: True)
    def echo_message(message):
        chat_id = message.chat.id
        bb= newcaseincity.hh
        vv= newcaseincity.vv
        healthytoday = newcaseincity.xx
        deathtoday = newcaseincity.zz
        text = message.text
        #bb = newcaseincity.newcasesincity(dd)
        for position, item in enumerate(cardlabel):
            if item == text:
                bot.send_message(chat_id,f'اخر تقرير محدث عن  {item} 📃 ')
                #bot.send_message(chat_id,position)
                bot.send_message(chat_id,'  حالات اليوم 😞 ')
                bot.send_message(chat_id,bb[position])
                bot.send_message(chat_id,'  حالات التعافي اليوم 😊')
                bot.send_message(chat_id,healthytoday[position])
                bot.send_message(chat_id,'  وفيات اليوم 😣')
                bot.send_message(chat_id,deathtoday[position])
                bot.send_message(chat_id,f'  اجمالي عدد الحالات في  {item}  👀 ')
                bot.send_message(chat_id,cardcases[position])
                bot.send_message(chat_id,'  اجمالي الحالات النشطة 😕')
                bot.send_message(chat_id,vv[position])
                bot.send_message(chat_id,'   اجمالي حالات التعافي 💚')
                bot.send_message(chat_id,cardcured[position])
                bot.send_message(chat_id,' اجمالي الوفيات 😢')
                bot.send_message(chat_id,carddeath[position])
                bot.send_message(chat_id,'لعرض جميع الحالات لهذا اليوم اضغط على /start')
                break
        if item != text:
            bot.send_message(chat_id,'تاكد من كتابة اسم المدينة او المنطقة !! 😇  ')

except:
    print("erooor")



try:
    while True:

        bot.polling(none_stop=True)
except:

    time.sleep(10)




