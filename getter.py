from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError
from time import sleep
from flask import Flask, render_template
from models import Reply, Params

param = Params()


def parse_html(thread, params):
    """
    Parse html, get soup and write post and replies
    to html_file. Calls download if preserve is True
    """

    app = Flask('archive-chan', template_folder='./assets/templates/')

    req = Request(
        thread.url,
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

    try:
        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()
    except Exception as e:
        print(e, "retrying...")
        sleep(10)
        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()

    page_soup = soup(page_html, "lxml")
    op_info = getOP(page_soup, params, thread)
    replies = getReplyWrite(page_soup, params, thread)

    with app.app_context():
        rendered = render_template('thread.html', thread=thread, op=op_info, replies=replies)
        with open("threads/{}/{}.html".format(thread.board, thread.tid), "w+") as html_file:
            html_file.write(rendered)


def download(path, name, params, retries=0):
    """
    Donwload file to `path` with `name`. If fails wait and retry,
    until total retries reached.
    """

    try:
        if params.verbose:
            print("Downloading image:", path, name)
        urlretrieve('{}'.format(path), '{}/{}'.format(params.path_to_download, name))
    except URLError:
        if(params.total_retries > retries):
            print("Failed, retrying", retries)
            retries += 1
            download(path, name, params, retries)


def getOP(page_soup, params, thread):
    """
    Gets the OP information from page soup.
    Returns OP elements in a tuple of strings
    """

    op_post = page_soup.find_all("div", {"class": "postContainer opContainer"})
    op_message = op_post[0].find_all("blockquote", {"class": "postMessage"})[0]
    op_img_src = op_post[0].find_all("div", {"class": "fileText"})[0].find_all("a")[0]['href']
    op_img_text = op_post[0].find_all("div", {"class": "fileText"})[0].find_all("a")[0].text
    op_subject = op_post[0].find_all("span", {"class": "subject"})[0].text
    op_name = op_post[0].find_all("span", {"class": "name"})[0].text
    op_date = op_post[0].find_all("span", {"class": "dateTime"})[0].text.split("No")[0]
    op_pid = op_post[0].find_all("div", {"class": "post op"})[0]['id'][1:]
    op_img_src = 'https:{}'.format(op_img_src)

    if params.verbose:
        print("Downloading post:", op_pid, "posted on", op_date[:-12])

    if params.preserve:
        download(op_img_src, op_img_text, params)
        op_img_src = '{}/{}'.format(thread.tid, op_img_text)

    p1 = Reply(op_name, op_date, op_message, op_pid, op_img_src, op_img_text, op_subject)
    return p1


def getReplyWrite(page_soup, params, thread):
    """
    Gets the reply information from page soup and
    returns a list of replies.
    """

    reply_post = page_soup.find_all("div", {"class": "postContainer replyContainer"})
    replies = []
    total_posts = len(reply_post)
    if params.total_posts:
        total_posts = min(params.total_posts, len(reply_post))

    for i in range(0, total_posts):
        reply = reply_post[i]
        reply_message = reply.find_all("blockquote", {"class": "postMessage"})[0]
        reply_img = reply.find_all("div", {"class": "fileText"})
        reply_img_src = ''
        reply_img_text = ''
        if len(reply_img) > 0:
            reply_img = reply_img[0].find_all("a")[0]
            reply_img_src = reply_img['href']
            reply_img_text = reply_img.text
            reply_img_src = 'https:{}'.format(reply_img_src)

            if params.preserve:
                download(reply_img_src, reply_img_text, params)
                reply_img_src = '{}/{}'.format(thread.tid, reply_img_text)

        reply_name = reply.find_all("span", {"class": "name"})[0].text
        reply_date = reply.find_all("span", {"class": "dateTime"})[0].text.split("No")[0]
        reply_pid = reply.find_all("div", {"class": "post reply"})[0]['id'][1:]

        if params.verbose:
            print("Downloading reply:", reply_pid, "replied on", reply_date[:-9])

        reply_info = Reply(reply_name, reply_date, reply_message, reply_pid, reply_img_src, reply_img_text)
        replies.append(reply_info)
    return replies
