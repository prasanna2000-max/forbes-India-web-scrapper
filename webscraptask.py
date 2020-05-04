from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup
import itertools
import time 
import requests
import shutil
import sqlite3
import os

#opening the browser
browser = webdriver.Chrome()
#navigates you to the 100 celebrites in india website  page.
browser.get('https://www.forbesindia.com/lists/2019-celebrity-100/1819/all')

time.sleep(10)
#waits for the browser to open all the dynamic contents
wait = WebDriverWait(browser, 1000).until(EC.visibility_of_element_located((By.ID,"list_rank")))
print("after wait")
#get html page version of the following webpage	
html = browser.page_source
#delcaring a variable for the name of the celebrity to be saved
each_text=[]
#getting into the beautifulsoup
filesoup = BeautifulSoup(html, "html.parser")
#finding the names of the celebrity	
for each in filesoup.find_all('div',{"class":"name"}):
	string1=(each.text.replace('name',''))
	each_text.append(string1[:-1])
#variable for getting the links of the img		
img=[]
#finding the div class with class rounded of the celebrity pages
for each in filesoup.find_all('img',{"class":"rounded"}):
	
	img.append(each.get('src'))
j=1
filenames=[]
for im in img:
	try:
		ext=im[im.rindex('.'):]
		filen=str(j)+ext
		filenames.append(filen)
		res=requests.get(im,stream=True)
		with open(filen,"wb") as file:
			shutil.copyfileobj(res.raw,file)
	except Exception as e:
		print(e)
	j=j+1



#similarly for the ranking,earnings of the celebrites
rank=[]
about=[]
earning=[]

#for rank 
for each in filesoup.find_all('div',{"class":"rank"}):
	string1=(each.text.replace('rank',''))
	rank.append(string1)
#for about
for each in filesoup.find_all('div',{"class":"celeb-middle"}):
	string1=(each.text)
	about.append(string1[:-21])
#for earning number
for each in filesoup.find_all('div',{"class":"earning-number"}):
	string1=(each.text)
	earning.append(string1)


#saving the data in a database

conn = sqlite3.connect('database.db')

cn = conn.cursor()
#inserting the data
for (a,b,c,d,e) in zip(rank,each_text,earning,about,filenames):
	cn.execute("insert into table1(rank,name,earnings,about,img) values(?,?,?,?,?)",(a,b,c,d,e))

conn.commit()
conn.close()
browser.close()