import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers = headers)
soup = BeautifulSoup(data.text, 'html.parser')
chart = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for song in chart:
    ranking_text = song.find('td.number > #text')
    if ranking_text == None:
        continue
    ranking =chart.select('td.number > #text')[0].get_text()
    title = chart.select('a.title.ellipsis')[0].get_text()
    artist = chart.select('a.artist.ellipsis')[0].get_text()
    db.music.insert_one({'ranking': ranking, 'title': title, 'artist': artist})
    print(ranking, title, artist)