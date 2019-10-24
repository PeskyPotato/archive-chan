from bs4 import BeautifulSoup as soup 
from archiver import archive
from urllib.request import Request
from urllib.request import urlopen
import requests
import json
import argparse
from time import time
from models import Thread


def catalog_threads(cat, verbose, preserve):
    url = "https://a.4cdn.org/{}/threads.json".format(cat)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        for page in data:
            for thread in page["threads"]:
                t_id = thread["no"]
                archive("http://boards.4chan.org/{}/thread/{}".format(cat, t_id), verbose, preserve)
    else:
        print("Invalid request:",url)


def main():
    start_time = time()

    p = False
    v = False

    parser = argparse.ArgumentParser(description="Archives 4chan threads")
    parser.add_argument("Board", help="Enter the board to download")
    parser.add_argument("-p","--preserve_files", help="Save images and video files locally", action="store_true")
    parser.add_argument("-v", "--verbose", help="Print more information on each post", action="store_true")

    args = parser.parse_args()

    cat = args.Board
    if args.preserve_files:
        p = True
    if args.verbose:
        v = True

    catalog_threads(cat, v, p)
    print("Time elapsed:", str(time()-start_time) + "s")

if __name__ == "__main__":
    main()

