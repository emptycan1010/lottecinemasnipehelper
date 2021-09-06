#!/usr/bin/env python
# coding: utf-8

# In[101]:


import requests
import telegram
import json
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup
webhook = "yourDiscordWebhook Here"
url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
token = "YourTelegramTokenhere"
bot = telegram.Bot(token)
dic = {"MethodName": "GetPlaySequence",
       "channelType": "MA",
       "osType": "",
       "osVersion": "",
       "playDate": "2021-09-09", # 날짜. 과거로 설정해둘시 가장 최근의 시간표를 보여줌.
       "cinemaID": "1|1|영화관의 ID", 
       "representationMovieCode": ""} # 영화 ID, 공백시 모든영화 로딩
parameters = {"paramList": str(dic)}
response = requests.post(url, data = parameters).json()
print("\n")

# In[102]:


# response


# In[103]:


movies_response = response['PlaySeqs']['Items']


# In[104]:


def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    for movie_no in movie_no_list:
        movies = [item for item in response if item["MovieCode"] == movie_no]
        title = movies[0]["MovieNameKR"]
        timetable = get_time_table(movies)
        print(title, timetable, "\n")
        file = open('2009.txt', 'r')
        num = file.read()
        if num < "111111":
            if title == "**영화의 정확한 명칭**":
                print ('예매 오픈!')
                bot.send_message(chat_id=yourChannelID, text= title + " 예매 오픈! 시간 : " + str(timetable)) # 텔레그램 전송용
                data = { # 디스코드 전송용
                    "content" : "@everyone",
                    "username" : " Notifier"
                }
                data["embeds"] = [
                    {
                        "description" : title,
                        "url" : "https://www.lottecinema.co.kr/NLCHS/Ticketing#none",
                        "title" : "영화 예매하러가기"}
                ]
                result = requests.post(webhook, json = data)

                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(err)
                else:
                    print("Payload delivered successfully, code {}.".format(result.status_code));# In[ ]:
                file = open('2009.txt', 'w')
                file.write(num + "1")
        

        
def get_movie_no_list(response):
    movie_no_list = []
    for item in response:
        movie_no = item["MovieCode"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    print("광복notfound")
    return movie_no_list



def get_time_table(movies):
    tuples = []
    for movie in movies:
        time = movie["StartTime"]
        seats = movie["BookingSeatCount"]
        tuple = (time, seats)
        tuples.append(tuple)
    return tuples


# In[105]:


split_movies_by_no(movies_response)
