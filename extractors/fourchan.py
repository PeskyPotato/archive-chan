from .extractor import Extractor
from models import Reply


class FourChanE(Extractor):
    VALID_URL = r'https?://boards.(4channel|4chan).org/(?P<board>[\w-]+)/thread/(?P<thread>[0-9]+)'

    def __init__(self):
        pass

    def extract(self, thread, params):
        self.parse_html(thread, params)

    def getOP(self, page_soup, params, thread):
        op_post = page_soup.find_all("div", {"class": "postContainer opContainer"})
        op_message = op_post[0].find_all("blockquote", {"class": "postMessage"})[0]
        op_img_src = op_post[0].find_all("div", {"class": "fileText"})[0].find_all("a")[0]['href']
        op_img_text = op_post[0].find_all("div", {"class": "fileText"})[0].find_all("a")[0].text
        op_subject = op_post[0].find_all("span", {"class": "subject"})[1].text
        op_name = op_post[0].find_all("span", {"class": "name"})[0].text
        op_date = op_post[0].find_all("span", {"class": "dateTime"})[0].text.split("No")[0]
        op_pid = op_post[0].find_all("div", {"class": "post op"})[0]['id'][1:]
        op_img_src = 'https:{}'.format(op_img_src)

        if params.verbose:
            print("Downloading post:", op_pid, "posted on", op_date[:-9])

        if params.preserve:
            self.download(op_img_src, op_img_text, params)
            op_img_src = '{}/{}'.format(thread.tid, op_img_text)

        p1 = Reply(op_name, op_date, op_message, op_pid, op_img_src, op_img_text, op_subject)
        return p1

    def getReplyWrite(self, page_soup, params, thread):
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
                    self.download(reply_img_src, reply_img_text, params)
                    reply_img_src = '{}/{}'.format(thread.tid, reply_img_text)

            reply_name = reply.find_all("span", {"class": "name"})[0].text
            reply_date = reply.find_all("span", {"class": "dateTime"})[0].text.split("No")[0]
            reply_pid = reply.find_all("div", {"class": "post reply"})[0]['id'][1:]

            if params.verbose:
                print("Downloading reply:", reply_pid, "replied on", reply_date[:-9])

            reply_info = Reply(reply_name, reply_date, reply_message, reply_pid, reply_img_src, reply_img_text)
            replies.append(reply_info)
        return replies
