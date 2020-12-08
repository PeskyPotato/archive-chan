from multiprocessing import Pool
from time import time
import os
import re
import signal
import argparse
import requests
from models import Thread, boards, Params
from extractors.extractor import Extractor
from extractors.fourchan_api import FourChanAPIE

params = Params()


def parse_input():
    """
    Get user input, assigns url, thread, flags and
    all other global variables
    """

    parser = argparse.ArgumentParser(description="Archives 4chan threads")
    parser.add_argument("thread", help="Enter the link to the 4chan thread")
    parser.add_argument("-p", "--preserve_files", help="Save images and video files locally", action="store_true")
    parser.add_argument("-r", "--retries", help="Set total number of retries if a download fails")
    parser.add_argument("--posts", help="Number of posts to download")
    parser.add_argument("-v", "--verbose", help="Print more information on each post", action="store_true")
    parser.add_argument("--use_db", help="Stores threads into a database, this is experimental", action="store_true")
    parser.add_argument(
        "-a", "--archived",
        action="store_true",
        help="Download threads from /archive/ as well"
    )
    parser.add_argument(
        "-ao", "--archived_only",
        action="store_true",
        help="Downloads threads from /archive/ instead"
    )
    args = parser.parse_args()

    url = args.thread
    if args.preserve_files:
        params.preserve = True

    if args.verbose:
        params.verbose = True

    if args.retries:
        try:
            params.total_retries = int(args.retries)
        except ValueError:
            print("Number of retries must be an integer.")
            os.sys.exit(1)

    if args.posts:
        try:
            params.total_posts = int(args.posts)
        except ValueError:
            print("Number of posts must be an integer.")
            os.sys.exit(1)

    if args.use_db:
        params.use_db = True

    params.archived = args.archived
    params.archived_only = args.archived_only

    return url


def archive(thread_url):
    """
    Get values from the url to create a Thread object.
    Passes the thread to parse_html to be download.
    """
    match = None
    # check for valid urls in extractors
    for cls in Extractor.__subclasses__():
        extractor = None
        if re.match(cls.VALID_URL, thread_url):
            match = re.match(cls.VALID_URL, thread_url)
            extractor = cls()

    if not(match):
        print("Improper URL:", thread_url)
        return 1

    board = match.group('board')
    thread_id = match.group('thread')
    thread = Thread(thread_id, board, thread_url)

    params.path_to_download = 'threads/{}/{}'.format(thread.board, thread.tid)
    if not os.path.exists(params.path_to_download):
        os.makedirs(params.path_to_download)

    if params.verbose:
        print("Downloading thread:", thread.tid)
    extractor.extract(thread, params)


def feeder(url):
    """
    Checks the type of input and creates list of urls
    which are then used to call archive.
    """

    processes = []
    # list of thread urls
    if ".txt" in url:
        with open(url, "r") as f:
            for thread_url in f:
                processes.append(thread_url.strip())
    # a board (only gets from 4chan)
    elif url in boards:
        if not params.archived_only:
            url_api = "https://a.4cdn.org/{}/threads.json".format(url)
            r = requests.get(url_api)
            if r.status_code == 200:
                data = r.json()
                for page in data:
                    for thread in page["threads"]:
                        processes.append(
                            "http://boards.4chan.org/{}/thread/{}".format(url, thread["no"])
                        )
        if params.archived or params.archived_only:
            url_api = "https://a.4cdn.org/{}/archive.json".format(url)
            r = requests.get(url_api)
            if r.status_code == 200:
                data = r.json()
                for thread_no in data:
                    processes.append(
                        "http://boards.4chan.org/{}/thread/{}".format(url, thread_no)
                    )

        else:
            print("Invalid request:", url)
    # single thread url
    else:
        archive(url)

    sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = Pool(processes=4)
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        res = pool.map_async(archive, processes)
        res.get(86400)
    except KeyboardInterrupt:
        print("Terminating download")
        pool.terminate()
    else:
        pool.close()


def main():
    start_time = time()
    url = parse_input()
    feeder(url)
    print("Time elapsed: %.4fs" % (time() - start_time))


if __name__ == "__main__":
    main()
