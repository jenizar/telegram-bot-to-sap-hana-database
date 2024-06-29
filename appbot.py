import json
import requests
import time
import urllib
from hdbcli import dbapi
from datetime import datetime

#import config


#https://api.telegram.org/bot<token>/METHOD_NAME
TOKEN = "<Telegram Bot TOKEN>" 
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
text2 = ""

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates, text3):
    for update in updates["result"]:
        text = update["message"]["text"]       
        chat = update["message"]["chat"]["id"]
        #send_message(text, chat)
        text2 = text 
    text3 = text2
    print(text3) 

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]  
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    #letter1 = 'Python Book Store. We sell Python books :'
    #letter2 = '1. Basic Python :  IDR 100.000'
    #letter3 = '2. Intermediate Python : IDR 200.000'
    #letter4 = '3. Advance Python : IDR 300.000.'
    #letter5 = ' Please type : 1, 2, 3' 
    #text = letter1 + letter2 + letter3 + letter4 + letter5

    text = ""
    chat = '453469622'    
    send_message(text, chat)
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        #print(updates)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            for update in updates["result"]:
                text = update["message"]["text"]       
                chat = update["message"]["chat"]["id"]      
            array = text.split(",")
            print(text)
            print(array)
            #idate1 = datetime.today().strftime('%Y-%m-%d')
            now = datetime.now() # current date and time
            idate1 = now.strftime("%d/%m/%Y, %H:%M:%S") 
            empid1 = array[0]
            storeid1 = array[1]
            barcode1 = array[2]
            stock1 = array[3]
            price1 = array[4]
            con = dbapi.connect(
            address="4b25c31e-9856-4586-a8d0-b1caa0f89d06.hana.trial-us10.hanacloud.ondemand.com",
            port=443,
            user="DBADMIN",
            password="MyHanadb911_")
            cur=con.cursor()
            sql = "INSERT INTO PYSTOCK.PRODUCT(idate, empid, storeid, barcode, stock, price) VALUES (?,?,?,?,?,?)"
            val = (idate1,empid1,storeid1,barcode1,stock1,price1)
            cur.execute(sql, val)
            con.commit()
        time.sleep(0.5)

if __name__ == '__main__':
      main()
