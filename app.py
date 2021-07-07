import os

from flask import render_template, Flask, send_from_directory
from flask_talisman import Talisman


app = Flask(__name__)
Talisman(app)


@app.route("/", methods=["POST", "GET"])
def home():
    """
    Home route with installable package
    """
    return render_template('index.html')


@app.route("/health", methods=["POST", "GET"])
def health():
    """
    Health check endpoint that wil confirm if the app is healthy
    """
    return "app is healthy"


@app.route('/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(os.getcwd(), filename=filename)

