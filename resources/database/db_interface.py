import sqlite3


class Database(object):
    __DB_LOCATION = "./chan.db"

    def __init__(self):
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor = self.__connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS boards (
                                    id integer PRIMARY KEY,
                                    board text NOT NULL UNIQUE,
                                    title text NOT NULL,
                                    ws_board integer NOT NULL,
                                    per_page integer NOT NULL,
                                    pages integer NOT NULL,
                                    max_filesize integer NOT NULL,
                                    max_webm_filesize integer NOT NULL,
                                    max_comment_chars integer NOT NULL,
                                    max_webm_duration integer NOT NULL,
                                    bump_limit integer NOT NULL,
                                    image_limit integer NOT NULL,
                                    cooldowns_t integer NOT NULL,
                                    cooldowns_r integer NOT NULL,
                                    cooldowns_i integer NOT NULL,
                                    meta_description text NOT NULL,
                                    spoilers integer,
                                    custom_spoilers integer,
                                    is_archived integer,
                                    troll_flags integer,
                                    country_flags integer,
                                    user_ids integer,
                                    oekai integer,
                                    sjis_tags integer,
                                    code_tags integer,
                                    text_only integer,
                                    forced_anon integer,
                                    webm_audio integer,
                                    require_subject integer,
                                    min_image_width integer,
                                    min_image_height integer
                                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS threads (
                                    custom_id text PRIMARY KEY,
                                    board_id integer NOT NULL,
                                    no integer NOT NULL,
                                    resto integer NOT NULL,
                                    sticky integer,
                                    closed integer,
                                    now text NOT NULL,
                                    time integer NOT NULL,
                                    name text NOT NULL,
                                    trip text,
                                    p_id text,
                                    capcode text,
                                    country text,
                                    country_name text,
                                    troll_country text,
                                    sub text,
                                    com text,
                                    tim integer,
                                    filename text,
                                    ext text,
                                    fsize integer,
                                    md5 text,
                                    w integer,
                                    h integer,
                                    tn_w integer,
                                    tn_h integer,
                                    filedeleted integer,
                                    spoiler integer,
                                    custom_spoiler integer,
                                    replies integer,
                                    images integer,
                                    bumplimit integer,
                                    imagelimit integer,
                                    tag text,
                                    semantic_url text,
                                    since4pass integer,
                                    unique_ips integer,
                                    m_img integer,
                                    archived integer,
                                    archived_on integer,
                                    tail_size integer,
                                    preserved integer,

                                    FOREIGN KEY (board_id)
                                    REFERENCES boards(id)
                                )""")

    def insert_board(self, board):
        sql = '''INSERT OR REPLACE INTO boards (
                    board, title, ws_board, per_page, pages, max_filesize,
                    max_webm_filesize, max_comment_chars, max_webm_duration,
                    bump_limit, image_limit, cooldowns_t, cooldowns_r,
                    cooldowns_i,meta_description, spoilers, custom_spoilers,
                    is_archived, troll_flags, country_flags, user_ids, oekai,
                    sjis_tags,code_tags, text_only, forced_anon, webm_audio,
                    require_subject, min_image_width, min_image_height
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )'''
        self.cursor.execute(sql, board)
        self.__connection.commit()

    def insert_reply(self, reply):
        sql = '''WITH ins (
                    custom_id, no, resto, board, sticky, closed, now, time,
                    name,trip, p_id, capcode, country, country_name,
                    troll_country, sub, com, tim, filename, ext, fsize, md5,
                    w, h, tn_w, tn_h, filedeleted, spoiler, custom_spoiler,
                    replies, images, bumplimit, imagelimit, tag, semantic_url,
                    since4pass, unique_ips, m_img, archived, archived_on,
                    tail_size, preserved
                ) AS (
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?
                    )
                ) INSERT OR REPLACE INTO threads (
                    custom_id, no, resto, board_id, sticky, closed, now, time,
                    name, trip, p_id, capcode, country, country_name,
                    troll_country, sub, com, tim, filename, ext, fsize, md5, w,
                    h, tn_w, tn_h, filedeleted, spoiler, custom_spoiler,
                    replies, images, bumplimit, imagelimit, tag, semantic_url,
                    since4pass, unique_ips, m_img, archived, archived_on,
                    tail_size, preserved
                ) SELECT
                    ins.custom_id, ins.no, ins.resto, boards.id, ins.sticky,
                    ins.closed, ins.now, ins.time, ins.name, ins.trip,
                    ins.p_id, ins.capcode, ins.country, ins.country_name,
                    ins.troll_country, ins.sub, ins.com, ins.tim, ins.filename,
                    ins.ext, ins.fsize, ins.md5, ins.w, ins.h, ins.tn_w,
                    ins.tn_h, ins.filedeleted, ins.spoiler, ins.custom_spoiler,
                    ins.replies, ins.images, ins.bumplimit, ins.imagelimit,
                    ins.tag, ins.semantic_url, ins.since4pass, ins.unique_ips,
                    ins.m_img, ins.archived, ins.archived_on, ins.tail_size,
                    ins.preserved
                FROM boards
                JOIN ins
                ON ins.board = boards.board
                '''
        self.cursor.execute(sql, self.reply_tuple(reply))
        self.__connection.commit()

    def fetch_replies(self, op_no):
        sql = '''
        SELECT * FROM threads WHERE no =?
        UNION
        SELECT * FROM threads WHERE resto=?'''
        self.cursor.execute(sql, (op_no, op_no))
        return self.cursor.fetchall()

    def reply_tuple(self, reply):
        return (reply.custom_id, reply.no, reply.resto, reply.board,
                reply.sticky, reply.closed, reply.now, reply.time,
                reply.name, reply.trip, reply.id, reply.capcode,
                reply.country, reply.country_name, reply.troll_country,
                reply.sub, reply.com, reply.tim, reply.filename,
                reply.ext, reply.fsize, reply.md5, reply.w, reply.h,
                reply.tn_w, reply.tn_h, reply.filedeleted, reply.spoiler,
                reply.custom_spoiler, reply.replies, reply.images,
                reply.bumplimit, reply.imagelimit, reply.tag,
                reply.semantic_url, reply.since4pass, reply.unique_ips,
                reply.m_img, reply.archived, reply.archived_on,
                reply.tail_size, reply.preserved)

    def __del__(self):
        self.__connection.close()
