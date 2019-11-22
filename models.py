boards = {
    #Japanese Culture
    "a" : ["Anime & Manga", "favicon-ws.ico", "styles-ws.css"],
    "c" : ["Anime/Cute", "favicon-ws.ico", "styles-ws.css"],
    "w" : ["Anime/Wallpapers", "favicon-ws.ico", "styles-ws.css"],
    "m" : ["Mecha", "favicon-ws.ico", "styles-ws.css"],
    "cgl" : ["Cosplay & EGL", "favicon-ws.ico", "styles-ws.css"],
    "cm" : ["Cute/Male", "favicon-ws.ico", "styles-ws.css"],
    "f" : ["Flash", "favicon.ico", "styles.css"],
    "n" : ["Transportation", "favicon-ws.ico", "styles-ws.css"],
    "jp" : ["Otaku Culture", "favicon-ws.ico", "styles-ws.css"], 
    #Video Games
    "v" : ["Video Games", "favicon-ws.ico", "styles-ws.css"],
    "vg" : ["Video Games Generals", "favicon-ws.ico", "styles-ws.css"],
    "vp" : ["Pokemon", "favicon-ws.ico", "styles-ws.css"],
    "vr" : ["Retro Games", "favicon-ws.ico", "styles-ws.css"],
    #Interests
    "co" : ["Comics & Cartoons", "favicon-ws.ico", "styles-ws.css"],
    "g" : ["Technology", "favicon-ws.ico", "styles-ws.css"],
    "tv" : ["Television & Film", "favicon-ws.ico", "styles-ws.css"],
    "k" : ["Weapons", "favicon-ws.ico", "styles-ws.css"],
    "o" : ["Auto", "favicon-ws.ico", "styles-ws.css"],
    "an" : ["Animals & Nature", "favicon-ws.ico", "styles-ws.css"],
    "tg" : ["Traditional Games", "favicon-ws.ico", "styles-ws.css"],
    "sp" : ["Sports", "favicon-ws.ico", "styles-ws.css"],
    "asp" : ["Alternative Sports", "favicon-ws.ico", "styles-ws.css"],
    "sci" : ["Science & Math", "favicon-ws.ico", "styles-ws.css"],
    "his" : ["History & Humanities", "favicon-ws-ico", "styles-ws.css"],
    "int" : ["International",  "favicon-ws.ico", "styles-ws.css"],
    "out" : ["Outdoors", "favicon-ws.ico", "styles-ws.css"],
    "toy" : ["Toys", "favicon-ws.ico", "styles-ws.css"],
    #Creative 
    "i" : ["Oekaki", "favicon.ico", "styles.css"],
    "po" : ["Papercraft & Origami", "favicon-ws.ico", "styles-ws.css"],
    "p" : ["Photography", "favicon-ws.ico", "styles-ws.css"],
    "ck" : ["Food & Cooking", "favicon-ws.ico", "styles-ws.css"],
    "ic" : ["Artwork/Critique", "favicon.ico", "styles.css"],
    "wg" : ["Wallpapers/General", "favicon.ico", "styles.css"],
    "lit" : ["Literature", "favicon-ws.ico", "styles-ws.css"],
    "mu" : ["Music", "favicon-ws.ico", "styles-ws.css"],
    "fa" : ["Fashion", "favicon-ws.ico", "styles-ws.css"],
    "3" : ["3DCG", "favicon-ws.ico", "styles-ws.css"],
    "gd" : ["Graphic Design", "favicon-ws.ico", "styles-ws.css"],
    "diy" : ["Do-It-Yourself", "favicon-ws.ico", "styles-ws.css"],
    "wsg" : ["Worksafe GIF", "favicon-ws.ico", "styles-ws.css"],
    "qst" : ["Quests",  "favicon-ws.ico", "styles-ws.css"],
    #Other
    "biz" : ["Business & Finance", "favicon-ws.ico", "styles-ws.css"],
    "trv" : ["Travel", "favicon-ws.ico", "styles-ws.css"],
    "fit" : ["Fitness", "favicon-ws.ico", "styles-ws.css"],
    "x" : ["Paranormal", "favicon-ws.ico", "styles-ws.css"],
    "adv" : ["Advice","favicon-ws.ico", "styles-ws.css"],
    "lgbt" : ["LGBT", "favicon-ws.ico", "styles-ws.css"],
    "mlp" : ["Pony", "favicon-ws.ico", "styles-ws.css"],
    "news" : ["Current News", "favicon-ws.ico", "styles-ws.css"],
    "wsr" : ["Worksafe Requests", "favicon-ws.ico", "styles-ws.css"],
    "vip" : ["Very Important Posts", "favicon-ws.ico", "styles-ws.css"],
    #Misc.
    "b" : ["Random", "favicon.ico", "styles.css"],
    "r9k" : ["ROBOT9001", "favicon.ico", "styles.css"],
    "pol" : ["Politically Incorrect", "favicon.ico", "styles.css"],
    "bant" : ["International/Random", "favicon.ico", "styles.css"],
    "soc" : ["Cams & Meetups", "favicon.ico", "styles.css"], 
    "s4s" : ["Shit 4chan Says", "favicon.ico", "styles.css"],
    #Adult
    "s" : ["Beautiful Women", "favicon.ico", "styles.css"],
    "hc" : ["Hardcore", "favicon.ico", "styles.css"],
    "hm" : ["Handsome Men", "favicon.ico", "styles.css"],
    "h" : ["Hentai", "favicon.ico", "styles.css"],
    "e" : ["Ecchi", "favicon.ico", "styles.css"],
    "u" : ["Yuri", "favicon.ico", "styles.css"],
    "d" : ["Hentai/Alternative", "favicon.ico", "styles.css"],
    "y" : ["Yaoi", "favicon.ico", "styles.css"],
    "t" : ["Torrents", "favicon.ico", "styles.css"],
    "hr" : ["High Resolution", "favicon.ico", "styles.css"],
    "gif" : ["Adult GIF", "favicon.ico", "styles.css"],
    "aco" : ["Adult Cartoons", "favicon.ico", "styles.css"],
    "r" : ["Adult Requests", "favicon.ico", "styles.css"],
}

class Reply:
    def __init__(self, name, date, message, pid, img_src=None, img_text=None, subject=None):
        self.name = name
        self.date = date
        self.message = message
        self.pid = pid
        self.img_src = img_src
        self.img_text = img_text
        self.subject = subject
        self.is_img = False
        self.is_webm = False
        self.set_conditionals()
    
    def set_conditionals(self):
        if (self.img_src != ""):
            if (self.img_src[-4:] == 'webm'):
                self.is_webm = True
            else:
                self.is_img = True

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