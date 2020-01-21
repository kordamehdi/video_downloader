import requests 
import os
from bs4 import BeautifulSoup
import urllib2


# specify the URL of the archive here 
video_url = "https://www.learningcrux.com/play/wireshark-packet-analysis-and-ethical-hacking-core-skills/"
url = "https://www.learningcrux.com/video/wireshark-packet-analysis-and-ethical-hacking-core-skills/"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def creat_directories(i,j):

    title_url = url +str(i) + "/" + str(j)
    req = urllib2.Request(title_url , headers=hdr)
    page = urllib2.urlopen(req )
    soup = BeautifulSoup(page, "html.parser")
    name_box = soup.find('h2', attrs={'class': 'py-2'})
    name = name_box.text  # name = chaptre_title - video_title
    names = name.split('-',1)
    names = [ x.replace('/',"_") for x in names]
    names = [ x.strip() for x in names]

    if not os.path.exists("wireSharkCourse/"+names[0]):
        os.makedirs("wireSharkCourse/"+names[0])

    return names

def download_video_series(a,b):
  
    for i in range(a,21):
        for j in range(b,100):
            #creating the request
            link = video_url+ str(i) +"/" + str(j)
            res = requests.get(link, stream=True)
            contentType = res.headers["Content-Type"]
            if contentType != "video/mp4":
                break

            # creating the directorie
            names = creat_directories(i, j)
            file_name = '/'.join(names)
            file_name="wireSharkCourse/"+file_name
            print("Downloading video : %s" % names[1] +" in %s"% file_name)

            # download started

            with open(file_name, 'wb+') as f:
                for chunk in res.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print("downloaded!")
            with open("remember", 'wb+') as f:
                f.write(str(i)+"\n"+str(j+1))

    print("All videos downloaded!")



    return
  
  
if __name__ == "__main__":
    # download all videos
    with open("remember", "r") as fp:
        a=fp.readline()
        b=fp.readline()
    download_video_series(int(a),int(b))
     
