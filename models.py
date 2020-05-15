boards = {
    # Japanese Culture
    "a": ["Anime & Manga", "favicon-ws.ico", "variables-ws.css"],
    "c": ["Anime/Cute", "favicon-ws.ico", "variables-ws.css"],
    "w": ["Anime/Wallpapers", "favicon-ws.ico", "variables-ws.css"],
    "m": ["Mecha", "favicon-ws.ico", "variables-ws.css"],
    "cgl": ["Cosplay & EGL", "favicon-ws.ico", "variables-ws.css"],
    "cm": ["Cute/Male", "favicon-ws.ico", "variables-ws.css"],
    "f": ["Flash", "favicon.ico", "variables.css"],
    "n": ["Transportation", "favicon-ws.ico", "variables-ws.css"],
    "jp": ["Otaku Culture", "favicon-ws.ico", "variables-ws.css"],
    # Video Games
    "v": ["Video Games", "favicon-ws.ico", "variables-ws.css"],
    "vg": ["Video Games Generals", "favicon-ws.ico", "variables-ws.css"],
    "vp": ["Pokemon", "favicon-ws.ico", "variables-ws.css"],
    "vr": ["Retro Games", "favicon-ws.ico", "variables-ws.css"],
    # Interests
    "co": ["Comics & Cartoons", "favicon-ws.ico", "variables-ws.css"],
    "g": ["Technology", "favicon-ws.ico", "variables-ws.css"],
    "tv": ["Television & Film", "favicon-ws.ico", "variables-ws.css"],
    "k": ["Weapons", "favicon-ws.ico", "variables-ws.css"],
    "o": ["Auto", "favicon-ws.ico", "variables-ws.css"],
    "an": ["Animals & Nature", "favicon-ws.ico", "variables-ws.css"],
    "tg": ["Traditional Games", "favicon-ws.ico", "variables-ws.css"],
    "sp": ["Sports", "favicon-ws.ico", "variables-ws.css"],
    "asp": ["Alternative Sports", "favicon-ws.ico", "variables-ws.css"],
    "sci": ["Science & Math", "favicon-ws.ico", "variables-ws.css"],
    "his": ["History & Humanities", "favicon-ws-ico", "variables-ws.css"],
    "int": ["International", "favicon-ws.ico", "variables-ws.css"],
    "out": ["Outdoors", "favicon-ws.ico", "variables-ws.css"],
    "toy": ["Toys", "favicon-ws.ico", "variables-ws.css"],
    # Creative
    "i": ["Oekaki", "favicon.ico", "variables.css"],
    "po": ["Papercraft & Origami", "favicon-ws.ico", "variables-ws.css"],
    "p": ["Photography", "favicon-ws.ico", "variables-ws.css"],
    "ck": ["Food & Cooking", "favicon-ws.ico", "variables-ws.css"],
    "ic": ["Artwork/Critique", "favicon.ico", "variables.css"],
    "wg": ["Wallpapers/General", "favicon.ico", "variables.css"],
    "lit": ["Literature", "favicon-ws.ico", "variables-ws.css"],
    "mu": ["Music", "favicon-ws.ico", "variables-ws.css"],
    "fa": ["Fashion", "favicon-ws.ico", "variables-ws.css"],
    "3": ["3DCG", "favicon-ws.ico", "variables-ws.css"],
    "gd": ["Graphic Design", "favicon-ws.ico", "variables-ws.css"],
    "diy": ["Do-It-Yourself", "favicon-ws.ico", "variables-ws.css"],
    "wsg": ["Worksafe GIF", "favicon-ws.ico", "variables-ws.css"],
    "qst": ["Quests", "favicon-ws.ico", "variables-ws.css"],
    # Other
    "biz": ["Business & Finance", "favicon-ws.ico", "variables-ws.css"],
    "trv": ["Travel", "favicon-ws.ico", "variables-ws.css"],
    "fit": ["Fitness", "favicon-ws.ico", "variables-ws.css"],
    "x": ["Paranormal", "favicon-ws.ico", "variables-ws.css"],
    "adv": ["Advice", "favicon-ws.ico", "variables-ws.css"],
    "lgbt": ["LGBT", "favicon-ws.ico", "variables-ws.css"],
    "mlp": ["Pony", "favicon-ws.ico", "variables-ws.css"],
    "news": ["Current News", "favicon-ws.ico", "variables-ws.css"],
    "wsr": ["Worksafe Requests", "favicon-ws.ico", "variables-ws.css"],
    "vip": ["Very Important Posts", "favicon-ws.ico", "variables-ws.css"],
    # Misc.
    "b": ["Random", "favicon.ico", "variables.css"],
    "r9k": ["ROBOT9001", "favicon.ico", "variables.css"],
    "pol": ["Politically Incorrect", "favicon.ico", "variables.css"],
    "bant": ["International/Random", "favicon.ico", "variables.css"],
    "soc": ["Cams & Meetups", "favicon.ico", "variables.css"],
    "s4s": ["Shit 4chan Says", "favicon.ico", "variables.css"],
    # Adult
    "s": ["Beautiful Women", "favicon.ico", "variables.css"],
    "hc": ["Hardcore", "favicon.ico", "variables.css"],
    "hm": ["Handsome Men", "favicon.ico", "variables.css"],
    "h": ["Hentai", "favicon.ico", "variables.css"],
    "e": ["Ecchi", "favicon.ico", "variables.css"],
    "u": ["Yuri", "favicon.ico", "variables.css"],
    "d": ["Hentai/Alternative", "favicon.ico", "variables.css"],
    "y": ["Yaoi", "favicon.ico", "variables.css"],
    "t": ["Torrents", "favicon.ico", "variables.css"],
    "hr": ["High Resolution", "favicon.ico", "variables.css"],
    "gif": ["Adult GIF", "favicon.ico", "variables.css"],
    "aco": ["Adult Cartoons", "favicon.ico", "variables.css"],
    "r": ["Adult Requests", "favicon.ico", "variables.css"],
}


