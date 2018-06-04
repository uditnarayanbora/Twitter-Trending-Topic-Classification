import pandas as pd
import tweepy
import re
from stop_words import get_stop_words
from tweepy import OAuthHandler
from textblob import TextBlob
from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import urllib2
from collections import Counter
import matplotlib.pyplot as plt

class classifications():
    def __init__(self,root):
        self.topFrame=Frame(root,width=1090,height=1000)
        self.topFrame.pack()
        self.botFrame=Frame(root)
        self.botFrame.pack(side=BOTTOM)
        self.init_start()
    def init_start(self):
        #self.photo=PhotoImage(file="Hashtags.ppm")
        #self.lab=Label(self.topFrame,image=self.photo)
        #self.lab.pack(fill=X)
        #self.image = Image.open('img.jpeg')
        #self.image.resize((1080, 1000), Image.ANTIALIAS)
        #self.photo = ImageTk.PhotoImage(self.image)
        #self.photo_panel = Label(root, image=self.photo)
        #self.photo_panel.config(image=self.photo)
        #self.photo_panel.place(x=0,y=0)
        #self.images = Image.open('sa.jpeg')
        #self.images.resize((1080, 1000), Image.ANTIALIAS)
        #self.photos = ImageTk.PhotoImage(self.images)
        #self.photo_panels = Label(self.topFrame, image=self.photos)
        #self.photo_panels.config(image=self.photos)
        #self.photo_panels.pack()
        self.labelt=Label(self.topFrame,text="TWITTER TRENDING TOPIC CLASSIFICATION",bg="blue",fg="black")
        self.labelt.config(height=4,width=100)
        self.labelt.config(font="Verdana 30 bold")
        self.labelt.pack(fill=X)
        self.label1=Label(self.botFrame,text="Enter the Trending Topics : ",fg="black")
        self.label1.config(font="Times 20 bold")
        self.label1.config(height=15,width=25)
        self.entry1=Entry(self.botFrame,textvariable="topic",bd=5)
        self.label1.grid(row=4)
        self.entry1.grid(row=4,column=1)
        self.classify = Button(self.botFrame, text="Classify",height=3,width=8,font="Times 15 bold",bg="teal",command=self.getValue)
        self.classify.grid(row=4,column=5,sticky=W,padx=25,pady=3) 
    def clean(self,tweet):
            s_words = get_stop_words('en')
            tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
            words = tweet.split(" ")
            for word in words:
                    if word.lower() in s_words:
                            del words[words.index(word)]
            return ' '.join(words)

    def fetchCat(self,url):
        lines = []
        try:
            response = urllib2.urlopen("https://en.wikipedia.org" + url)
            lines = response.read().splitlines(True)
            response.close()
            for line in lines:
                if line.strip().startswith('<div id="catlinks"'):
                    wcat = line.find('/wiki/Category:')
                    wqot =  line.find('"',wcat)
                    return line[wcat:wqot]
        except:
            pass

    def findCategory(self,url):
            catArray = []
            fetCat = self.fetchCat(url)
            catArray.append(fetCat)
            category = ""
            parentCategoryArray = ["Health","Politic","Technology","Sports","Entertainment","Education","Science"]
            try:
                    for i in range(15):
                            for pcat in parentCategoryArray:
                                    if re.search(pcat,fetCat,re.IGNORECASE):
                                            category = pcat
                                            return category
                            fetCat = fetchCat(fetCat)
                    if category == "":
                            return "Others"
            except : 
                    return "Others"

    def plotGraph(self,d):
            plt.bar(range(len(d)), d.values(), align="center")
            plt.xticks(range(len(d)),list(d.keys()))
            plt.show()


    def getValue(self):
        top=self.entry1.get()
        #print top
        if " " in top :
            tkMessageBox.showerror("Error","Trending Topic should not contain space")
        elif "#" in top:
            tkMessageBox.showerror("Error","Topic should not contain #")
            
        else:    
            CONSUMER_KEY='wj03pqAivE4af5s4YccaFsUVL'
            CONSUMER_SECRET='0AhhU1QPzGXTDS0BKjIZFwbLsrlacBlMy7nDcTvt1TiZMCjU44'
            ACCESS_TOKEN='921322828288344064-NCZm2oFxt1Nq3WgaborC5l2Vqj63lMH'
            ACCESS_TOKEN_SECRET='jG9DENbSqdHKBjpIeAPzXo5DNETcEPsz4ZESRkdY6BDUd'

            try:
                auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
                auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
                api = tweepy.API(auth)
            except:
                print "Error in connecting!"

            try:
                    query = "#"+top
                    count = 50
                    f_tweets = []
                    for tweet in tweepy.Cursor(api.search,q=query + '-filter:retweets',since='2018-04-12',until='2018-06-04', lang='en').items(count):
                            f_tweets.append(tweet.text)
            except tweepy.TweepError as te:
                print te
            c_tweets = []
           
            if len(f_tweets)== 0 :
                tkMessageBox.showerror('Error','No such Trending Topic exist')
            else:
                #print "Tweets Extracted from Twitter :"
                #print f_tweets
                for tweet in f_tweets:
                        c_tweets.append(self.clean(tweet))
                #print "Pre-processed Tweets :"
                #print c_tweets
                np = []

                for tweet in c_tweets:
                        blob = TextBlob(tweet)
                        np.append(blob.noun_phrases)

                ngrams = []
                for phrases in np:
                        for phrase in phrases:
                                blob = TextBlob(phrase)
                                n3 = blob.ngrams(n=3)
                                n2 = blob.ngrams(n=2)
                                n1 = blob.ngrams(n=1)
                                for i in n3:
                                        ngrams.append(i)
                                for i in n2:
                                        ngrams.append(i)
                                for i in n1:
                                        ngrams.append(i)


                final = []

                for i in ngrams:
                        final.append("_".join(i))

                significant_phrases = dict(Counter(final).most_common(50))
                #print "Extracted keywords"
                #print significant_phrases

                classification = {}

                sport=open('sports.txt')
                tech=open('technology.txt')
                ent=open('entertainment.txt')
                pol=open('politics.txt')
                heal=open('health.txt')
                sci=open('science.txt')
                edu=open('education.txt')
                sport1=0
                tech1=0
                ent1=0
                poll=0
                heal1=0
                sci1=0
                edu1=0

                dict1=set(line.strip() for line in sport)
                dict2=set(line.strip() for line in tech)
                dict3=set(line.strip() for line in ent)
                dict4=set(line.strip() for line in pol)
                dict5=set(line.strip() for line in heal)
                dict6=set(line.strip() for line in sci)
                dict7=set(line.strip() for line in edu)

                for word in significant_phrases:
                        if word in dict1:
                                #print word
                                sport1=sport1+ significant_phrases[word]

                #print sport1

                for word in significant_phrases:
                        if word in dict2:
                                print word
                                tech1=tech1+ significant_phrases[word]
                #print tech1

                for word in significant_phrases:
                        if word in dict3:
                                #print word
                                ent1=ent1+ significant_phrases[word]

                #print ent1

                for word in significant_phrases:
                        if word in dict4:
                                #print word
                                poll=poll+ significant_phrases[word]

                #print poll

                for word in significant_phrases:
                        if word in dict5:
                                #print word
                                heal1=heal1+ significant_phrases[word]

                #print heal1

                for word in significant_phrases:
                        if word in dict6:
                                #print word
                                sci1=sci1+ significant_phrases[word]

                #print sci1

                for word in significant_phrases:
                        if word in dict7:
                                print word
                                edu1=edu1+ significant_phrases[word]

                #print sci1



                total=ent1+poll+tech1+sport1+heal1+sci1+edu1
                print "Dictionary scores :"
                r_sport=sport1/float(total)
                print "Sport : "
                print r_sport
                r_tech=tech1/float(total)
                print "Technology : "
                print r_tech
                r_ent=ent1/float(total)
                print "Entertainment : "
                print r_ent
                r_poll=poll/float(total)
                print "Politic : "
                print r_poll
                r_heal=heal1/float(total)
                print "Health : "
                print r_heal
                r_sci=sci1/float(total)
                print "Science : "
                print r_sci
                r_edu=edu1/float(total)
                print "Education : "
                print r_edu

                classification={}
                classification['Sports']=r_sport
                classification['Technology']=r_tech
                classification['Entertainment']=r_ent
                classification['Politic']=r_poll
                classification['Health']=r_heal
                classification['Science']=r_sci
                classification['Education']=r_edu

                significant_phrase = dict(Counter(final).most_common(5))
                #print significant_phrase


                classify = {}
                for key in significant_phrase.keys():
                        url = "https://en.wikipedia.org/wiki/" + key
                        statusCode = 0
                        try:
                                statusCode = urllib2.urlopen(url).getcode()
                        except:
                                pass
                        if statusCode == 200:
                                #print key
                                category = self.findCategory("/wiki/" + key)
                                if category in classify: 
                                        classify[category] += significant_phrase[key]
                                else:
                                        classify[category] = significant_phrase[key]
                        else:
                                pass
                s = sum(classify.values())
                for key in classify.keys():
                        classify[key] = classify[key]/float(s)
                        #print classify[key]
                for key in classify.keys():
                        if key in classification.keys() :
                                classify[key]=classify[key]+classification[key]
                        if key=="Others":
                                del classify["Others"]
                for key in classification.keys():
                        if key  not in classify.keys():
                                classify[key]=classification[key]
                m=0
                for key in classify.keys():
                        if classify[key]>m :
                                m=classify[key]
                                k=key
                print k
                self.label1i=Label(self.botFrame,text="The category of #",fg="black")
                self.label1i.config(font="Times 20 bold")
                self.label1i.config(height=15,width=25)
                self.label1i.grid(row=4)
                self.label1i=Label(self.botFrame,text="is "+k,fg="black")
                self.label1i.config(font="Times 20 bold")
                self.label1i.config(height=15,width=25)
                self.label1i.grid(row=4,column=2)
                self.classify = Button(self.botFrame, text="Quit",height=3,width=8,font="Times 15 bold",bg="teal",command=self.botFrame.quit)
                self.classify.grid(row=4,column=5,sticky=W,padx=25,pady=3) 
                self.plotGraph(classify)
root=Tk()

b=classifications(root)
root.mainloop()

