from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import URLError
from writer import writeReply
from os import sys
from models import Reply

'''
Donwload file to `path` with `name`. If fails wait and retry, 
until total retries reached.

Keyword Arguments:
    path            -- 4chan url to file as string
    verbose         -- True to print
    path_to_download -- download path as string
    total_retries   -- maximum number of retries on URLError as int
    retries         -- used for recursion, starting value 0  
'''
def download(path, name, verbose, path_to_download, total_retries, retries = 0):
    try:
        if verbose: print("Downloading image:", path, name)
        urlretrieve('{}'.format(path), '{}/{}'.format(path_to_download, name))
    except URLError:
        if(total_retries > retries):
            print("Failed, retrying", retries)
            retries += 1
            download(path, name, path_to_download, total_retries, retries)

'''
Gets the OP information from page soup.

Keyword arguments:
    page_soup       -- page_soup object to parse
    verbose         -- True to print
    preserve        -- True to download media
    path_to_download -- download path as string
    total_retries   -- maximum number of retries on URLError as int

Returns OP elements in a tuple of strings
'''
def getOP(page_soup, verbose, preserve, path_to_download, total_retries, thread):
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

    if verbose: print("Downloading post:", op_pid, "posted on", op_date[:-12])

    if preserve:
        download(op_img_src, op_img_text, verbose, path_to_download, total_retries)
        op_img_src = '{}/{}'.format(thread.tid, op_img_text)

    p1 = Reply(op_name, op_date, op_message, op_pid, op_img_src, op_img_text, op_subject)
    return p1

'''
Gets the reply information from page soup and appends
them all to the html file.

Keyword arguments:
    page_soup       -- page_soup object to parse
    verbose         -- True to print
    preserve        -- True to download media
    path_to_download -- download path as string
    total_retries   -- maximum number of retries on URLError as int
    thread          -- thread number from url as string
'''
def getReplyWrite(page_soup, verbose, preserve, path_to_download, total_retries, total_posts, thread):
    reply_post = page_soup.find_all("div", {"class":"postContainer replyContainer"})
    reply_count = 0 # stats counter for replies downloaded
    image_count = 1 # stats counter for images downloaded
    counter = 1
    for reply in reply_post:
        reply_message = reply.find_all("blockquote", {"class":"postMessage"})[0]
        reply_img = reply.find_all("div", {"class":"fileText"})
        reply_img_src = ''
        reply_img_text = ''
        if len(reply_img) > 0:
            reply_img = reply_img[0].find_all("a")[0]
            reply_img_src = reply_img['href']
            reply_img_text = reply_img.text
            reply_img_src = 'https:{}'.format(reply_img_src)

            if preserve:
                download(reply_img_src, reply_img_text, verbose, path_to_download, total_retries)
                reply_img_src = '{}/{}'.format(thread.tid, reply_img_text)
                image_count += 1

        reply_name = reply.find_all("span", {"class":"name"})[0].text
        reply_date = reply.find_all("span", {"class":"dateTime"})[0].text
        reply_pid = reply.find_all("div", {"class":"post reply"})[0]['id']

        if verbose: print("Downloading reply:", reply_pid, "replied on", reply_date[:-12])
        
        reply_info = Reply(reply_name, reply_date, reply_message, reply_pid, reply_img_src, reply_img_text)

        writeReply(thread, reply_info)

        if total_posts:
            counter += 1
            if counter > total_posts:
                return
        reply_count += 1