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

from flask import Flask, abort
from asciidocapi import AsciiDocAPI, AsciiDocError

site = Flask(__name__)

asciidoc = AsciiDocAPI()


@site.route("/")
def index():
    return "Nothing to see here, move along"


@site.route("/post/<title>")
def serve_post(title):
    title = title.encode()
    file = ".".join([title, "txt"])
    if not os.path.isfile(file):
        abort(404)
    out = StringIO.StringIO()
    try:
        asciidoc.execute(file, out)
    except AsciiDocError:
        abort(500)
    return out.getvalue()


if __name__ == "__main__":
    site.run(debug=True)
