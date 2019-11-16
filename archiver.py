from writer import *
from getter import *
from models import Thread
import requests
import argparse
from time import time
from time import sleep
import re
import os
from multiprocessing import Process, Pool
import signal

VALID_URL = r'https?://boards.(4channel|4chan).org/(?P<board>[\w-]+)/thread/(?P<thread>[0-9]+)'
verbose = False
preserve = False
total_retries = 5
total_posts = None

'''
Get user input, assigns url, thread, flags and 
all other global variables
'''
def parse_input():
    global preserve, total_retries, total_posts, verbose
    # Parse input
    parser = argparse.ArgumentParser(description="Archives 4chan threads")
    parser.add_argument("Thread", help="Enter the link to the 4chan thread")
    parser.add_argument("-p","--preserve_files", help="Save images and video files locally", action="store_true")
    parser.add_argument("-r", "--retries", help="Set total number of retries if a download fails")
    parser.add_argument("--posts", help="Number of posts to download")
    parser.add_argument("-v", "--verbose", help="Print more information on each post", action="store_true")
    
    args = parser.parse_args()

    url = args.Thread
    if args.preserve_files:
        preserve = True

    if args.verbose:
        verbose = True

    if args.retries:
        total_retries = int(args.retries)
    
    if args.posts:
        total_posts = int(args.posts)

    return url

'''
Parse html, get soup and write post and replies
to html_file. Calls download if preserve is True
'''
def parse_html(thread):
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
        sleep(10)
        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()

    page_soup = soup(page_html, "lxml")
    writeHeader(thread)
    op_info  = getOP(page_soup, verbose, preserve, 
                     path_to_download, total_retries, thread)    
    writeOP(thread, op_info)
    getReplyWrite(page_soup, verbose, preserve, 
                  path_to_download, total_retries, total_posts, thread)

'''
Get values from the url to create a Thread object.
Passes the thread to parse_html to being download.
'''
def archive(thread_url):
    global verbose, preserve
    match =re.match(VALID_URL, thread_url)
    if not(match):
        print("Improper URL:", thread_url)
        sys.exit(1)

    board = match.group('board')
    thread_id = match.group('thread')
    thread = Thread(thread_id, board, thread_url)

    global path_to_download
    path_to_download = 'threads/{}/{}'.format(thread.board, thread.tid)
    if not os.path.exists(path_to_download):
        os.makedirs(path_to_download)

    if verbose: 
        print("Downloading thread:", thread.tid)
    parse_html(thread)

'''
Checks the type of input and creates list of urls
which are then used to call archive.
'''
def feeder(url):
    processes = []
    if ".txt" in url:
        with open(url, "r") as f:
            for thread_url in f:
                processes.append(thread_url.strip())
    elif url in boards:
        url_api = "https://a.4cdn.org/{}/threads.json".format(url)
        r = requests.get(url_api)
        if r.status_code == 200:
            data = r.json()
            for page in data:
                for thread in page["threads"]:
                    processes.append("http://boards.4chan.org/{}/thread/{}".format(url, thread["no"]))
        else:
            print("Invalid request:", url)
    else:
        archive(url)

    sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = Pool(processes=4)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        res = pool.map_async(archive, processes)
        res.get(60)
    except KeyboardInterrupt:
        print("Terminating download")
        pool.terminate()
    else:
        pool.close()

def main():
    start_time = time()
    url  = parse_input()
    feeder(url)
    print("Time elapsed: %.4fs" % (time()-start_time))

if __name__ == "__main__":
    main()