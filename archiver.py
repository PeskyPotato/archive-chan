from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import urlretrieve
from os import sys
import os
import argparse

# Parse input
parser = argparse.ArgumentParser(description="Archives 4chan threads")
parser.add_argument("Thread", help="Enter the link to the 4chan thread")
parser.add_argument("-p","--preserve_files", help="Save images and video files locally", action="store_true")

args = parser.parse_args()

url = args.Thread

if args.preserve_files:
    print("preserving files")
    preserve = True
else:
    preserve = False

thread = ''
cat = ''
path_to_css = 'css/stylesheet.css'

# Get thread
if len(sys.argv) == 2:
    url = sys.argv[1]

url_split = url.split('/')
if url_split[-2] != 'thread':
    thread = url_split[-2]
    cat = url_split[-4]
else:
    thread = url_split[-1]
    cat = url_split[-3]

print(url, thread)
print(url, thread)
print(url, thread)
print(url, thread)
print(url, thread)

path_to_download = '{}/{}'.format(cat, thread)
if not os.path.exists(path_to_download):
    os.makedirs(path_to_download)


def download(path, name):
    print("Downloading", path, name)
    urlretrieve('{}'.format(path), '{}/{}'.format(path_to_download, name))

def write_header(posttitle):
    html_file.write("<!DOCTYPE html>\n<html>\n<head>\n")
    html_file.write('\t<meta charset="utf-8"/>\n')
    html_file.write('\t<link rel="stylesheet" href="css/styles.css">\n')
    html_file.write('\t<title>' + posttitle + '</title>\n')
    html_file.write('</head>\n<body>\n')

# Get page soup to parse
# url = 'http://boards.4channel.org/{}/thread/{}'.format(cat,thread)
print(url)
req = Request(
    url,
    data=None,
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'
    }
)

uClient = urlopen(req)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "lxml")

# Get op details
op_post = page_soup.find_all("div", {"class":"postContainer opContainer"})
op_message = op_post[0].find_all("blockquote", {"class":"postMessage"})[0].text
op_img_src = op_post[0].find_all("div", {"class":"fileText"})[0].find_all("a")[0]['href']
op_img_text = op_post[0].find_all("div", {"class":"fileText"})[0].find_all("a")[0].text
op_subject = op_post[0].find_all("span", {"class":"subject"})[0].text
op_name = op_post[0].find_all("span", {"class":"name"})[0].text
op_date = op_post[0].find_all("span", {"class":"dateTime"})[0].text
op_pid = op_post[0].find_all("div", {"class":"post op"})[0]['id']
# op_backlinks = op_post[0].find_all("div", {"class":"backlink"})
op_img_src = 'https:{}'.format(op_img_src)

print("-----------------")
print("subject " + op_subject)
print("message " + op_message)
print("img "  + op_img_src + " text " + op_img_text)
print("name " + op_name)
print("date " + op_date)
print("pid " + op_pid)

if preserve:
    download(op_img_src, op_img_text)
    op_img_src = '{}/{}'.format(path_to_download,op_img_text)

# Get reply details
reply_post = page_soup.find_all("div", {"class":"postContainer replyContainer"})
# reply_message = reply_post[0].find_all("blockquote", {"class":"postMessage"})[0]
# reply_img = reply_post[0].find_all("a", {"class":"fileThumb hoverZoomLink"})
# reply_img_src = ''
# if len(reply_img) > 0:
#     print("we have an image")
#     reply_img_src = reply_img[0]['href']
#     reply_img_text = reply_img[0].text
# reply_name = reply_post[0].find_all("span", {"class":"name"})[0].text
# reply_date = reply_post[0].find_all("span", {"class":"dateTime"})[0].text
# reply_pid = reply_post[0].find_all("div", {"class":"post reply"})[0]['id']

# print("----------")
# print("message", reply_message)
# print("img", reply_img)
# print("name", reply_name)
# print("date", reply_date)
# print("pid", reply_pid)

