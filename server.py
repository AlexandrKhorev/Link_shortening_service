from main import *
from flask import Flask, request, redirect, abort

import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--base-url")

base_url = parser.parse_args().base_url
base_host, base_port = split_link(base_url)

ls = Link_shortening(base_url)

app = Flask(__name__)


@app.route("/")
def index():
    return "Link shortening service"


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
    return redirect(f"{url[0]}")


@app.errorhandler(404)
def not_found(error):
    return {
               "error": "Not found"
           }, 404


if __name__ == '__main__':
    app.run(debug=True, host=base_host, port=base_port)
