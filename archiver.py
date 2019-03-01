from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import URLError
from os import sys
import os
import argparse

# Boards
boards = {
    #Japanese Culture
    "a" : "Anime and Manga",
    "c" : "Anime/Cute",
    "w" : "Anime/Wallpapers",
    "m" : "Mecha",
    "cgl" : "Cosplay and EGL",
    "cm" : "Cute/Male",
    "f" : "Flash",
    "n" : "Transportation",
    "jp" : "Otaku Culture", 
    "vp" : "Pokemon",
    #Interests
    "v" : "Video Games",
    "vg" : "Video Games Generals",
    "vr" : "Retro Games",
    "co" : "Comics & Cartoons",
    "g" : "Technology",
    "tv" : "Television & Film",
    "k" : "Weapons",
    "o" : "Auto",
    "an" : "Animals & Nature",
    "tg" : "Traditional Games",
    "qst" : "Quests", 
    "sp" : "Sports",
    "asp" : "Alternative Sports",
    "sci" : "Science & Math",
    "int" : "International", 
    "out" : "Outdoors",
    "toy" : "Toys",
    "biz" : "Business & Finance",
    #Creative
    "i" : "Oekaki",
    "po" : "Papercraft & Origami",
    "p" : "Photography",
    "ck" : "Food & Cooking",
    "ic" : "Artwork/Critique",
    "wg" : "Wallpapers/General",
    "mu" : "Music", 
    "fa" : "Fashion", 
    "3" : "3DCG",
    "gd" : "Graphic Design",
    "diy" : "Do-It-Yourself",
    "wsg" : "Worksafe GIF",
    #Adult
    "s" : "Beautiful Women",
    "hc" : "Hardcore",
    "hm" : "Handsome Men",
    "h" : "Hentai", 
    "e" : "Ecchi", 
    "u" : "Yuri", 
    "d" : "Hentai/Alternative",
    "y" : "Yaoi", 
    "t" : "Torrents", 
    "hr" : "High Resolution",
    "gif" : "Adult GIF",
    #Other
    "trv" : "Travel",
    "fit" : "Fitness", 
    "x" : "Paranormal", 
    "lit" : "Literature", 
    "adv" : "Advice",
    "lgbt" : "LGBT",
    "mlp" : "Pony",
    #MISC
    "b" : "Random",
    "r" : "Requests",
    "r9k" : "ROBOT9001",
    "pol" : "Politically Incorrect",
    "soc" : "Cams & Meetups", 
    "s4s" : "Shit 4chan Says"
}

url = ''
preserve = False
thread = ''
cat = ''
path_to_css = ''
path_to_download = '' 
total_retries = 5
total_posts = None

'''
Get user input, assigns url, thread, flags and 
all other global variables
'''
def parse_input():
    global url, preserve, thread, cat, path_to_css, path_to_download, total_retries, total_posts

    # Parse input
    parser = argparse.ArgumentParser(description="Archives 4chan threads")
    parser.add_argument("Thread", help="Enter the link to the 4chan thread")
    parser.add_argument("-p","--preserve_files", help="Save images and video files locally", action="store_true")
    parser.add_argument("-r", "--retries", help="Set total number of retries if a download fails")
    parser.add_argument("--posts", help="Number of posts to download")
    
    args = parser.parse_args()

    url = args.Thread

    if args.preserve_files:
        print("preserving files")
        preserve = True

    if args.retries:
        total_retries = int(args.retries)
    
    if args.posts:
        total_posts = int(args.posts)

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

    path_to_download = '{}/{}'.format(cat, thread)
    if not os.path.exists(path_to_download):
        os.makedirs(path_to_download)

'''
Donwload file to `path` with `name`. If fails
wait and retry, until total retries reached.
'''
def download(path, name, retries = 0):
        try:
            print("Downloading", path, name)
            urlretrieve('{}'.format(path), '{}/{}'.format(path_to_download, name))
        except URLError:
            if(total_retries > retries):
                print("Failed, retrying", retries)
                retries += 1
                download(path, name, retries)

'''
Parse html, get soup and write post and replies
to html_file. Calls download if preserve is True
'''
def parse_html():
    # Get page soup to parse
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
    op_message = op_post[0].find_all("blockquote", {"class":"postMessage"})[0]
    op_img_src = op_post[0].find_all("div", {"class":"fileText"})[0].find_all("a")[0]['href']
    op_img_text = op_post[0].find_all("div", {"class":"fileText"})[0].find_all("a")[0].text
    op_subject = op_post[0].find_all("span", {"class":"subject"})[0].text
    op_name = op_post[0].find_all("span", {"class":"name"})[0].text
    op_date = op_post[0].find_all("span", {"class":"dateTime"})[0].text
    op_pid = op_post[0].find_all("div", {"class":"post op"})[0]['id']
    op_img_src = 'https:{}'.format(op_img_src)

    print("-----------------")
    print("subject ", op_subject)
    print("message ", op_message)
    print("img ", op_img_src , " text ", op_img_text)
    print("name " + op_name)
    print("date " + op_date)
    print("pid " + op_pid)

    if preserve:
        download(op_img_src, op_img_text)
        op_img_src = '{}/{}'.format(path_to_download,op_img_text)

    # Get reply details
    reply_post = page_soup.find_all("div", {"class":"postContainer replyContainer"})

    # Write op details to html
    with open("{}.html".format(thread), "w") as html_file:
        html_file.write("<!DOCTYPE html>\n<html>\n<head>\n")
        html_file.write('\t<meta charset="utf-8"/>\n')
        html_file.write('\t<link rel="stylesheet" href="css/styles.css">\n')
        html_file.write('\t<title>' + thread + '</title>\n')
        html_file.write('</head>\n<body>\n')
        html_file.write('<div class="boardTitle">/{}/ - {}</div>'.format(cat, boards[cat]))
        
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
        # html_file.write('\t\t\t<blockquote class="postMessage" id="{}">\n\t\t\t\t{}\n\t\t\t</blockquote>\n\t\t</p>\n'.format(op_pid, op_message))
        html_file.write('\t\t\t{}\n'.format(op_message))

        # Fit the background with the text + media
        html_file.write('\t\t<div style="clear: both;"></div>\n\t</div>\n')
        counter = 1
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
            if total_posts:
                counter +=1
                if counter > total_posts:
                    break


if __name__ == "__main__":
    parse_input()
    parse_html()