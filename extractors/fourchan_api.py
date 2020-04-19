import requests
from flask import Flask, render_template
from .extractor import Extractor
from models import Reply


class FourChanAPIE(Extractor):
    VALID_URL = r'https?://boards.(4channel|4chan).org/(?P<board>[\w-]+)/thread/(?P<thread>[0-9]+)'

    def __init__(self):
        self.thread_data = None

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
        op_name = op_post["name"]
        op_date = op_post["now"]
        op_message = op_post.get("com", "")
        op_pid = op_post["no"]
        op_subject = op_post["sub"]

        if "tim" in op_post.keys():
            op_img_src = "https://i.4cdn.org/{}/{}{}".format(thread.board, op_post["tim"], op_post["ext"])
            op_img_text = "{}{}".format(op_post["filename"], op_post["ext"])

            if params.preserve:
                self.download(op_img_src, op_img_text, params)
                op_img_src = '{}/{}'.format(thread.tid, op_img_text)

        if params.verbose:
            print("Downloading post:", op_pid, "posted on", op_date)

        p1 = Reply(op_name, op_date, op_message, op_pid, op_img_src, op_img_text, op_subject)
        return p1

    def getReplyWrite(self, params, thread):
        reply_post = self.thread_data["posts"][1:]

        replies = []
        total_posts = len(reply_post)
        if params.total_posts:
            total_posts = min(params.total_posts, len(reply_post))

        for i in range(0, total_posts):
            reply = reply_post[i]
            reply_message = reply.get("com", "")

            reply_img_src = ''
            reply_img_text = ''
            if "tim" in reply.keys():
                reply_img_src = "https://i.4cdn.org/{}/{}{}".format(thread.board, reply["tim"], reply["ext"])
                reply_img_text = "{}{}".format(reply["filename"], reply["ext"])

                if params.preserve:
                    self.download(reply_img_src, reply_img_text, params)
                    reply_img_src = '{}/{}'.format(thread.tid, reply_img_text)

            reply_name = reply["name"]
            reply_date = reply["now"]
            reply_pid = reply["no"]

            if params.verbose:
                print("Downloading reply:", reply_pid, "replied on", reply_date)

            reply_info = Reply(reply_name, reply_date, reply_message, reply_pid, reply_img_src, reply_img_text)
            replies.append(reply_info)
        return replies
