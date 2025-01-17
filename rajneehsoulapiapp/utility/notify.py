import datetime
import pytz
import tzlocal
from sqlite3 import connect
from os import path
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin import *

ROOT=path.dirname(path.realpath(__file__))
db = connect(path.join(ROOT,'db.sqlite3'))
print("ROOT",ROOT)
print("db:",db)

weatherType = ""

userAdditionalDetails = connect(path.join(ROOT,'db.sqlite3'))
userAdditionalDetailsQuery = userAdditionalDetails.execute(" select * from selApp_useradditionalinfo")
userAdditionalDetailsList = userAdditionalDetailsQuery.fetchall()
print("userAdditionalDetailsList:->-------------------------> ",userAdditionalDetailsList)
userAdditionalDetailsDict = {}
for i in range(len(userAdditionalDetailsList)):
    userAdditionalDetailsDict[userAdditionalDetailsList[i][2]] = userAdditionalDetailsList[i][1]

print("userAdditionalDetailsDict:->-------------------------> ",userAdditionalDetailsDict)

#----------------------------------------#

channelList = ["TICKETS", "TRANSACTIONS"]
deepLinkList = ["NOTIFICATION_CALLBACK_TICKETS", "NOTIFICATION_CALLBACK_TRANSACTIONS",
                "NOTIFICATION_CALLBACK_GAME_PLAY"]
indexx = 0
ROOT=path.dirname(path.realpath(__file__))

cred = credentials.Certificate(path.join(ROOT,'smartelist.json'))
firebase_admin.initialize_app(cred)