# Write op details to html
with open("{}.html".format(thread), "w") as html_file:
    write_header(thread)
    
    # Title with link to media
    html_file.write('\t<div id="{}" class="post op">\n'.format(op_pid))
    html_file.write('\t\t<span class="name">{}</span>\n'.format(op_name))
    html_file.write('\t\tFile:\n')
    html_file.write('\t\t<a id="postlink" href="{}">{}</a>\n'.format(op_img_src, op_img_text))
    html_file.write('\t\t{}\n\t\t<br>\n'.format(op_date))

    # Media
    if op_img_src[-4:] == 'webm':
        html_file.write('\t\t<p style="float: left;">\n')
        html_file.write('\t\t\t<video height="450" controls>\n')
        html_file.write('\t\t\t\t<source src="{}" type="video/webm">\n\t\t\t</video>\n\t\t</p>\n'.format(op_img_src))

    else:
        html_file.write('\t\t<p style="float: left;">\n')
        html_file.write('\t\t\t<img src="{}" style="max-height: 250px">\n\t\t</p>\n'.format(op_img_src))

    # Message beside media
    html_file.write('\t\t<p style="float: left;">\n')
    html_file.write('\t\t\t<blockquote class="postMessage" id="{}">\n\t\t\t\t{}\n\t\t\t</blockquote>\n\t\t</p>\n'.format(op_pid, op_message))

    # Fit the background with the text + media
    html_file.write('\t\t<div style="clear: both;"></div>\n\t</div>\n')
    counter = 0
    for reply in reply_post:
        reply_message = reply.find_all("blockquote", {"class":"postMessage"})[0]
        reply_img = reply.find_all("div", {"class":"fileText"})
        reply_img_src = ''
        if len(reply_img) > 0:
            print("we have an image")
            reply_img = reply_img[0].find_all("a")[0]
            reply_img_src = reply_img['href']
            reply_img_text = reply_img.text
            reply_img_src = 'https:{}'.format(reply_img_src)
            
            if preserve:
                download(reply_img_src, reply_img_text)
                reply_img_src = '{}/{}'.format(path_to_download, reply_img_text)

        reply_name = reply.find_all("span", {"class":"name"})[0].text
        reply_date = reply.find_all("span", {"class":"dateTime"})[0].text
        reply_pid = reply.find_all("div", {"class":"post reply"})[0]['id']

        print("----------")
        print("message", reply_message)
        print("img", reply_img)
        print("name", reply_name)
        print("date", reply_date)
        print("pid", reply_pid)

        ###########
        #  REPLY  # 
        ###########

        # Title with link to media
        html_file.write('\t<div id="{}" class="post reply">\n'.format(reply_pid))
        html_file.write('\t\t<span class="name">{}</span>\n'.format(reply_name))

        if reply_img_src != '':
            html_file.write('\t\tFile:\n')
            html_file.write('\t\t<a id="postlink" href="{}">{}</a>\n\t\t'.format(reply_img_src, reply_img_text))
        html_file.write('\t\t{}\n\t\t<br>\n'.format(reply_date))

        # Media
        if reply_img_src != '':
            if reply_img_src[-4:] == 'webm':
                html_file.write('\t\t<p style="float: left;">\n')
                html_file.write('\t\t\t<video height="450" controls>\n')
                html_file.write('\t\t\t\t<source src="{}" type="video/webm">\n\t\t\t</video>\n\t\t</p>\n'.format(reply_img_src))

            else:
                html_file.write('\t\t<p style="float: left;">\n')
                html_file.write('\t\t\t<img src="{}" style="max-height: 250px">\n\t\t</p>\n'.format(reply_img_src))

        # Message beside media
        html_file.write('\t\t<p style="float: left;">\n')
        # html_file.write('\t\t\t<blockquote class="postMessage" id="{}">\n\t\t\t\t{}\n\t\t\t</blockquote>\n\t\t</p>\n'.format(reply_name, reply_message))
        html_file.write('\t\t\t{}\n'.format(reply_message))

        # Fit the background with the text + media
        html_file.write('\t\t<div style="clear: both;"></div>\n\t</div>')
        counter +=1
        if counter > 5:
            break
