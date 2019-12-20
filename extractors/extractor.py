from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError
from time import sleep
from flask import Flask, render_template
from models import Reply


class Extractor:
    def __init__(self):
        pass

    def extract(self, thread, params):
        # self.parse_html(thread, params)
        pass

    def parse_html(self, thread, params):
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
        op_info = self.getOP(page_soup, params, thread)
        replies = self.getReplyWrite(page_soup, params, thread)

        with app.app_context():
            rendered = render_template('thread.html', thread=thread, op=op_info, replies=replies)
            with open("threads/{}/{}.html".format(thread.board, thread.tid), "w+") as html_file:
                html_file.write(rendered)

    def download(self, path, name, params, retries=0):
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
                self.download(path, name, params, retries)

    def getOP(self, page_soup, params, thread):
        """
        Gets the OP information from page soup.
        Returns OP elements in a tuple of strings
        """
        pass

    def getReplyWrite(self, page_soup, params, thread):
        """
        Gets the reply information from page soup and
        returns a list of replies.
        """
        pass