def sendPush(channelData, deeplinkData,  body, token, weatherType, uniqueId, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        data={

            'body': body,
            'title': "Weather Notification",
            'weatherType': weatherType,
            'uniqueId': str(uniqueId),
            'channel': "ALERT1",
            'displayNotification': 'YES'
        },
        tokens=[token]
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


#-------------------------------------------#

"""fr = db.execute(" select * from enroll_expired_scheduledlist")
frow = fr.fetchall()

pn_r = db.execute("select * from enroll_pin_unpin")
pn_r_row = pn_r.fetchall()"""

cur = db.execute(" select * from selApp_scheduleitemlist")
row = cur.fetchall()

#////////////////////////




print("Row:", row)
for i in range(len(row)):
    print("Row -->", row)
    current_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
   # current_utc_time = current_local_time
    #local_timezone = tzlocal.get_localzone()
    #print("Current UTC Time to Local Time : ",
     #     x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))
    x = current_local_time.strftime('%Y-%m-%d %H:%M:%S')
    current_date_time_object = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    print("row[i][4]: ",row[i][4]) # """ row[i][4] gives pinned data """
    print("++++++++++++++++++++++++++++++++++++>" * 2)

    if (row[i][4] == '0'):
        print("------------------------------------->")
        scheduled_datetime_object = datetime.datetime.strptime(row[i][2] + " " + row[i][1], '%d-%m-%Y %H:%M:%S')
        print("scheduled_datetime_object", scheduled_datetime_object)
        print("diff : total seconds:-> ", (current_date_time_object - scheduled_datetime_object).total_seconds())
        print("------------------------------------->")
        if (current_date_time_object - scheduled_datetime_object).total_seconds()/60 > 0:
            print("------------------------------------->" * 20)
            print()
            print("delete it")
            cur.execute(" insert into selApp_expireditemlist(id, expired_time, expired_date, scheduleItem, user_id, pinned)values(?,?,?,?,?,?)",(row[i][0],row[i][1],row[i][2],row[i][3],row[i][6],row[i][4]))
            cur.execute(" delete from selApp_scheduleitemlist where time=?",(row[i][1],))
            db.commit()
        else:
            print(" abhi time h")


"""    for j in range(len(pn_r_row)):
        if int(row[i][0]) == int(pn_r_row[j][1]):
          if int(pn_r_row[j][2]) == 1:
            xg = 1
            break
        else:
            xg = 0
"""

"""
    if xg != 1:
            y=row[i][2]+" "+row[i][3]
            y=datetime.datetime.strptime(y,'%Y-%m-%d %H:%M:%S')
            print("scheduled Time :",y)
            print("local time :",x)
            difference = y - x
            print("difference :",difference)
            print("type(difference) :",type(difference))
            print("difference.total_seconds()",difference.total_seconds())
            print("type(difference.total_seconds())",type(difference.total_seconds()))
            if difference.total_seconds()/60 < 0:
                    print()
                    print(difference.total_seconds()/60," delete it")
                    cur.execute(" insert into enroll_expired_scheduledlist(id,schedule_items,schedule_date,schedule_time,user_id)values(?,?,?,?,?)",(row[i][0],row[i][1],row[i][2],row[i][3],row[i][4],))
                    cur.execute(" delete from enroll_scheduled where schedule_time=?",(row[i][3],))
                    db.commit()
            else:
                    print()
                    print(difference.total_seconds()/60," abhi time h")

    else:
        print("PINNED !")
"""




#///////////////////////
"""
print("Row:", row)
for i in range(len(row)):
    current_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
   # current_utc_time = current_local_time
    #local_timezone = tzlocal.get_localzone()
    #print("Current UTC Time to Local Time : ",
     #     x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))
    x=current_local_time
    x = x.strftime('%Y-%m-%d %H:%M:%S')
    x = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    xg = 0
    for j in range(len(pn_r_row)):
        if int(row[i][0]) == int(pn_r_row[j][1]):
          if int(pn_r_row[j][2]) == 1:
            xg = 1
            break
        else:
            xg = 0
    if xg != 1:
            y=row[i][2]+" "+row[i][3]
            y=datetime.datetime.strptime(y,'%Y-%m-%d %H:%M:%S')
            print("scheduled Time :",y)
            print("local time :",x)
            difference = y - x
            print("difference :",difference)
            print("type(difference) :",type(difference))
            print("difference.total_seconds()",difference.total_seconds())
            print("type(difference.total_seconds())",type(difference.total_seconds()))
            if difference.total_seconds()/60 < 0:
                    print()
                    print(difference.total_seconds()/60," delete it")
                    cur.execute(" insert into enroll_expired_scheduledlist(id,schedule_items,schedule_date,schedule_time,user_id)values(?,?,?,?,?)",(row[i][0],row[i][1],row[i][2],row[i][3],row[i][4],))
                    cur.execute(" delete from enroll_scheduled where schedule_time=?",(row[i][3],))
                    db.commit()
            else:
                    print()
                    print(difference.total_seconds()/60," abhi time h")

    else:
        print("PINNED !")

for i in range(len(frow)):
    current_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
   # current_utc_time = current_local_time
    #local_timezone = tzlocal.get_localzone()
    #print("Current UTC Time to Local Time : ",
     #     x := current_utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata')))
    x=current_local_time
    x = x.strftime('%Y-%m-%d %H:%M:%S')
    x = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    xy=frow[i][2]+" "+frow[i][3]
    xy = datetime.datetime.strptime(xy, '%Y-%m-%d %H:%M:%S')
    df = x - xy
    print()
    print("df.total_seconds()/60 : ",df.total_seconds()/60)
    print()
    if df.total_seconds()/60 > 1:
         cur.execute(" delete from enroll_expired_scheduledlist where schedule_time=?", (frow[i][3],))
         print("delete from expired list")
         db.commit()
    else:
        print("abhi ni :",df.total_seconds()/60)
"""

print("/"*200)

#############################################################################################

# check and deleted first !
connecting_to_db = connect(path.join(ROOT,'db.sqlite3'))
sqlite_select_query = connecting_to_db.execute('DELETE FROM selApp_weather_ackno')
connecting_to_db.commit()

##############################################################################################
# Weather API + its Logic + Mail Acknowledgement

import requests
import json
from sqlite3 import connect
from datetime import datetime
import pytz

LIST = []

current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))
current_time = current_local_time.strftime('%d-%m-%Y %H:%M')
current_datetime_object = datetime.strptime(current_time, '%d-%m-%Y %H:%M')

