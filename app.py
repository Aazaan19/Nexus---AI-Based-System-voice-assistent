
import ctypes
from anyio import sleep
from flask import *
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
from fpdf import FPDF
from os.path import exists
import os
import platform
import json
import smtplib
from platformdirs import user_data_dir
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from flask import request
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
import time
import random
import ecapture as ec
from asyncio import sleep
import socket
import subprocess
import qrcode
import speedtest
import pyautogui
import re
import wolframalpha
import pyjokes as pyjokes
from PIL import Image, ImageGrab 
import geocoder
from geopy.geocoders import Nominatim
import pymysql
from pytube import YouTube



headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}




app = Flask(__name__)
app.secret_key = 'random string'

def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="NexusDB")
    return connection


#close DB connection
def dbClose():
    dbConnection().close()
    return

#global city

#logout code
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/home', methods = ['POST', 'GET'])
def home():
    global city
    import geocoder
    g = geocoder.ip('me')
    print(g.latlng)

    latitudeData = str(g.latlng[0])
    longitudeData = str(g.latlng[1])
    print()
    print(latitudeData, longitudeData)
    print()

    coordinates =(latitudeData, longitudeData)
    
    geoLoc = Nominatim(user_agent="GetLoc")
        
    # passing the coordinates
    locname = geoLoc.reverse(coordinates)
     
    # printing the address/location name
    print(locname.address)
   
    Address = locname.address
    
    Address = Address.split(',')
    #print("Address:")
    #print(Address)
    city = Address[1]
    #print("city="+city)
    
    return render_template("index.html")

@app.route('/about', methods = ['POST', 'GET'])
def about():
    return render_template("about.html")

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    return render_template("contact.html")

@app.route('/webSpeech', methods = ['POST', 'GET'])
def webSpeech():
    return render_template("webSpeech.html")

@app.route('/', methods=["GET","POST"])
def login():
    msg = ''
    if request.method == "POST":
        # session.pop('user',None)
        mobno = request.form.get("mobno")
        password = request.form.get("pas")
        # print(mobno+password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM userdetails WHERE mobile = %s AND password = %s',
                                      (mobno, password))
        if result_count > 0:
            print(result_count)
            session['user'] = mobno
            return redirect(url_for('home'))
            # return jsonify(dict(redirect='home'))
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
    return render_template('login.html')



@app.route('/register', methods=["GET","POST"])
def register():
    print("register")
    if request.method == "POST":
        try:
            name = request.form.get("name")
            address = request.form.get("address")
            mailid = request.form.get("mailid")
            mobile = request.form.get("mobile")
            pass1 = request.form.get("pass1")

            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM userdetails WHERE mobile = %s', (mobile))
            res = cursor.fetchone()
            if not res:
                sql = "INSERT INTO userdetails (name, address, email, mobile, password) VALUES (%s, %s, %s, %s, %s)"
                val = (name, address, mailid, mobile, pass1)
                cursor.execute(sql, val)
                con.commit()
                status= "success"
                print(status)
                #return redirect(url_for('login'))
                return redirect(url_for('login'))
            else:
                status = " Mobile no. already Registered"
            return status
        except:
            print("Exception occured at user registration")
            return redirect(url_for('login'))
        finally:
            dbClose()
    return render_template('register.html')






