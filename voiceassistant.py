
import speech_recognition as sr #MUST INSTALL ALL THE LIBRARIES
from gtts import gTTS
import wikipedia as wk
import wolframalpha
import pyttsx3
import pyjokes
import datetime
from datetime import datetime
import time
import playsound
import weathercom
import os
import json
import  requests
import webbrowser
import urllib.request
import urllib.parse
import re
import pyautogui
from bs4 import BeautifulSoup
import subprocess
import nltk    
from nltk.tokenize import word_tokenize
nltk.download('punkt')  

r = sr.Recognizer()
def voice_command_processor(ask=False): #recognize voice
    with sr.Microphone() as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source, phrase_time_limit=3)   #you may set a different time limit

        text = ''
        text = text.lower()
        try:
            text=r.recognize_google(audio)  #use google tts
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError as e:
            print("Service is down")

        return text.lower()


def voice_command_processor_jarvis(ask=False):  #jarvis "ai" 
    with sr.Microphone() as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source, phrase_time_limit=6)   #bigger time limit for jarvis

        text = ''
        text = text.lower()
        try:
            text=r.recognize_google(audio)
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError as e:
            print("Service is down")

        return text.lower()


def audio_playback(text):       #create a temporary mp3 file and play the answer
    filename = "test.mp3"
    tts = gTTS(text=text, lang='en-us')
    tts.save(filename)
    playsound.playsound(filename, block=False)
    os.remove(filename)
   




def execute_voice_command(text):
    


        if 'wait' in text:
            audio_playback("Ok, I'll wait")
            
            while text != 'wake up':    #until it hears "wake up" again, stays in this loop
                print("Waiting")
                text = voice_command_processor()
                
        if 'wake up' in text:
               audio_playback("Hello again!")
               print("Hello again!")      
    #AI-----------------------------------
        words = word_tokenize(text)
        if 'jarvis' in words:
            audio_playback("What do you want to ask?")
            query = voice_command_processor_jarvis()
            client = wolframalpha.Client('###########')  #ADD THE API KEY
            print(query)
            try:
                res = client.query(query)
                answer = next(res.results).text
                audio_playback(answer)
                print(answer)
            except:
                try:
                    answer = wk.summary(query, sentences=2)     #says the first 2 sentences of the wikipedia article
                    audio_playback(answer)
                    print(answer)
                except:
                    audio_playback("Sorry, I don't know the answer.")
                    print("Sorry, I don't know the answer.")
            



        
    # SCRIPT WEATHER -----------------------------------------------


        if "weather" in text:
             api_key = "############"   #ADD THE API KEY for openweathermap
             base_url = "https://api.openweathermap.org/data/2.5/weather?"
             audio_playback("Tell me the city name")
             city_name = voice_command_processor()
             complete_url = base_url + "appid=" + api_key + "&q=" + city_name
             response = requests.get(complete_url)
             x = response.json()
             if x["cod"] != "404":
                 y = x["main"]
                 current_temperature = y["temp"]
                 current_humidiy = y["humidity"]
                 z = x["weather"]
                 temp_cel = current_temperature - 273.15
                 weather_description = z[0]["description"]
                 audio_playback(" Temperature in " + city_name + "  is " + str(temp_cel)[:2] + "degrees , humidity is " + str(current_humidiy) + "% and it's " + str(weather_description))
                 print(" Temperature in  " + city_name + " is = " + str(temp_cel)[:2] +"\n The humidity (in percentage) = " + str(current_humidiy) + "\n Description = " + str(weather_description))

