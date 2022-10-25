from flask import redirect, render_template, request, request_started
from app import app

class Main:
    @app.route("/")
    def index():
        return render_template('index.html')