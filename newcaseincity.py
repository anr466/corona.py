import requests
from bs4 import BeautifulSoup
import time
import telebot
import re

# نضع التوكن لبوت التلقرام
TOKEN = "1041038137:AAEwfNa6L05P1EqcHGw_JsJ9VF4w6sxsF0o"

bot = telebot.TeleBot(TOKEN)



##########################################
#اصابات المدن الجديده
hh = []
url3 = 'https://sehhty.com/sa-covid1/'
response3 = requests.get(url3)
page3 = response3.content
soup3 = BeautifulSoup(page3 , 'html.parser')
table = soup3.find('table',id='sacasestoday')
for body in table.find_all('tbody'):
    rows = body.find_all('tr')
    for row in rows:
        pp = row.find('td',style='background:#5d10cc;color:white;')
        if pp:
            dd = pp.get_text().strip('+')
            hh.append(dd)




########الحالات النشطة###########
vv = []

for body in table.find_all('tbody'):
    rows = body.find_all('tr')
    for row in rows:
        pp = row.find('td',style='color: #f39219;')
        if pp:
            dd = pp.get_text().strip('%')
            qq = dd[:-3]
            vv.append(qq)    


########التعافي الجديدة ###########
xx = []
for body in table.find_all('tbody'):
    rows = body.find_all('tr')
    for row in rows:
        pp = row.find('td',style='background:#2fab4b;color:white;')
        if pp:
            dd = pp.get_text().strip('+')
            xx.append(dd)




########الوفيات الجديدة ###########
zz = []
for body in table.find_all('tbody'):
    rows = body.find_all('tr')
    for row in rows:
        pp = row.find('td',style='background:#bb3441;color:white;')
        if pp:
            dd = str(pp.get_text().strip('+'))
            zz.append(dd)



