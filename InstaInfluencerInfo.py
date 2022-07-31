# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 07:06:34 2022

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


""" For HTML Processing """
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


""" For Insertion Into Table in Database """ 
def InsertToInstaPerson(username,profilename,verification,followerCnt,TotalPostCnt,Reach):
    connection = pymysql.connect(host="localhost",
    user="fauji",
    password="IndianArmy",
    database="flipkartg")
    cursor = connection.cursor()
    string ="INSERT INTO INSTAPSON VALUES" 
    str2="("+'"'+username+'"'+","+'"'+profilename+'"'+","+'"'+verification+'"'+","+followerCnt+","+TotalPostCnt+","+Reach+")"+";"
    #print(str2)
    str_fin = string+str2
    print(str_fin)
    try:
        cursor.execute(str_fin)
        cursor.execute("COMMIT;")
    except:
        print("Data already in DB or some other error")       
    
    cursor.execute("SELECT *FROM INSTAPSON;")
    tb = cursor.fetchall()
    print("The person data : ", tb)
    connection.close()

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


""" Defining a child Instagram Bot Class """
class Instagram_bot(Bot):
    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        print(self.browser.title)
        time.sleep(4)
        emailInput = self.browser.find_element("xpath","//input[@name='username']")
        passwordInput = self.browser.find_element("xpath","//input[@name='password']")

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
    def PressOkay(self ,driver):
        time.sleep(4)
        okay = driver.find_element(By.CLASS_NAME,"sqdOP.yWX7d.y3zKF")
        okay.send_keys(Keys.RETURN)
        time.sleep(2)
    def PressNotNow(self, driver):
        time.sleep(3)
        notnow = driver.find_element(By.CLASS_NAME,"_a9--._a9_1")
        notnow.send_keys(Keys.RETURN)
        time.sleep(1)
    def processProfileI(self ,name):
        profiles = []
        for n in name:
            profile = n.get_attribute("text")
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
    def ProcessCommentI(self , comment1):
        comments  = []
        for c in comment1: 
            comment = c.get_attribute("innerHTML")
            comment = strip_tags(comment)
            comm_split = comment.split()
            num_words = len(comm_split)
            if(num_words >= 3): # this gets rid of more , but have to think what happens when there is no comment 
                comment = comm_split[-2]
                comments.append(comment)
        return comments
    def ProcessLikeI(self , like1):
        likes  = []
        for lik in like1:
            like = lik.get_attribute("text")
            substring = "likes"
            if substring in like:
                like_con = like.split()
                likes.append(like_con[0])
        return likes
    def ReachFollowerPage(self,user_name):
        #Moves to the mentioned URL
        URL_p1 = "https://www.instagram.com/"
        end_s ="/"
        URL = URL_p1+user_name+end_s

        self.browser.get(URL)
        #Induce delay to avoid suspicion
        time.sleep(10)
    def isVerified(self,engine):
        try:
            Element_obtained = trendBot.browser.find_element(By.CLASS_NAME,
            "_ab8w._ab94._ab99._ab9f._ab9m._ab9p._abb0._abcm")
            BlueTick = Element_obtained.get_attribute("innerHTML")
            Tick = strip_tags(BlueTick)
            ver = "Verified"
            if ver in Tick:
                print(Tick)
                return True   
            else:
                print("Not Verified")
                return False
        except:
            print("Element Not found")
            return False
    def findTotalPosts(self ,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "_aacl._aacp._aacu._aacx._aad6._aade")
            PostCount = Element_obtained.get_attribute("innerHTML")
            Post_c = strip_tags(PostCount)
            Post_f = Post_c.split()
            PCount = Post_f[0]
            thousands = "K"
            comma = ","
            millions = "M"
            if thousands in PCount:
                mid_c =PCount.replace(thousands,"000")
                tw_Cnt = mid_c.replace(".","")
                print(tw_Cnt)
                return(tw_Cnt)
            elif millions in PCount:
                mid_c =PCount.replace(millions,"000000")
                tw_Cnt = mid_c.replace(".","")
                print(tw_Cnt)
                return(tw_Cnt)
            elif comma in PCount:
                tw_Cnt= PCount.replace(comma,"")
                print(tw_Cnt)
                return tw_Cnt
            else:
                print(PCount)
                return (PCount)
            print(PCount)
        except:
            print("Element Not found")
            return 0
    def findTotalFollowers(self,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "_aa_7")
            PostCount = Element_obtained.get_attribute("innerHTML")
            p = PostCount.split()
            pi = p[26]
            piF= pi.split("=")
            piFo= piF[1]
            piFol = piFo.split(">")
            piFoll = piFol[0]
            piFollo = piFoll.split('"')
            piFollow = piFollo[1]
            comma =","
            if comma in piFollow:
                piFollower=piFollow.replace(comma,"")
            print(piFollower)
            return piFollower
        except:
            print("Element Not found")
            return 0
    def findProfileName(self,engine):
        try:
            Element_obtained = engine.find_element(By.CLASS_NAME,
            "_aa_c")
            Unam = Element_obtained.get_attribute("innerHTML")
            Usern = Unam.split(">")
            Profn = Usern[1]
            Profnam = Profn.split("<")
            Profname = Profnam[0]
            print(Profname)
            return Profname
        except:
            print("Element Not found")
            return 0



""" List of All the influencers whose data we want to obtain """

followers =["bridesofsabyasachi","afashionistasdiaries","manishmalhotraworld","VogueSpain",
            "vogueindia","eattweetblog","anitadongre","harpersbazaarus","elleusa",
            "sabyasachiofficial","vogueitalia","voguefrance","britishvogue",
            "voguerunway","voguemagazine","thevofashion"]


""" Starting selenium """
trendBot = Instagram_bot("trendfinder2022@gmail.com","hackgrid2022")
wait = WebDriverWait(trendBot.browser, 10)


"""Lists for storing information """
Verified = []
TotalPostCount = []
FollowerCounts = []
ProfileNames = []
UserNames = []
HashtagMentions = []


"""Obtaining all the neccesary information from all the influencers of interest"""
for follower in followers:
    trendBot.ReachFollowerPage(follower)
    value =trendBot.isVerified(trendBot.browser)
    Verified.append(value)
    PostCount =trendBot.findTotalPosts(trendBot.browser)
    TotalPostCount.append(PostCount)
    followercount =trendBot.findTotalFollowers(trendBot.browser)
    FollowerCounts.append(followercount)
    pname =trendBot.findProfileName(trendBot.browser)
    ProfileNames.append(pname)
    UserNames.append(follower)
    print(follower)
    try:
        trendBot.ReachHashtagPage(follower)
        hashtag_reach = trendBot.browser.find_element(
            By.CLASS_NAME,
            "_aacl._aacp._aacu._aacx._aad6._aade")
        reach =trendBot.process_HashTag_Reach(hashtag_reach)
        HashtagMentions.append(reach)
    except:
        print("Could not reach the page")
        reach ="0"

""" Inserting the obtained valued to the InstagPersons table """

length = len(followers)
for i in range(0,length):
    verig = Verified[i]
    if (verig == True):
        verig = "Yes"
    else:
        verig = "No"
    InsertToInstaPerson(UserNames[i],ProfileNames[i],verig, FollowerCounts[i],TotalPostCount[i],HashtagMentions[i])