@app.route('/command', methods = ['POST', 'GET'])
def command():
    #global city
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices[1].id)
    engine.setProperty('voice', voices[0].id)


    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    def pdf_converter(Text):
        # save FPDF() class into a
        # variable pdf
            pdf = FPDF()

        # Add a page
            pdf.add_page()

        # set style and size of font
        # that you want in the pdf
            pdf.set_font("Arial", size = 15)

        # create a cell
            pdf.cell(200, 10, txt = "Your Data is ",
                ln = 1, align = 'C')

        # add another cell
            pdf.cell(200, 10, txt = Text,ln = 2, align = 'C')

        # save the pdf with name .pdf
            if exists("voiceTotext.pdf"):
                os.remove("voiceTotext.pdf")
                time.sleep(3)
                pdf.output("voiceTotext.pdf") 
            else:
                pdf.output("voiceTotext.pdf")

    

    def wishMe():
        try:
            hour = int(datetime.datetime.now().hour)
            if hour>=0 and hour<12:
                speak("Good Morning!")
                speak("I am Nexus. Please tell me how may I help you") 
            elif hour>=12 and hour<18:
                speak("Good Afternoon!")   
                speak("I am Nexus. Please tell me how may I help you") 
            else:
                speak("Good Evening!")  
                speak("I am Nexus. Please tell me how may I help you") 
            
        except Exception as e:
            print(e)
    
    def htLine1(coinRes):
        return speak("It's " + coinRes)


    def htLine2(coinRes):
        return speak("You got " + coinRes)


    def htLine3(coinRes):
        return speak("It landed on " + coinRes)  

    # function for dino game
    def click(key):
        pyautogui.keyDown(key)
        return

    def isCollision(data):
    # Check colison for birds
        for i in range(530,560):
            for j in range(160, 195):
                if data[i, j] < 100:
                    click("down")
                    return

    # Check colison for cactus
        for i in range(530, 620):
            for j in range(200, 230):
                if data[i, j] < 100:
                    click("up")
                    return
        return         
    
    def Download(finallink):
        # python tutorial
        print(finallink)
        ############################################    Get youtube links    ############################################################
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.maximize_window()
        driver.implicitly_wait(30)
        wait = WebDriverWait(driver, 30)

        driver.get("https://www.youtube.com/results?search_query=%22"+finallink+"%22")

        size = driver.find_elements(By.XPATH, "//ytd-thumbnail[@class='style-scope ytd-video-renderer']")
        Mylist = []
        videolink = []
        mintime_index = 0
        j = 1
        for i in range(len(size)-4):
            element = driver.find_element(By.XPATH, f"(//ytd-thumbnail[@class='style-scope ytd-video-renderer'])[{j}]")
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            thumbnail_href = element.find_element(By.XPATH, ".//a").get_attribute('href')
            #print(thumbnail_href)
            time = element.find_element(By.XPATH, ".//descendant::span[contains(@class,'ytd-thumbnail-overlay-time-status-renderer')]").get_attribute('aria-label')
            print(time)
            timelist = time.split(',')
            totaltime = 0
            totaltime1 = 0
            totaltime3 = 0 
            totaltime2 = 0
            mintime = 0                  
            Vindex =0
            
            print("j="+str(j) )
            print(timelist)
            
            for t in timelist:
                #print("t1="+t)
                t= t.strip()
                #print("t2="+t)
                substr=""
                substr = t.split(" ") 
                #print("substr[1] ="+substr[1])
                if (substr[1] == 'hours' or substr[1] == 'hour'):
                    totaltime1 = int(substr[0]) * 3600
                elif(substr[1] == 'minutes'):
                    totaltime2 = int(substr[0]) * 60
                elif substr[1] == 'seconds':
                    totaltime3 = int(substr[0])
                    
                totaltime = totaltime1 + totaltime2 + totaltime3
                
            Mylist.append(totaltime)
            videolink.append(thumbnail_href)
            # print(Mylist)
            mintime=min(Mylist)
            print("mintime="+str(mintime))
            mintime_index = (Mylist.index(mintime))
            print("mintime index:"+str(mintime_index))
            #print(Mylist.index(mintime))             
                
            j =  j + 1
        print(Mylist) 
        # print("video_link="+videolink[mintime_index])   
        ############################################    Download video based on youtube links   #############################################################    
        print()
        print(videolink[mintime_index])
        print()
        youtubeObject = YouTube(videolink[mintime_index], use_oauth=True, allow_oauth_cache=True)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        try:
            youtubeObject.download("static/youtubeVideo/")
        except Exception as e:
            print(e)
            print("An error has occurred")
        speak("Download is completed successfully")


    def defination(searchtext):
        url = 'https://www.dictionary.com/browse/'
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        })
        wikistr = wikipedia.summary(searchtext, sentences=3)
        index = wikistr.find(searchtext)
        if (index != -1):
            wikidef = wikipedia.summary(searchtext, sentences=3)
            return (wikidef)
        else:
            req = requests.get(url + searchtext, headers)
            soup = BeautifulSoup(req.content, 'html.parser')

            mydivs = soup.findAll("div", {"value": "1"})[0]

            for tags in mydivs:
                meaning = tags.text
            return (meaning) 
        
    def sendEmail(to, content):
         server = smtplib.SMTP('smtp.gmail.com', 587)
         server.ehlo()
         server.starttls()
         server.login("aazu21680@gmail.com", 'Shazaan@19')
         server.sendEmail("aazu21680@gmail.com",to, content)
         server.close()
        
    def whatsapp(to, message):

        person = [to]
        string = message
        chrome_driver_binary = "C:\\Program Files\\Google\\Chrome\Application\\chromedriver.exe"
        # Selenium chromedriver path
        driver = webdriver.Chrome(chrome_driver_binary)
        driver.get("https://web.whatsapp.com/")
        #wait = WebDriverWait(driver,10)
        sleep(2)

        for name in person:
            print('IN')
            user = driver.find_element_by_xpath("//span[@title='{}']".format(name))
            user.click()
            print(user)
            for _ in range(10):
                text_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                text_box.send_keys(string)
                sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
                sendbutton.click()


        
    ##########################################################################################################################
    def takeCommand():
        #It takes microphone input from the user and returns string output
        # print(city)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            # print(e)    
            speak("Say that again please...")  
            return "None"
        return query
    
   
    def textToPdf(timeForPage):
        # Exception handling to handle
        # exceptions at the runtime
        try:
            r = sr.Recognizer()

            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=timeForPage)
                
                #listens for the user's input
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("Did you say ",MyText)
                pdf_converter(MyText)
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

    wishMe()        
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query        
        if 'hi' in query or 'hey' in query:
            speak("How are you?")
        
        elif 'on wikipedia' in query or 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            # print(results)
            speak(results)

        elif 'who are you' in query or 'what can you do' in query:
            speak(
                'I am Nexus  your persoanl Buddy. I am programmed to minor tasks like'
                'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather'
                'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!'
            )

        elif "who made you" in query or "who created you" in query or "who discovered you" in query:
            speak("I was built by Gowhar and his Team")
            print("I was built by Gowhar and his Team")

        elif 'fine' in query or 'good' in query:
            speak("That's Great! Tell me what can I help you")
    
        elif 'open youtube' in query:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in query:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'whatsapp' in query:
            try:
                print("J: To whom should i send? ")
                speak("To whom should i send?")
                to = takeCommand()
                print("J: What should i send?")
                speak("What should i send?")
                message = takeCommand()
                speak('You will have to scan for whatsapp web. ')
                print('J: You will have to scan for whatsapp web. ')
                whatsapp(to, message)
                speak("Message has been sent !")
                print("* J: Message has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this message")


        elif 'open gmail' in query:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open chrome' in query:
            codePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
            os.startfile(codePath)  

        elif 'open github' in query:
            os.system("start chrome www.github.com")

        elif 'open geeks for geeks' in query:
            os.system("start chrome www.geeksforgeeks.org") 

        elif 'covid-19 tracker' in query:
            webbrowser.open_new_tab(
                "https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen"
            )
            speak("covid-19 tracker is open now")
            time.sleep(5)

        elif "remember that" in query:
            speak("What should I remember")
            user_ip = takeCommand().lower().replace(' ', '')
            data = takeCommand()
            speak("You said me to remember that" + data)
            print("You said me to remember that " + str(data))
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You told me to remember that" + remember.read())
            print("You told me to remember that " + str(remember))

        elif "shoping" in query or 'shopping' in query:
            websites = ['amazon', 'flipkart', 'myntra', 'limeroad']
            print('\n'.join(websites))
            speak("nice mood sir!, what do you want to open?")
            user_ip = takeCommand().lower().replace(' ', '')

            for website in websites:
                if website in user_ip:
                    webbrowser.open(website + '.com')
            speak("here you are sir")

        elif 'online courses' in query or 'course' in query:
            platforms = [
                'coursera', 'udemy', 'edx', 'skillshare', 'datacamp', 'udacity'
            ]
            speak("Which platform that you prefer : ")
            print("\n".join(platforms))
            courseStatement1 = takeCommand().lower()
            if len(courseStatement1) == 0:
                continue
            if 'coursera' in courseStatement1:
                webbrowser.open_new_tab("https://www.coursera.org")
                speak("Coursera is open now")
                time.sleep(2)
            elif 'udemy' in courseStatement1:
                webbrowser.open_new_tab("https://www.udemy.com")
                speak("udemy is open now")
                time.sleep(2)
            elif 'edx' in courseStatement1:
                webbrowser.open_new_tab("https://www.edx.org/")
                speak("edx is open now")
                time.sleep(2)
            elif 'skillshare' in courseStatement1:
                webbrowser.open_new_tab("https://www.skillshare.com")
                speak("skill share is open now")
                time.sleep(2)
            elif 'datacamp' in courseStatement1:
                webbrowser.open_new_tab("https://www.datacamp.com")
                speak("datacamp is open now")
                time.sleep(2)
            elif 'udacity' in courseStatement1:
                webbrowser.open_new_tab("https://www.udacity.com")
                speak("udacity is open now")
                time.sleep(2)
            else:
                speak("Sorry we couldn't find your search!!!")
            time.sleep(3)
        elif 'jobs' in query or 'job' in query or 'job recommandation' in query or 'work' in query:
            platforms = ['linkedin', 'indeed', 'glassdoor', 'hackerrank', 'naukri','intern shala']
            speak("which platform that you prefer:")
            print('\n'.join(platforms))
            jobStatement1 = takeCommand().lower()
            if (len(jobStatement1) == 0):
                continue
            if 'linkedIn' in jobStatement1:
                webbrowser.open_new_tab("https://www.linkedin.com/jobs")
                speak("LinkedIn is open now")
                time.sleep(2)
            elif 'indeed' in jobStatement1:
                webbrowser.open_new_tab("https://www.indeed.com/jobs")
                speak("Indeed is open now")
                time.sleep(2)
            elif 'glassdoor' in jobStatement1:
                webbrowser.open_new_tab("https://www.glassdoor.com/jobs")
                speak("Glassdoor is open now")
                time.sleep(2)
            elif 'hackerrank' in jobStatement1:
                webbrowser.open_new_tab(
                    "https://www.hackerrank.com/jobs/search")
                speak("HackerRank is open now")
                time.sleep(2)
            elif 'naukri' in jobStatement1:
                webbrowser.open_new_tab("https://www.naukri.com/jobs")
                speak("Naukri is open now")
                time.sleep(2)
            elif 'intern shala' in jobStatement1:
                webbrowser.open_new_tab('internshala.com')
                speak('Intern Shala is open now')
                time.sleep(2)
            else:
                speak("Sorry we couldn't find your search!!!")
            time.sleep(3)
        # elif 'news' in query or 'news headline' in query or 'top news' in query or 'some news' in query:
        #     speak('Here are some headlines from the India today')

        #     newsQuery = query.split("regarding")[1]

        #     cmp_name = newsQuery.replace(" ","%20")

        #     url="https://news.google.com/search?q="+cmp_name+"&hl=en-IN&gl=IN&ceid=IN%3Aen"

        #     html_content = requests.get(url).text

        #     soup = BeautifulSoup(html_content, 'html.parser')
        #     # print(soup.prettify())

        #     table1 = soup.find_all('a', attrs = {'class':'DY5T1d RZIKme'})

        #     headng = []
        #     lnk = []
        #     for i in table1:
        #         a = i["href"]
        #         lnk.append(a)
        #         b = i.text
        #         headng.append(b)

        #     headng = headng[:5]
        #     for i in headng:
        #         print(i)
        #         speak(i)
        
        
        elif 'movie ticket booking' in query or 'movie booking' in query or 'movie ticket' in query:
            speak('Here are some top websites for ticket booking')
            webbrowser.open_new_tab("https://in.bookmyshow.com/")
            speak(" Book my show website is open now")
            time.sleep(2)

        elif 'train ticket booking' in query or 'train booking' in query or 'train ticket' in query or 'train ticket' in query:
            speak('Here are some top websites for tarin ticket booking')
            webbrowser.open_new_tab("https://www.easemytrip.com/railways/")
            speak(" Ease My trip website is open now, have a good journey !")
            time.sleep(2)

        elif 'bus ticket booking' in query or 'bus booking' in query or 'bus ticket' in query:
            speak('Here are some top websites for bus ticket booking')
            webbrowser.open_new_tab("https://www.redbus.in")
            speak(" Red bus website is open now, have a good journey !")
            time.sleep(2)

        elif 'airplane ticket booking' in query or 'airplane booking' in query or 'airplane ticket' in query:
            speak('Here are some top websites for airplane ticket booking')
            webbrowser.open_new_tab("https://www.goindigo.in")
            speak(" Indigo website is open now, have a good journey !")
            time.sleep(2)

        elif "hotel" in query or "hotel booking" in query:
            speak('Opening go ibibo .com')
            webbrowser.open_new_tab('goibibo.com/hotels')
            time.sleep(2)
        elif 'top engineering colleges in india' in query or 'indian engineering college' in query or 'engineering college' in query:
            webbrowser.open_new_tab(
                "https://www.shiksha.com/b-tech/ranking/top-engineering-colleges-in-india/44-2-0-0-0"
            )
            speak("Colleges as per NIRF Ranking are open on Shiksha website!")
            time.sleep(2)

        elif 'top medical colleges in india' in query or 'indian medical college' in query or 'medical college' in query:
            speak('Here are some top Medical Colleges in India')
            webbrowser.open_new_tab(
                "https://medicine.careers360.com/colleges/ranking")
            speak("Colleges as per NIRF rankings are opened!")
            time.sleep(2)

        elif 'top science colleges in india' in query or 'indian science college' in query or 'science college' in query:
            speak('Here are some top website for Science Colleges in India')
            webbrowser.open_new_tab(
                "https://collegedunia.com/science-colleges")
            speak(" College Dunia website is opened!")

        elif 'top law colleges in india' in query or 'indian law college' in query or 'law college' in query:
            speak('Here are some top website for law Colleges in India')
            webbrowser.open_new_tab(
                "https://www.collegedekho.com/law-humanities/law-colleges-in-india/"
            )
            speak(" College Deko website is opened!")
            time.sleep(2)

        elif 'top research colleges in india' in query or 'indian research college' in query or 'research college' in query:
            speak('Here are some top website for Research Colleges in India')
            webbrowser.open_new_tab(
                "https://www.biotecnika.org/2019/09/top-govt-research-institutes-present-in-india-top-10-list/"
            )
            speak("Biotechnika website is opened!")
            time.sleep(2)
        elif "weather" in query:

            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature in kelvin unit is " +
                    str(current_temperature) +
                    "\n humidity in percentage is " + str(current_humidiy) +
                    "\n description  " + str(weather_description))
                speak(" Temperature in kelvin unit = " +
                    str(current_temperature) +
                    "\n humidity (in percentage) = " + str(current_humidiy) +
                    "\n description = " + str(weather_description))
                
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
            print(f"the time is {strTime}")
            speak(f"the time is {strTime}")
        
        elif 'news' in query or 'news headline' in query or 'top news' in query or 'some news' in query:
            speak('Here are some headlines from the India today')

            res = requests.get('https://www.indiatoday.in/top-stories')
            soup = BeautifulSoup(res.text, 'lxml')

            news_box = soup.find('div', {'class': 'B1S3_content__wrap__9mSB6'})
            all_news = news_box.find_all('p')

            for news in all_news:
                print('\n' + news.text)
                speak(news.text)
                print()
                time.sleep(6)

        elif "open stackoverflow" in query:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'search' in query:
            print("hi im in search")
            statement = query.replace("search", "")
            webbrowser.open_new_tab("https://www.google.com/search?q="+statement)
            time.sleep(5)

        elif 'flip the coin' in query or 'toss the coin' in query or 'toss a coin' in query:
            chances = ['Heads', 'Tails']
            coinRes = random.choice(chances)
            picLine = random.randint(1, 3)
            lines = [htLine1(coinRes), htLine2(coinRes), htLine3(coinRes)]
            lines[picLine - 1]()

        elif 'dice' in query:
            num = random.randint(1, 6)
            speak("Your dice number is " + str(num))
        elif 'ip' in query or 'host name and ip' in query:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print("Host-name: " + host_name)
            print("IP address: " + host_ip)
            speak("Your host name is" + host_name + "and ip address is" +
                host_ip)

        elif 'on screen keyboard' in query or 'onscreen keyboard' in query:
            subprocess.run('osk', shell=True)

        elif 'cmd' in query or 'command prompt' in query or 'terminal' in query:
            os.system("start cmd")

        elif 'module in python' in query or 'pip list' in query or 'libraries in python' in query or 'module installed in python' in query:
            subprocess.run('pip list', shell=True)
            speak("Printing all the modules installed in Python")

        # checks internet speed
        elif 'internet speed' in query:
            st = speedtest.Speedtest()
            dl = st.download()
            up = st.upload()
            print('download speed : ' + str(dl) + ' bits/sec')
            print('upload speed : ' + str(up) + ' bits/sec')
            speak('download speed : ' + str(dl) + ' bits/sec')
            speak('upload speed : ' + str(up) + ' bits/sec')

        elif 'play music' in query or "play song" in query:
             speak("Here You go with music")
             #music_dir = "G:\\Song"
             music_dir = "C:\\Users\\user\\Music"
             songs = os.listdir(music_dir)
             print(songs)
             random = os.startfile(os.path.join(music_dir, songs[1]))

        # Hide and unhide files and folder
        elif 'hide folder' in query or 'hide all files' in query:
            os.system('attrib +h /s /d')
            speak("sir, all the files in this folder are now hidden.")

        elif 'unhide files' in query or 'visible to everyone' in query:
            os.system('attrib -h /s /d')
            speak("sir, all the files in this folder are now visible to everyone.")

        elif 'generate qr code' in query:
            img = qrcode.make("https://github.com/Ash515/AshTech-AI_Personal_Voice_Assistant/")
            img.save("repo_qr_code.png")
            subprocess.run('repo_qr_code.png', shell='True')

        elif 'take screenshot' in query or 'capture screen' in query:
            print('Taking screenshot in 3 second')
            speak('Taking screenshot in 3 second')
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save('screenshot.png')
            subprocess.run('screenshot.png', shell='True')

        elif 'dinosaur game' in query or 'chrome dino' in query:
            print("Hey, Chrome dino game will start in 8 sec make sure your internet is off")
            time.sleep(9)
            click('up') 
            
            while True:
                image = ImageGrab.grab().convert('L')  
                data = image.load()
                isCollision(data)

        elif 'volume up' in query or 'increase volume' in query:
            pyautogui.press('volumeup')

        elif 'volume down' in query or 'decrease volume' in query or 'lower the volume' in query:
            pyautogui.press('volumedown') 

        elif 'volume mute' in query or 'turn off the volume' in query or 'mute' in query:
            pyautogui.press('volumemute')

        elif 'jokes' in query or 'joke' in query:
            joke = pyjokes.get_joke('en', 'all')
            print(joke)
            speak(joke)

        elif 'pycharm' in query or 'open pycharm' in query:
            os.startfile('pycharm')
            speak("pycharm is open now")

        elif 'visual studio code' in query or 'open code' in query or 'code' in query or 'visual code' in query:
            os.startfile('code')
            speak('visual studio code is open now')

        elif "notepad" in query:
            speak("Opening Notepad")
            os.system("start Notepad")

        elif "outlook" in query:
            speak("Opening Microsoft Outlook")
            os.system("start outlook")

        elif "word" in query:
            speak("Opening Word")
            os.system("start winword")

        elif "paint" in query:
            speak("Opening Paint")
            os.system("start mspaint")

        elif "excel" in query:
            speak("Opening Excel")
            os.system("start excel")

        elif "start chrome" in query:
            speak("Opening Google Chrome")
            os.system("start chrome")

        elif 'chrome in incognito mode' in query or 'chrome in incognito' in query:
            speak("Opening Google Chrome in Incognito mode")
            os.system('start chrome -incognito')

        elif "power point" in query or "powerpoint" in query or "ppt" in query:
            speak("Opening Notepad")
            os.system("start powerpnt")

        elif "edge" in query:
            speak("Opening Microsoft Edge")
            os.system("start msedge")

        elif "snipping tool" in query:
            speak("Opening Snipping Tool")
            os.system("start snippingtool")

        elif "show deleted files" in query or "Recycle Bin" in query or "Delete files" in query or "search deleted files" in query:
            speak("Opening Recycle Bin")
            os.system("start shell:RecycleBinFolder")

        elif "calculator" in query:
            speak("Opening Calculator")
            os.system("start calc")

        elif "log off" in query or "sign out" in query:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications"
            )
            subprocess.call(["shutdown", "/l"])
        
        # Writing notes
        elif "write a note" in query:
            speak("What should i write, sir")
            print("J: What should i write, sir")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            file.write(note)

        # Showing note
        elif "show the note" in query:
            speak("Showing Notes")
            print("J: Showing Notes")
            file = open("jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))

        elif 'travel' in query or 'cab-booking' in query or 'trip' in query or 'ola' in query or 'uber' in query or 'Cab' in query:
            speak('It seems you are interested in travelling somewhere'
                'Want to Use Cab Sevices or Travel long distanced Trip')
            print("Cab Sevices or Travel long distanced Trip")
            travelask = takeCommand().lower()

            if "travel-long" or "distanced-trip" or "trip" in travelask:
                websites = ['makemytrip', 'booking', 'airbnb', 'Trivago']
                print('\n'.join(websites))
                speak("what do you want to open?")
                user_ip = takeCommand().lower().replace(' ', '')
                for website in websites:
                    if website in user_ip:
                        speak('Opening' + str(website))
                        webbrowser.open(website + '.com')

            elif "cab-services" or "cab" in travelask:
                print("Want to use Ola or Uber")
                speak('Want to use Ola or Uber')
                travelask2 = takeCommand().lower()
                if "ola" in travelask2:
                    webbrowser.open_new_tab("https://www.olacabs.com")
                    speak('Ola website is open now')
                elif "uber" in travelask2:
                    webbrowser.open_new_tab("https://www.uber.com/in/en/")

                    speak('Uber website is open now')

        elif 'search' in query or 'defination' in query:
                speak('I guess you want to search defination'
                    'What do you want to search about sir')
                print("What do you want to search about sir")
                definationask = takeCommand().lower()
                finalmeaning = defination(definationask)
                print(finalmeaning)
                speak(finalmeaning)

                speak('Uber website is open now')

        elif 'download video' in query or 'download' in query or 'video' in query:
            link11=query.split('of')           
            print("link11")
            print(link11)
            link22 = link11[1].split(' ')
            finallink = ('+'.join(link22))
            finallink = finallink[1:]
            print(finallink)
            speak(Download(finallink))

        elif "create a pdf" in query or "create pdf" in query:
            speak("How much pages you have sir?")
            pdf_statement = takeCommand().lower()
            print(pdf_statement)

            if "two pages" in pdf_statement:
               speak("Tell me sir what should I add")
               textToPdf(2)
            elif "one page" in pdf_statement:
                speak("Tell me sir what should I add")
                textToPdf(1)
            else:
                speak("Sorry we couldn't reach you!")

        elif 'ask some questions' in query or 'ask one question' in query or 'ask' in query or 'question' in query:
                   
            speak('I can answer to computational and geographical questions and what question do you want to ask now' )
            question = takeCommand()
            app_id = "YYKYHE-G3VJ67PE8J"
            api_key = "YYKYHE-G3VJ67PE8J"
            client = wolframalpha.Client(api_key)
            try:
              res = client.query(question)
              answer = next(res.results).text
              speak(answer)
              print(answer)
            except:
              speak("I'm sorry, I could not find an answer to your question.")

        elif 'what is my current location' in query or 'what is my location' in query or 'where am I' in query:
            g = geocoder.ip('me')
            print(g.latlng)

            latitudeData = str(g.latlng[0])
            longitudeData = str(g.latlng[1])
            print()
            print("latitudeData, longitudeData")
            print(latitudeData, longitudeData)
            print()

            coordinates =(str(latitudeData), str(longitudeData))

            geoLoc = Nominatim(user_agent="GetLoc")
                    
            # passing the coordinates
            locname = geoLoc.reverse(coordinates)
                
            # printing the address/location name
            print(locname.address)

            Address = locname.address
            speak(Address)

        elif 'email' in query:
                try:
                    speak('What should I say? ')
                    content = takeCommand()
                    speak(content)
                    to = "gowharehmad45@gmail.com"
                    sendEmail(to, content)
                    speak('Email sent!')

                except Exception as e:
                    print(e)
                    speak('Sorry! I am unable to send your mail at this moment!')


        elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess. call('shutdown / p /f')
        
        elif "don't listen" in query or "stop listening" in query:
                speak("for how much time you want to stop Karen from listening commands")
                a = int(takeCommand())
                time.sleep(a)
                print(a)

        elif 'system' in query or 'system details' in query or 'hardware' in query:
            plat_det = platform.uname()
            print('User : ', plat_det.node)
            print('System :', plat_det.system, plat_det.release,
                  plat_det.version)
            print('Machine :', plat_det.machine)
            print('Processor : ', plat_det.processor)
            speak(plat_det.node)
            speak(plat_det.system)
            speak(plat_det.release)
            speak(plat_det.version)
            speak(plat_det.machine)
            speak(plat_det.processor)

        elif 'current user' in query:
            speak('Currently')
            speak(platform.node())
            speak('is logged in and has logged in')
            speak(user_data_dir[platform.node()])
            speak('times till now')
        
        elif "wi-fi and their password" in query or "wi-fi password" in query or  "wi-fi" in query:
            command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
            profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

            wifi_list = list()

            if len(profile_names) != 0:
                for name in profile_names:
                    wifi_profile = dict()
                    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        
                    if re.search("Security key           : Absent", profile_info):
                        continue

                    else:
                        wifi_profile["ssid"] = name
                        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                        password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
                        if password == None:
                            wifi_profile["password"] = None
                        else:
                            wifi_profile["password"] = password[1]
        
                        wifi_list.append(wifi_profile)


            with open('wifi_passwords.txt', 'w+') as fh:
                for x in wifi_list:
                    fh.write(f"Wifi_Name: {x['ssid']}\nPassword: {x['password']}\n")

            with open('wifi_passwords.txt', 'rb') as fh:
                    speak('Successfully stored all the wifi passwords in txt file')
                    subprocess.run('wifi_passwords.txt', shell=True)


        elif "good bye" in query or "ok bye" in query or "stop" in query or "quit" in query or "close" in query:
            print('your personal assistant Nexus is shutting down, Good bye')
            speak('your personal assistant Nexus is shutting down, Good bye')
            break



        #else:
            #wishMe()
            #query = takeCommand().lower() 
            

@app.route('/shop', methods = ['POST', 'GET'])
def shop():
    return render_template("shop.html")







if __name__ == "__main__":
    app.run("0.0.0.0", port=7000)
    # app.run(debug=True)
