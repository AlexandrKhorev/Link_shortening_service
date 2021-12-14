from flask import Flask, request, redirect, abort
from main import *

ls = Link_shortening('http://localhost:5000')

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/_short", methods=['POST'])
def parse_link():
    url = request.get_json()['url']
    short_link = ls.record_in_db(url)

    return {
        'shorten': short_link
    }


@app.route('/<path>', methods=['GET'])
def verify(path):
    url = ls.check_in_db(path)
    if url is None:
        return abort(404)
    print(url[0])
    return redirect(f"{url[0]}")


@app.errorhandler(404)
def not_found(error):
    return {
               "error": "Not found"
           }, 404

# 'https://www.site.com/with/long/url?and=param'
# 'https://www.youtube.com/watch?v=LcZ9uJn8ffA&ab_channel=%D0%98%D0%98%D0%9A%D0%A1%D0%9D%D0%98%D0%AF%D0%A3%D0%9C%D0%98%D0%A4%D0%98'
# 'https://vk.com/im?peers=-98563228_58897273_66775147_30462151_25635087_85953708_85378153'
# 'https://yandex.ru/search/?text=flask+start+server&lr=47'
# 'https://hashids.org/python/'
# 'https://www.site.com/with/long/url?and=param'
# 'https://yandex.ru/search/?text=flask+start+server&lr=47'
