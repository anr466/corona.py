
import requests
from bs4 import BeautifulSoup
import time
import telebot
import schedule
# نضع التوكن لبوت التلقرام
TOKEN = "1041038137:AAEwfNa6L05P1EqcHGw_JsJ9VF4w6sxsF0o"
# لازم نضع المعرف الرقمي للقناه بالتلقرام
chat_id = '174958495'
#ربط التوكن مع مكتبة التلقرام
bot = telebot.TeleBot(TOKEN)
#الاوامر
#updater = Updater(token='TOKEN', use_context=True)
# الموقع المستخدم لجلب الحالات نضعه في متغير 
url = 'https://elaph.com/coronavirus-statistics-in-saudi-arabia.html'
#الاستجابه
response = requests.get(url)
#استعراض محتويات الموقع
page = response.content
#نستخدم المكتبه BeautifulSoup
#لا استعراض محتويات الموقع الاندكس بلغة html
soup = BeautifulSoup(page , 'html.parser')
# نبحث عن المحتوى النصي الذي نريد استخدامه او استعراضه من الموقع
class_for_confirmed_today = soup.find_all(class_='col-lg-6 col-xl-6')
#هذا الاستعلام يجلب لنا الحالات اليوميه
today_confirmed_number = [item.find(class_='mb-0 font-30 text-white').get_text() for item in class_for_confirmed_today]
lable_confirmed_today = [item.find(class_='card-title font-14 text-white').get_text() for item in class_for_confirmed_today]
# يجلب لنا جميع الحالات 
class_for_all_confirmed = soup.find_all(class_='col-lg-6 col-xl-4')
all_number_confirmed = [item.find(class_='card-title font-14 text-white').get_text() for item in class_for_all_confirmed]
lable_all_confirmed = [item.find(class_='mb-0 font-30 text-white').get_text() for item in class_for_all_confirmed]

try:
    def todayconfirmed():
        bot.send_message(chat_id,'الحالات اليوميه لمصابي فايروس كورونا بالسعوديه فور الاعلان عنها ')
        index1 = 0 
        # يعرض اصابات اليوم فقط
        for item in lable_confirmed_today:

            bot.send_message(chat_id,item)
            if item == lable_confirmed_today[0]:
                if today_confirmed_number[0] == "0":
                     bot.send_message(chat_id,"لم يتم التحديث بعد")
                else:
                     bot.send_message(chat_id,today_confirmed_number[0])
            elif item == lable_confirmed_today[1]:
                if today_confirmed_number[1] == "0":
                     bot.send_message(chat_id,"لم يتم التحديث بعد")
                else:
                     bot.send_message(chat_id,today_confirmed_number[1])
                
            elif item == lable_confirmed_today[2]:
                bot.send_message(chat_id,today_confirmed_number[2])
            elif item == lable_confirmed_today[3]:
                bot.send_message(chat_id,today_confirmed_number[3])
        index1 +=1
except:
        bot.send_message(chat_id, 'error')
try:
    def allconfirmed(): 
        index2 = 0 
        bot.send_message(chat_id,text = 'اجمالي عدد الحالات')
        for item in all_number_confirmed:
             bot.send_message(chat_id,item)
             if item == all_number_confirmed[0]:
                   bot.send_message(chat_id,lable_all_confirmed[0])
             elif item == all_number_confirmed[1]:
                 bot.send_message(chat_id,lable_all_confirmed[1])
             elif item == all_number_confirmed[2]:
                 bot.send_message(chat_id,lable_all_confirmed[2])
             elif item == all_number_confirmed[3]:
                 bot.send_message(chat_id,lable_all_confirmed[3])
        index2 +=1
except:
    bot.send_message(chat_id,'error')

    
def showbotdelay():

    return todayconfirmed() ,allconfirmed()






@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, f'الحالات اليوميه  {showbotdelay()}')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

schedule.every().hour.do(showbotdelay)

# البوت يعمل للابد
while True:
       # يعمل للاب
    bot.polling(none_stop=True)
    schedule.run_pending()
    time.sleep(15)