class Params():
    verbose = False
    preserve = False
    total_retries = 5
    total_posts = None
    path_to_download = './'
    use_db = False

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Reply:
    def __init__(self, post):
        self.no = 0
        self.resto = 0
        self.sticky = 0
        self.closed = 0
        self.now = ""
        self.time = 0
        self.name = "Anonymous"
        self.trip = ""
        self.id = ""
        self.capcode = ""
        self.country = "XX"
        self.country_name = ""
        self.troll_country = ""
        self.sub = ""
        self.com = ""
        self.tim = 0
        self.filename = ""
        self.ext = ""
        self.fsize = 0
        self.md5 = ""
        self.w = 0
        self.h = 0
        self.tn_w = 0
        self.tn_h = 0
        self.filedeleted = 0
        self.spoiler = 0
        self.custom_spoiler = 0
        self.replies = 0
        self.images = 0
        self.bumplimit = 0
        self.imagelimit = 0
        self.tag = ""
        self.semantic_url = ""
        self.since4pass = 0
        self.unique_ips = 0
        self.m_img = 0
        self.archived = 0
        self.archived_on = 0
        self.tail_size = 0

        self.img_src = ""
        self.board = ""
        self.custom_id = str(post["no"]) + str(post["time"])
        self.preserved = False

        allowed_keys = list(self.__dict__.keys())

        self.__dict__.update((key, value) for key, value in post.items()
                             if key in allowed_keys)

        # Raise execption on rejected keys
        rejected_keys = set(post.keys()) - set(allowed_keys)
        if rejected_keys:
            print("Warning: invalid reply keys: {}".format(rejected_keys))


class Thread:
    def __init__(self, tid, board, url):
        self.tid = tid
        self.board = board
        self.url = url
        self.set_board()

    def set_board(self):
        self.board_name = boards[self.board][0]
        self.fav = boards[self.board][1]
        self.css = boards[self.board][2]
