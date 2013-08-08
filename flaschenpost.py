# Flaschenpost - a small and simple blog
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/Flaschenpost

import StringIO
import os

from flask import Flask, abort, render_template
from asciidocapi import AsciiDocAPI, AsciiDocError

site = Flask(__name__)
site.config.from_object(__name__)

asciidoc = AsciiDocAPI()


def index_posts(dir):
    return map(lambda x: os.path.splitext(x)[0], filter(
        lambda x: x.endswith(".txt"), os.listdir(dir)))


@site.route("/")
def index():
    return "Nothing to see here, move along"


@site.route("/post/")
def serve_post_index():
    dir = site.config.get("POST_DIR", ".")
    return render_template("post_index.html", posts=index_posts(dir))


@site.route("/post/<title>")
def serve_post(title):
    title = title.encode()
    file = ".".join([title, "txt"])
    if not os.path.isfile(file):
        abort(404)
    out = StringIO.StringIO()
    try:
        # TODO: cache generated files
        asciidoc.execute(file, out)
    except AsciiDocError:
        abort(500)
    return out.getvalue()


if __name__ == "__main__":
    site.run(debug=True)
