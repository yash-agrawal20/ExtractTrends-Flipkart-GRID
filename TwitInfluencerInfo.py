# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 07:31:21 2022

@author: Anirudh Sathish
"""

""" Importing the neccesary libraries """

#Selenium for web automation
#Selenium Version: 4.2.0
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

import time
from datetime import datetime
import pandas as pd
from dateutil import tz

from io import StringIO
from html.parser import HTMLParser

import pymysql

""" Processing HTML """

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

""" Inserting the information into the TWIGPERSON TABLE in the database """

def InsertToPerson(username,profilename,verification,followerCnt,location,bio):
    connection = pymysql.connect(host="localhost",
    user="fauji",
    password="IndianArmy",
    database="flipkartg")
    cursor = connection.cursor()
    string ="INSERT INTO TWIPERSON VALUES" 
    str2="("+'"'+username+'"'+","+'"'+profilename+'"'+","+'"'+verification+'"'+","+'"'+followerCnt+'"'+","+'"'+location+'"'+","+'"'+bio+'"'+")"+";"

    str_fin = string+str2
    try:
        cursor.execute(str_fin)
        cursor.execute("COMMIT;")
    except:
        print("Already exists in database or some other error")        
    
    cursor.execute("SELECT *FROM TWIPERSON;")
    tb = cursor.fetchall()
    print("The person data : ", tb)
    connection.close()


""" Introdcing Bot Classes """

#Defining a parent bot class
class Bot():
    def __init__(self , email, password):
        path ="C:/Users/aniru/chromedriver.exe"        
        self.browser = webdriver.Chrome(path)
        self.email = email
        self.password = password
    #Wait to get all elements of the page ready
    def Presence_Located(self ,pause , clsName):
        val = pause.until(EC.presence_of_all_elements_located((
        By.CLASS_NAME ,clsName)))
        return val
    def Process_Image_Download(self ,ImgUrl):
        imageUrls =[]
        for i in ImgUrl:
            imageUrl = i.get_attribute("src")
            imageUrls.append(imageUrl)
            response = requests.get(imageUrl)
            file = open("C://Users//aniru//FlipkartGrid//Images//img"+str(time.time())+".jpeg", "wb")
            file.write(response.content)
            file.close()
        return imageUrls
    def dealProfile(self ,profiles):
        new_profile = []
        for profile in profiles:
            profile = profile.replace("See All","") # Other Wise See all will be considered as profilename
            if profile != "":
                new_profile.append(profile)
        return new_profile
    def dealDates(self ,datetimelist):
        new_date = []
        for date in datetimelist:
            date = date.replace("T"," ")[:-5]
            utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('Asia/Kolkata')
            utc = utc.replace(tzinfo=from_zone)
            # Convert time zone
            central = utc.astimezone(to_zone)
            new_date.append(central)
        return new_date
    def dealRest(self , values):
        new_values = []
        for v in values:
            new_values.append(v)
        return new_values 


#Introducing an inherited Twitter bot class

class twitterBot(Bot):
    def signIn(self):
        #Moves to the mentioned URL
        self.browser.get('https://twitter.com/i/flow/login')
        print(self.browser.title)
        #Induce delay to avoid suspicion
        time.sleep(10)

        #Enter the email input and press enter , so as to move to next step 
        emailInput = self.browser.find_element(By.NAME,"text")
        emailInput.click()
        emailInput.send_keys(self.email)
        emailInput.send_keys(Keys.RETURN)
        #Induce delay
        time.sleep(10)

        #Enter the password input and press enter , to finally enter the page
        passwordInput = self.browser.find_element(By.NAME,"password")
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.RETURN)
        time.sleep(2) 
    def processProfileI(self ,name):
        profiles = []
        for n in name:
            profile = n.get_attribute("text")
            substring = "@"
            if substring not in profile:
                profiles.append(profile)
        return profiles
    def processDescriptionI(self , desc):
        descriptions = []
        for d in desc:
            description = d.get_attribute("innerHTML")
            description = strip_tags(description)
            descriptions.append(description)
        return descriptions
    def processDateI(self , dateList):
        datetimelist = []
        for d in dateList:
            date = d.get_attribute("innerHTML")
            dat = date.split()
            date = dat[1]
            dat_p = date.split('=')
            date = dat_p[1]
            dat = date.split('>')
            date = dat[0]
            make_list = date.split('"')
            date = make_list[1]
            datetimelist.append(date)
        return datetimelist
    def ProcessReactionI(self , Reactions):
        comments  = []
        retweets = []
        likes = []
        multiple = 0
        for r in Reactions:
            reaction = r.get_attribute("innerHTML")
            numberReaction = strip_tags(reaction)
            if(numberReaction != ""):
                thousands = "K"
                if thousands in numberReaction:
                    num = numberReaction.replace(thousands,"000")
                    numberReaction = num.replace(".",",")
                comma =","
                if comma in numberReaction:
                    change = numberReaction.replace(comma,"")
                    numberReaction= change
            else:
                numberReaction = 0 
            if(multiple%3 == 0):
                comments.append(numberReaction)
            elif(multiple%3 == 1):
                retweets.append(numberReaction)
            else:
                likes.append(numberReaction)
            multiple +=1
        return comments , retweets , likes
    def ReachFollowerPage(self,user_name):
        #Moves to the mentioned URL
        URL_p1 = "https://twitter.com/"
        URL = URL_p1+user_name

        self.browser.get(URL)
        #Induce delay to avoid suspicion
        time.sleep(10)
    def isVerified(self ,engine):
        try:
            Element_obtained = trendBot.browser.find_element(By.CLASS_NAME,
            "css-901oao.css-16my406.r-xoduu5.r-18u37iz.r-1q142lx.r-poiln3.r-bcqeeo.r-qvutc0")
            BlueTick = Element_obtained.get_attribute("innerHTML")
            substring ="svg"
            if substring in BlueTick:
                tick = 1
                print("Verified_Account")
                return True 
            else:
                print("Not Verified")
                return False
        except:
            print("Element Not found")
            return False
    def findTotalTweets(self ,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "css-901oao.css-bfa6kz.r-14j79pv.r-37j5jr.r-n6v787.r-16dba41.r-1cwl3u0.r-bcqeeo.r-qvutc0")
            TweetCount = Element_obtained.get_attribute("innerHTML")
            substring ="Tweets"
            if substring in TweetCount:
                Twee = TweetCount.split()
                TCount= Twee[0]
                thousands = "K"
                millions = "M"
                if thousands in TCount:
                    mid_c =TCount.replace(thousands,"000")
                    tw_Cnt = mid_c.replace(".","")
                    print(tw_Cnt)
                    return(tw_Cnt)
                elif millions in TCount:
                    mid_c =TCount.replace(millions,"000000")
                    tw_Cnt = mid_c.replace(".","")
                    print(tw_Cnt)
                    return(tw_Cnt)
                else:
                    print(TCount)
                    return (TCount)
            else:
                print("Not")
                return 0
        except:
            print("Element Not found")
            return 0
    def findLocation(self,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "css-901oao.r-18jsvk2.r-37j5jr.r-a023e6.r-16dba41.r-56xrmm.r-bcqeeo.r-qvutc0")
            Location = Element_obtained.get_attribute("innerHTML")
            Loc_t = Location.split('<span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"><span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">')
            Loc_t2 = Loc_t[1].split('</span></span></span>')
            Location = Loc_t2[0]
            print(Location)
            return Location
        except:
            statement = "No Location found"
            print(statement)
            return statement
    def findFollowerCount(self ,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "css-1dbjc4n.r-13awgt0.r-18u37iz.r-1w6e6rj")
            FollowerCount = Element_obtained.get_attribute("innerHTML")
            flwr = FollowerCount
            flwr_t = flwr.split('<span class="css-901oao css-16my406 r-18jsvk2 r-poiln3 r-1b43r93 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"><span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">')
            flwr_t2 = flwr_t[2].split('</span></span>')
            FollowerCount = flwr_t2[0]
            thousands = "K"
            comma = ","
            millions = "M"
            if thousands in FollowerCount:
                mid_c =FollowerCount.replace(thousands,"000")
                tw_Cnt = mid_c.replace(".","")
                print(tw_Cnt)
                return(tw_Cnt)
            elif millions in FollowerCount:
                mid_c =FollowerCount.replace(millions,"000000")
                tw_Cnt = mid_c.replace(".","")
                print(tw_Cnt)
                return(tw_Cnt)
            elif comma in FollowerCount:
                tw_Cnt= FollowerCount.replace(comma,"")
                print(tw_Cnt)
                return tw_Cnt
            else:
                print(FollowerCount)
                return (FollowerCount)
        except:
            statement = "Could not locate follower count"
            print(statement)
            return 0
    def findBio(self,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "css-901oao.r-18jsvk2.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0")
            Bio_HTML = Element_obtained.get_attribute("innerHTML")
            Bio_t = Bio_HTML.split('<span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">')
            Bio_H = Bio_t[1].split('</span>')
            Bio = Bio_H[0]
            if len(Bio) <= 1:
                statement = "Account has no Bio"
                print(statement)
                return statement
            print(Bio)
            return Bio
        except:
                statement = "Account has no Bio"
                print(statement)
                return statement
    def findProfileName(self,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "css-1dbjc4n.r-1wbh5a2.r-dnmrzs.r-1ny4l3l")
            Prof_HTML = Element_obtained.get_attribute("innerHTML")
            ProfileName = strip_tags(Prof_HTML)
            print(ProfileName)
            return ProfileName
        except:
            statement = "Failed to Find Bio"
            print(statement)
            return statement
    
    

"""Setting up a followers list from whom u want to obtain data """

followers =["voguesingapore","voguebrasil","vogueturkiye","VogueSpain","anirudhsathish_"]


""" Starting up Selenium """
trendBot = twitterBot("trendfinder2022@gmail.com","hackgrid2022")
wait = WebDriverWait(trendBot.browser, 10)


"""Setting up lists to store data """
Verified = []
TotalTweetCount = []
Locations = []
FollowerCounts = []
Bios =[]
ProfileNames = []
UserNames = []

""" Obtaining the required information from all followers """

for follower in followers:
    trendBot.ReachFollowerPage(follower)
    value =trendBot.isVerified(trendBot.browser)
    Verified.append(value)
    tweetCount = trendBot.findTotalTweets(trendBot.browser)
    TotalTweetCount.append(tweetCount)
    location = trendBot.findLocation(trendBot.browser)
    Locations.append(location)
    FollowerCount = trendBot.findFollowerCount(trendBot.browser)
    FollowerCounts.append(FollowerCount)
    Bio = trendBot.findBio(trendBot.browser)
    Bios.append(Bio)
    UserNames.append(follower)
    ProfileName = trendBot.findProfileName(trendBot.browser)
    ProfileNames.append(ProfileName)

"""Inserting obtained info , to the table in the database """
length = len(followers)
for i in range(0,length):
    verig = Verified[i]
    if (verig == True):
        verig = "Yes"
    else:
        verig = "No"
    InsertToPerson(UserNames[i],ProfileNames[i],verig, FollowerCounts[i],Locations[i],Bios[i])