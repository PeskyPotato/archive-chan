from ..database.db_interface import Database
from flask import render_template, send_from_directory, abort
from models import Thread

def index():
    return "Homepage"

def thread(board, no):
    db = Database()
    replies = db.fetch_replies(int(no))
    if not replies:
        abort(404)

    thread = Thread(no, board, '')
    op_info = db.reply_to_dict(replies[0])
    op_info['img_src'] = "/threads/{}/{}/{}".format(board, op_info["no"], op_info["filename"]+op_info["ext"])
    _replies = []
    for r in replies[1:]:
        reply = db.reply_to_dict(r)
        if "tim" in reply.keys():
            reply['img_src'] = "/threads/{}/{}/{}".format(board, op_info["no"], reply["filename"]+reply["ext"])
        _replies.append(reply)

    return render_template('thread.html', thread=thread, op=op_info, replies=_replies)

def image_path(filename):
    return send_from_directory(app.config)