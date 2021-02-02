from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"

OPEN_WEATHER_KEY = 'd0fb542bf2fee380d2adb9b72da1403d' #key API ต้อง crete ขึ้นมาเอง

OPEN_NEW_URL = "http://newsapi.org/v2/everything?q={0}&from=2021-02-01&sortBy=publishedAt&apiKey={1}"

OPEN_NEW_KEY = "176b3912788048c78981e6f2d4381617"

@app.route("/")
def home():
    city = request.args.get('city')  #สามารถส่ง parameter ทางหน้าหลักได้ ตรง url
    if not city:
        city = 'bangkok' #set กรุงเทพเป็นหลัก ถ้าไม่ได้ส่งค่ามา
    weather = get_weather(city, OPEN_WEATHER_KEY)

    new = get_new('covid-19',OPEN_NEW_KEY)

    return render_template("home.html", weather=weather,new=new)



def get_new(news,OPEN_NEW_KEY):

    query = quote(news)

    url = OPEN_NEW_URL.format(news,OPEN_NEW_KEY) 

    data = urlopen(url).read() #ยิง request ไป ตอบกลับมาเป็น json xml

    parsed = json.loads(data)

    news = None
    Arr = []
    for x in range (5):
        if parsed.get('articles'):

            title = parsed['articles'][x]['title']
            description = parsed['articles'][x]['description']
            url = parsed['articles'][x]['url']
            urlToImage = parsed['articles'][x]['urlToImage']

            news = { 'title': title,  
                     'description': description,
                     'url': url,
                     'urlToImage': urlToImage
                   
                   }
            Arr.append(news)
                   
    return Arr

    

def get_weather(city,API_KEY):

    query = quote(city)

    url = OPEN_WEATHER_URL.format(city, API_KEY) #สร้างมาเพื่อเก็บตัวเเปรมาไว้ใน {0}

    data = urlopen(url).read() #ยิง request ไป ตอบกลับมาเป็น json xml

    parsed = json.loads(data)

    weather = None
    if parsed.get('weather'): #check ว่า สามารถ get key weather ได้รึเปล่า

        description = parsed['weather'][0]['description']
        temperature = parsed['main']['temp']
        city = parsed['name']
        country = parsed['sys']['country']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        speed = parsed['wind']['speed']
        icon = parsed['weather'][0]['icon']


        weather = {'description': description,   #ประกาศตัวเเปร weather เป็น dictionary เป็นรวม
                   'temperature': temperature,
                   'city': city,
                   'country': country,
                   'pressure' : pressure,
                   'humidity' : humidity,
                   'speed' : speed,
                   'icon' : icon
                   }
    return weather


    


@app.route('/news')
def news():
    newk = request.args.get('newk')  #สามารถส่ง parameter ทางหน้าหลักได้ ตรง url
    if not newk:
        newk = "music" 
    new = get_newz(newk,OPEN_NEW_KEY)

    

    return render_template('news.html', new=new)

def get_newz(news,OPEN_NEW_KEY):

    query = quote(news)

    url = OPEN_NEW_URL.format(news,OPEN_NEW_KEY) 

    data = urlopen(url).read() #ยิง request ไป ตอบกลับมาเป็น json xml

    parsed = json.loads(data)

    news = None
    Arr = []
    if parsed.get('articles'):

        for x in parsed['articles']:
            title = x['title']
            description = x['description']
            url = x['url']
            

            news = { 'title': title,  
                     'description': description,
                     'url': url
                   }
            Arr.append(news)
                   
    return Arr


@app.route('/about')
def about():
   return render_template('about.html')


app.env="development"
app.run(debug=True)