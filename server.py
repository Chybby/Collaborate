#!/usr/bin/env python2.7

from config import *

app = Flask(__name__)

@app.route("/")
def index():
    return 'wob'

if __name__ == "__main__":
    app.run(debug=True)
