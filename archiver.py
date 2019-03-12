from writer import *
from getter import *
import argparse
from time import time
import os

url = ''
preserve = False
thread = ''
cat = ''
path_to_css = ''
path_to_download = '' 
total_retries = 5
total_posts = None
verbose = False
#number of posts, number of images
stats = []

'''
Get user input, assigns url, thread, flags and 
all other global variables
'''
def parse_input():
    global url, preserve, thread, cat, path_to_css, path_to_download, total_retries, total_posts, verbose

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

    path_to_css = '../css/stylesheet.css'

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

    path_to_download = '{}/{}'.format(cat, thread)
    if not os.path.exists(path_to_download):
        os.makedirs(path_to_download)

    if verbose: print("Downloading thread:", thread)

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

    writeHeader(thread, cat)
    op_info  = getOP(page_soup, verbose, preserve, path_to_download, total_retries, thread)    
    writeOP(thread, cat, op_info[5], op_info[0], op_info[1], op_info[2], op_info[3], op_info[4])
    getReplyWrite(page_soup, verbose, preserve, path_to_download, total_retries, thread, total_posts, cat)

def main():
    start_time = time()
    parse_input()
    parse_html()
    print("Time elapsed:", str(time()-start_time) + "s")

if __name__ == "__main__":
    main()