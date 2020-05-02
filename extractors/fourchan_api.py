import requests
from flask import Flask, render_template
from .extractor import Extractor
from models import Reply
from resources.database.db_interface import Database


class FourChanAPIE(Extractor):
    VALID_URL = r'https?://boards.(4channel|4chan).org/(?P<board>[\w-]+)/thread/(?P<thread>[0-9]+)'

    def __init__(self):
        self.thread_data = None
        self.db = Database()

    def extract(self, thread, params):
        self.get_data(thread, params)

    def get_data(self, thread, params):
        """
        Get JSON and parse replies from 4chan API and
        writes to html_file. Calls download if preseve
        is True.
        """
        app = Flask('archive-chan', template_folder='./assets/templates/')

        r = requests.get("https://a.4cdn.org/{}/thread/{}.json".format(thread.board, thread.tid))
        self.thread_data = None
        if(r.status_code == requests.codes.ok):
            self.thread_data = r.json()
        else:
            return

        op_info = self.getOP(params, thread)
        replies = self.getReplyWrite(params, thread)

        with app.app_context():
            rendered = render_template('thread.html', thread=thread, op=op_info, replies=replies)
            with open("threads/{}/{}.html".format(thread.board, thread.tid), "w+") as html_file:
                html_file.write(rendered)

    def getOP(self, params, thread):
        op_post = self.thread_data["posts"][0]

        if "tim" in op_post.keys():
            op_post["img_src"] = "https://i.4cdn.org/{}/{}{}".format(thread.board, op_post["tim"], op_post["ext"])
            op_img_text = "{}{}".format(op_post["filename"], op_post["ext"])

            if params.preserve:
                self.download(op_post["img_src"], op_img_text, params)
                op_post["img_src"] = '{}/{}'.format(thread.tid, op_img_text)

        if params.verbose:
            print("Downloading post:", op_post["no"], "posted on", op_post["now"])

        op_post["board"] = thread.board
        p1 = Reply(op_post)
        self.db.insert_reply(p1)
        return p1

    def getReplyWrite(self, params, thread):
        reply_post = self.thread_data["posts"][1:]

        replies = []
        total_posts = len(reply_post)
        if params.total_posts:
            total_posts = min(params.total_posts, len(reply_post))

        for i in range(0, total_posts):
            reply = reply_post[i]

            if "tim" in reply.keys():
                reply["img_src"] = "https://i.4cdn.org/{}/{}{}".format(thread.board, reply["tim"], reply["ext"])
                reply_img_text = "{}{}".format(reply["filename"], reply["ext"])
                if params.preserve:
                    self.download(reply["img_src"], reply_img_text, params)
                    reply["img_src"] = '{}/{}'.format(thread.tid, reply_img_text)

            if params.verbose:
                print("Downloading reply:", reply["no"], "replied on", reply["now"])

            reply["board"] = thread.board
            reply_info = Reply(reply)
            replies.append(reply_info)
            self.db.insert_reply(reply_info)
        return replies
