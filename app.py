from flask import Flask, render_template, redirect, request, url_for
import pymysql
import json
from blueprints.bilisearch import bp as bili_bp
app = Flask(__name__)


# @app.route('/result/?<string:search>', methods=['GET'])
# def result(search):
#     return search
app.register_blueprint(bili_bp)


if __name__ == '__main__':
    app.run()
