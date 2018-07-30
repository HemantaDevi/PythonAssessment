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

print(moviename_dict)
similarurl="https://subscene.com/subtitles/" 

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)
        for info in zf.infolist():
            fname=info.filename
            return fname

def subDownloader(url,cname):
    usock = urlopen("http://www.google.com/") #function for opening desired url
    file_name = cname+".zip"
    f=open(file_name, 'wb')                        
    file_size = int(usock.info().getheaders("Content-Length")[0]) #getting size in bytes of fi
    downloaded=0                      
    block_size=8192   #bytes to be downloaded in each loop till file pointer does not return eof
    while True:
        buff = usock.read(block_size)
        if not buff:
                break
        downloaded = downloaded + len(buff)
        f.wirte(buff)
    f.close()
    path=os.getcwd()
    name=unzip(file_name,path)
    os.rename(name,cname+".srt")
    os.remove(file_name)

def getSubtitleLink(page):
    start_link=page.find('/english')
    if start_link==-1:
        return False
    page=page[start_link-100:]
    start_link=page.find("<a href=")
    if start_link==-1:
        return False
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url

def get_page(url):
    hdr={'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req= Request(url,headers=hdr)
    return urlopen(req).read()

def get_download_link(url):
    page=get_page(url)
    start_link=page.find('<div class="download">')
    if start_link==-1:
        return False
    page=page[start_link-100:]
    start_link=page.find("<a href=")
    if start_link==-1:
    
        return False
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url

mainUrl="http://subscene.com"

path=sys.argv[1]
start_index=path.rindex("\\")
end_index=path.rindex(".")
filename=path[start_index+1:end_index]
url="http://subscene.com/subtitles/release?q="
fUrl=url+filename
extn=getSubtitleLink(get_page(fUrl))
url=mainUrl+extn
downlink=get_download_link(url)
fDownllink=mainUrl+downlink
subDownloader(fDownllink,filename)

#while True:
    #a=raw_input("Done")
    #if a:
        #break
#print("error")


