import requests
import bs4
import argparse
import os

parser = argparse.ArgumentParser("Helper tool for downloading all files from a given AtoZmedia link")
parser.add_argument("url", type=str, help="URL which lists all files available for download - usually https://www2.atozmedia.com/soundcard/default.asp?view=download&soundcardID=XXXX&downloadCode=XXXXXXXXXXXXXXXX")
parser.add_argument("-d", "--dest-dir", type=str, help="Destination directory to write files to")
args = parser.parse_args()

URL = args.url
DEST_DIR = args.dest_dir
if DEST_DIR == None or DEST_DIR == "":
    DEST_DIR == "./"

response = requests.get(URL)
content = response.content
soup = bs4.BeautifulSoup(content, features='html.parser')

# <a href="../common/download.asp?type=soundcard&amp;downloadCode=XXXXXXXXXXX&amp;uploadID=XXXXXX" target="_blank">BAND - SONG.wav</a>
for item in soup.find_all('li'):
    item: bs4.Tag
    for child in item.children:
        if child.name != 'a':
            continue
        link = child['href']
        if link[:2] == '..':
            link = URL[:URL.index('/', 10)] + link[2:]
        filename = child.get_text()
        file = requests.get(link)
        try:
            open(os.path.join(DEST_DIR, filename), "wb+").write(file.content)
            print("Successfully wrote file \"{}\" to disk".format(filename))
        except:
            raise
