import os,sys,zipfile
import requests
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
import json
import re
import zipfile
import os
import sys
import shutil

directory_list=list()

#get list of names
for root, dirs, files in os.walk("movies/",topdown=False):
    for name in dirs:
        directory_list.append(os.path.join(name))

#print(directory_list)

moviename_dict=dict()

#filter out  put in another list
for dirname in directory_list:
    m=re.search('(.+).(\d\d\d\d).\d\d\d\dp', dirname)

#print(m.group(1))
str1 = m.group(1).replace(".","-")
str2 = m.group(2)

#print(str1)
#print(str2)
moviename_dict[str1]=str2

site = "http://subscene.com"

def remzip(fname):
    try:
        os.remove(fname)
    except IOError:
        print("Couldn't delete Zip File")

def extzip(fname):
    print (os.path.dirname(fname))
    try:
            with zipfile.ZipFile(fname,'r') as subzip:
                    subzip.extractall(os.path.dirname(fname))
    except:
            os.remove(fname)
            print("Could not extract zip file")
            sys.exit()

def dlzip(fname,req):
        print("Downloading Zip")
        try:
                with open(fname,'wb') as subzip:
                        subzip.write(req.content)
        except IOError:
                print("Could not write zip")
                print("Exiting")
                os.system("Pause")
                sys.exit()
        print("Downloaded zip to:",fname)

def rename(srtname,loaction,name):
        rchoice=raw_input("Want To rename Subtitle?(Y/N): ")
        if rchoice in 'yY':
            rename=raw_input('Rename to(-s for same as search: ')
            if rename == '-s':
                rename= name 
            renloc=loaction+rename+".srt"
            os.rename(srtname,renloc)
            print("File renamed")
            print("Thanks for using the script")
            os.system("pause")
            sys.exit()
        elif rchoice in 'nN':
            print("Thanks for using script")
            os.system("pause")
            sys.exit()

  def findSub(query):
      req=requests.get(query)
      source=BeautifulSoup(req.text,"html.parser")

      subs = source.find_all('tr')

      link=site
      hrefs=[]
      nsub=0
      snames=[]

      for sub in subs:
          tdata = sub.find_all('td')
          if "English" in tdata[0].get_text():
                nsub +=1
                sname=tdata[0].find_all('span')[1].get_text
                snames.append(sname)
                if nsub >10:
                         break
                print(nsub,". ",sname)
                hrefs.append(tdata[0].find('a')['href'])   
      try:
            assert(len(hrefs) != 0)
      except AssertionError:
            print("Sorry Sub could not be found")
            print("exiting")
            sys.exit(1)

      schoice = int(raw_input("Select Sub: "))-1
      href=hrefs[schoice] 

      link+ = href

      try:
            assert(link != site)
      except AssertionError:
             print("Sorry couldnt be found")
             restart()

      req = requests.get(link)
      source=BeautifulSoup(req.text,"html.parser")

      subname=sname[schoice]
      print("subtitle: ",subname)

      choice=rw_input("proceed?(Y/N): ")
      while(choice != 'y'):
              if(choice=='n' or choice=='N'):
                  print("Exiting")
                  os.system("pause")
                  sys.exit()
              choice=raw_input("proceed? (Y/N): ")

      dl = source.find('div',class_='download')
      dlink=site+dl.a['href']

      req=requests.get(dlink)

      location= os.path.abspath(raw_input("Save subtitle ti folder"))+'\\'
      if location=='-s':
          location=os.path.abspath(os.getcwd())+"\\"
      fname=location+'sub.zip'
      srtname=location+subname+".srt"
      dlzip(fname,req)
      extzip(fname)
      remzip(fname)
      rename(srtname,location,name)

def SearchQuery(name):
        query="http://subscene.com.subtitles.release?q="
        cname=name.replace(" ","%20")
        query +=cname+"&r=true"
        return query

def restart():
        os.system('pause')
        os.system('cls')
        os.system('"'+_file_+'"')

def credits():
        print 
        print("-----------------")
        os.system("pause")
           