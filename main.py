import sqlite3 as sq
import random as rnd

with sq.connect('links.db', check_same_thread=False) as db:
    cursor = db.cursor()
    # cursor.execute("""DROP TABLE IF EXISTS shorted_links""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS shorted_links (
        url TEXT,
        token TEXT,
        number_of_transitions INTEGER DEFAULT 0   
        )""")


class Link_shortening:
    __token_length = 8

    def __init__(self, domain):
        self.domain = domain

    def __generate_token(self):
        token = ''
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        token += rnd.choice(alphabet[10:]) + ''.join([rnd.choice(alphabet) for _ in range(self.__token_length - 1)])
        return token

    def check_in_db(self, short_url):
        with sq.connect('links.db', check_same_thread=False) as db:
            cursor = db.cursor()
            url = cursor.execute(f"""SELECT url FROM shorted_links WHERE token='{short_url}'""").fetchone()
            if url is not None:
                cursor.execute(
                    f"""UPDATE shorted_links SET number_of_transitions = number_of_transitions + 1 WHERE token = '{short_url}'""")
            return cursor.execute(f"""SELECT url FROM shorted_links WHERE token='{short_url}'""").fetchone()

    def record_in_db(self, url):

        with sq.connect('links.db', check_same_thread=False) as db:
            cursor = db.cursor()

            token_new = self.__generate_token()

            if cursor.execute(f"""SELECT * FROM shorted_links WHERE url = '{url}'""").fetchone() is None:
                while not cursor.execute(
                        f"""SELECT * FROM shorted_links WHERE token = '{token_new}'""").fetchone() is None:
                    token_new = self.__generate_token()
                cursor.execute(f"""INSERT INTO shorted_links (url, token) VALUES ('{url}', '{token_new}')""")
                db.commit()

            else:
                token_new = cursor.execute(f"""SELECT token FROM shorted_links WHERE url = '{url}'""").fetchone()[0]

        return f'{self.domain}/{token_new}'