#CLOSE BROWSER
        if 'stop' in text:
            os.system("pkill "+ "chromium") #change "chromium" to your browser if needed

 #PLAY MUSIC YOUTUBE
        if 'play' in text:
            text = text[5:]
            audio_playback("Searching for " + text)     

            if text != '':
                url = f"https://www.youtube.com/results?search_query={text}"    #this opens youtube search results
                webbrowser.get().open(url)
                time.sleep(30)
                audio_playback("Choose the song with a number, starting from 0") #here you choose the song that shows up on the screen
                time.sleep(1)
                song = voice_command_processor()
                print(song)
                while not song.isnumeric():
                    audio_playback("I'm sorry, I couldn't recognize the number, can you say it again?")
                    time.sleep(1)
                    song = voice_command_processor()
                    
                x = int(song)
                if x == 0:
                    print(x)
                    pyautogui.press("enter", presses=3)     #just to open the song without the mouse
                else:
                    x = int(song) + 4
                    print(x)
                    pyautogui.press("tab", presses=x)
                    pyautogui.press("enter", presses=1)
               
                    


   
#TELL THE TIME
        if 'time' in text:

            hora = datetime.now().strftime('%I:%M %p')
            print('Current time is ' + hora)
            audio_playback('Current time is ' + hora)

#TELL DATE
        if 'day' in text:
                from datetime import date
                today = date.today()
                today = datetime.now().strftime("%d %B, %Y")
                print("Today is ", today)
                audio_playback("Today is " + today)

#TELL A JOKE
        if 'joke' in text:
            text = pyjokes.get_joke()
            audio_playback(text)
            print(text)

#WIKIPEDIA SEARCH

        #-maybe add a function to cancell ---------------------------------

        if "search" in text:        #should say "search" + "the thing you want to search"
            audio_playback("Let me " + text + ", hold on a second")
            try:
                app_id = "#############"    #ADD THE API KEY
                client = wolframalpha.Client(app_id)
                res = client.text(text)
                answer = next(res.results).text
                print(answer)
                audio_playback("Your answer is " + answer)


            except:

                text = text.split(' ')
                text = " ".join(text[0:])
                audio_playback(wk.summary(text, sentences=2))

                print(wk.summary(text, sentences=2))



        
            #this function runs the scripts to turn on/off the led ON THE GPIO PORT 18 (raspberry pi)
        if 'lights on' in text:
            audio_playback("Turning the lights on")
            python_file_path = '-------------------/turnonled.py' #ADD THE CORRECT PATH
            command = ['sudo', '-S', '/usr/bin/python3.9', python_file_path]
            password = '######\n'                           #ADD YOUR SUDO PASSWORD
            p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = p.communicate(password)
            print(output)
            print(error)
        if 'lights off'  in text:
            audio_playback("Turning the lights off")
            python_file_path = '----------------------/turnoffled.py' #ADD THE CORRECT PATH
            command = ['sudo', '-S', '/usr/bin/python3.9', python_file_path]
            password = '######\n'   #ADD YOUR SUDO PASSWORD
            p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = p.communicate(password)
            print(output)
            print(error)
           
             
            
            
        
#HARD CODED ANSWERS


        if 'virus' in text:
            audio_playback("It depends, who's asking?")

        if "where" in text:
            audio_playback("I'm stuck inside this Raspberry and this cardboard helmet")

        if "go on a date" in text:
            audio_playback("I'm sorry, I'm in a serious relationship with... ahm... uhh... nevermind, I'm busy today")

        if "hello" in text:
            audio_playback("Hello master, how are you doing today?")

        if "good" in text:
            audio_playback("That's nice to hear!")

        if "sad" in text:
            audio_playback("Oh I'm really sorry to hear that. Unfortunately I can't really help you, I don't know what's that")

        if "nervous" in text:
            audio_playback("You're fine! You got this")

        if "how are you" in text:
            audio_playback("I'm ready to help you!")

        if "and you" in text:
              audio_playback("I'm ready to help you!")

        if "what are you" in text:
              audio_playback("I am Jarvis, your Virtual Voice assistant")

        if "exit" in text:
          audio_playback("Goodbye!")
          exit()
          


print("Starting")
audio_playback("Hello")
while True:
    command = voice_command_processor()
    print(command)
    execute_voice_command(command)
    


