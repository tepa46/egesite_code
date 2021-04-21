from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import os
import json


app = Flask(__name__)


@app.route('/')
def main_page():
    return """
        <p>привет</p>    
        """


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
    # Bot.main()