xc = current_local_time.strftime('%d-%m-%Y')
xd = xc.split('-')


con = connect(path.join(ROOT,'db.sqlite3'))
cur = con.execute(" select * from selApp_scheduleitemlist")
row = cur.fetchall()
print("row:",row)


"""cityQuery = con.execute("select * from selApp_City")
cityDetailsList = cityQuery.fetchall()
cityDetailsDict = {}
for i in range(len(cityDetailsList)):
    cityDetailsDict[cityDetailsList[i][2]] = cityDetailsList[i][1]

print("cityDetailsDict: ", cityDetailsDict)"""

uniqueId = 0

for i in row:
    print('i[2]:', i[2])
    I = i[3]

    scheduleWholeTime = i[1].split(":")
    scheduleWholeDate = i[2].split("-")

    scheduleItemName = i[3]

    print("scheduleWholeDate: ", i[1].split(":"))
    print("scheduleWholeDate: ", i[2].split("-"))
    print("scheduleItemName: ", scheduleItemName)
    user_id = i[5] # """ i[5] gives foreignkey user_id """
    print("user_id: ", user_id)

    schedule_date = int(scheduleWholeDate[0])
    print("schedule_date:", schedule_date)
    schedule_month = int(scheduleWholeDate[1])
    print("schedule_month:", schedule_month)
    schedule_year = int(scheduleWholeDate[2])
    print("schedule_year:", schedule_year)

    schedule_hour = int(scheduleWholeTime[0])
    print("schedule_hour: ", schedule_hour)
    schedule_minute = int(scheduleWholeTime[1])
    print("schedule_minute: ", schedule_minute)

    present_date = int(xd[0])
    print("present_date:", int(xd[0]))
    present_month = int(xd[1])
    print("present_month:", present_month)

    api_address = "https://api.openweathermap.org/data/2.5/forecast?appid=61d38a3c289f168e130b1fa745c9a37c&q="
    """
    if (cityDetailsDict.get(user_id)==None):
        print("->"*80)
        print("user_id ----> ",user_id)
        print("cityDetailsDict.get(user_id)",cityDetailsDict.get(user_id))
        continue
    else:
        print("-----)"*80)
        print("cityDetailsDict.get(user_id)", cityDetailsDict.get(user_id))
        url = api_address + cityDetailsDict.get(user_id)
    """
    url = api_address + "Gurugram"
    json_data = requests.get(url).json()
    json_string = json.dumps(json_data, indent=4)
    data = json.loads(json_string)
    ################################################################################################################
    l = []
    mon = {'lp': {1: 31,  2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31},
    'nlp': {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}}

    if schedule_year % 100 == 0:
        if schedule_year % 400 == 0:
            mon = mon["lp"]
        else:
            mon = mon["nlp"]
    else:
        if schedule_year % 4 == 0:
            mon = mon["lp"]
        else:
            mon = mon["nlp"]
    print("mon:",mon)
    to_see_for = []
    if schedule_date == 1:
        if present_month == schedule_month -1:
            sm = int(schedule_month) - 1
            having_days = mon[sm]
            for i in range(2):
                to_see_for.append(having_days-i)
    elif schedule_date == 2:
       if present_date + 1 != schedule_date:
         if present_month == schedule_month - 1:
             sm = int(schedule_month) - 1
             having_days = mon[sm]
             to_see_for.append(having_days)
         if schedule_month == present_month + 1:
             to_see_for.append(1)
       else:
           to_see_for.append(1)

    else:
        if present_month == schedule_month:
            having_days = schedule_date
            for i in range(1,3):
                to_see_for.append(having_days-i)

    print("to see for :",to_see_for)
    print("_"*300)
    for i in data['list']:
        print(i)
    print("_"*300)
    extract_weatherdata = []
    for i in range(len(data['list'])):
        weathers_date_time = data['list'][i]['dt_txt']
        weathers_date_time = weathers_date_time.split(" ")
        weathers_date = weathers_date_time[0]
        wsd = weathers_date.split("-")
        wsd_only_date = wsd[2]
        if len(to_see_for)!=0:
           if len(to_see_for) != 1:
             if to_see_for[1] == present_date or to_see_for[0] == present_date :
                if schedule_date == int(wsd_only_date):
                    extract_weatherdata.append(data['list'][i])
           else:
             if to_see_for[0] == present_date :
                if schedule_date == int(wsd_only_date):
                   extract_weatherdata.append(data['list'][i])

    print("extract_weatherdata :",extract_weatherdata)
    for j in extract_weatherdata:
        print(j)
    ##################################################################################################################
    checking_time = schedule_hour + schedule_minute / 100
    print("checking_time:",checking_time)
    print("-"*50)
    #################################################################################################################
    for i in range(len(extract_weatherdata)):
        extract_weathersdata_weathers_date_time = extract_weatherdata[i]['dt_txt']
        extract_weathersdata_weathers_date_time = extract_weathersdata_weathers_date_time.split(" ")
        extract_weathersdata_weathers_time = extract_weathersdata_weathers_date_time[1]
        e_wst = extract_weathersdata_weathers_time.split(":")
        e_wst_only_hour = e_wst[0]
        print("int(e_wst_only_hour) - 3 :",int(e_wst_only_hour) - 3)
        print("checking_time:",checking_time)
        print("int(e_wst_only_hour):",int(e_wst_only_hour))
        if int(e_wst_only_hour) - 3 <= checking_time <= int(e_wst_only_hour):
            if 0 <= schedule_hour < 12:
                gmt = 'A.M'
            elif 12 <= schedule_hour <= 23:
                gmt = 'P.M'

            current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))

            if extract_weatherdata[i-1]['weather'][0]['description'] == 'clear sky':
                          print(" extract_weatherdata['list'][i-1]['weather'][0]['description'] ",extract_weatherdata[i-1]['weather'][0]['description'])
                          weatherType = extract_weatherdata[i-1]['weather'][0]['description']
                          temp_max = "{:.2f}".format(float(extract_weatherdata[i-1]['main']['temp_max']) - 273.15) + " " + u"\u2103"
                          LIST.append(extract_weatherdata[i-1]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item : " + I + " on " + str(
                          schedule_date) + " - " + str(schedule_month) + " - " + str(schedule_year) + " at " + str(schedule_hour) + ":" + str(
                          schedule_minute) + " " + str(gmt))
                          LIST.append(uniqueId)
                          uniqueId += 1

                          body = extract_weatherdata[i-1]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item : " + I + " on " + str(
                          schedule_date) + " - " + str(schedule_month) + " - " + str(schedule_year) + " at " + str(schedule_hour) + ":" + str(
                          schedule_minute) + " " + str(gmt)

                          userFcmToken = userAdditionalDetailsDict.get(user_id)
                          print("." * 70)
                          print("user_id: ", user_id)
                          print("userFcmToken: ", userFcmToken)
                          print("." * 70)
                          if userFcmToken is not None:
                              sendPush(channelList[indexx], deepLinkList[indexx], body, userFcmToken, weatherType, LIST[1])

            else:
                          print("extract_weatherdata['list'][i-1]['weather'][0]['description']",extract_weatherdata[i-1]['weather'][0]['description'])
                          weatherType = extract_weatherdata[i-1]['weather'][0]['description']
                          temp_max = "{:.2f}".format(float(extract_weatherdata[i-1]['main']['temp_max']) - 273.15) + " " + u"\u2103"
                          LIST.append(extract_weatherdata[i-1]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item: " + I + " on " + str(
                                  schedule_date) + " - " + str(schedule_month) + " - " + str(
                                  schedule_year) + " at " + str(schedule_hour) + ":" + str(
                                  schedule_minute) + " " + str(gmt))
                          LIST.append(uniqueId)
                          uniqueId += 1

                          body = extract_weatherdata[i-1]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item: " + I + " on " + str(
                                  schedule_date) + " - " + str(schedule_month) + " - " + str(
                                  schedule_year) + " at " + str(schedule_hour) + ":" + str(
                                  schedule_minute) + " " + str(gmt)
                          userFcmToken = userAdditionalDetailsDict.get(user_id)
                          print("."*70)
                          print("userFcmToken: ", userFcmToken)
                          print("."*70)
                          if userFcmToken is not None:
                              sendPush(channelList[indexx], deepLinkList[indexx], body, userFcmToken, weatherType, LIST[1])

        elif checking_time > 21 or checking_time == 21.0:
            if int(e_wst_only_hour) == 21:
                if 0 <= schedule_hour < 12:
                          gmt = 'A.M'
                elif 12 <= schedule_hour <= 23:
                          gmt = 'P.M'

                          print("else part 21 ~ 24 ")

                current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))

                print("extract_weatherdata[i] :",extract_weatherdata[i])
                if extract_weatherdata[i]['weather'][0]['description'] == 'clear sky':
                    print(" extract_weatherdata['list'][i]['weather'][0]['description'] EA",
                          extract_weatherdata[i]['weather'][0]['description'])
                    weatherType = extract_weatherdata[i]['weather'][0]['description']
                    temp_max = "{:.2f}".format(float(extract_weatherdata[i]['main']['temp_max']) - 273.15) + " " + u"\u2103"
                    LIST.append(
                        extract_weatherdata[i]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item : " + I + " on " + str(
                            schedule_date) + " - " + str(schedule_month) + " - " + str(
                            schedule_year) + " at " + str(schedule_hour) + ":" + str(
                            schedule_minute) + " " + str(gmt))
                    LIST.append(uniqueId)
                    uniqueId += 1

                    body = extract_weatherdata[i]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item: " + I + " on " + str(schedule_date) + " - " + str(schedule_month) + " - " + str(
                                  schedule_year) + " at " + str(schedule_hour) + ":" + str(
                                  schedule_minute) + " " + str(gmt)
                    userFcmToken = userAdditionalDetailsDict.get(user_id)
                    if userFcmToken is not None:
                          sendPush(channelList[indexx], deepLinkList[indexx], body, userFcmToken, weatherType, LIST[1])
                else:
                    print("extract_weatherdata['list'][i]['weather'][0]['description'] EB",
                          extract_weatherdata[i]['weather'][0]['description'])
                    weatherType = extract_weatherdata[i]['weather'][0]['description']
                    temp_max = "{:.2f}".format(float(extract_weatherdata[i]['main']['temp_max']) - 273.15) + " " + u"\u2103"
                    LIST.append(
                        extract_weatherdata[i]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item : " + I + " on " + str(
                            schedule_date) + " - " + str(schedule_month) + " - " + str(
                            schedule_year) + " at " + str(schedule_hour) + ":" + str(
                            schedule_minute) + " " + str(gmt))
                    LIST.append(uniqueId)
                    uniqueId += 1

                    body = extract_weatherdata[i]['weather'][0]['description'] + " day on your Scheduled Day, You have scheduled for an item: " + I + " on " + str(schedule_date) + " - " + str(schedule_month) + " - " + str(
                                  schedule_year) + " at " + str(schedule_hour) + ":" + str(
                                  schedule_minute) + " " + str(gmt)
                    userFcmToken = userAdditionalDetailsDict.get(user_id)
                    if userFcmToken is not None:
                          sendPush(channelList[indexx], deepLinkList[indexx], body, userFcmToken, weatherType, LIST[1])

    print("user_id :",user_id)
    ###############################################################################################################
    ###############################################################################################################

    if len(LIST)!=0:
        connecting_to_db = connect(path.join(ROOT,'db.sqlite3'))
        current_local_time = datetime.now(pytz.timezone('Asia/Kolkata'))

        sqlite_insert_query =  connecting_to_db.execute("""INSERT INTO selApp_weather_ackno(user_id, messages, time_of_message, messages_alert, weatherType,maxTemp)VALUES(?,?,?,?,?,?)""",(user_id,LIST[0],str(current_local_time),LIST[1], weatherType, temp_max))
        connecting_to_db.commit()
    LIST=[]
    extract_weatherdata=[]
    print("-"*100)

#  sendPush(channelList[indexx], deepLinkList[indexx], )
