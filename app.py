import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Image.create(prompt=animal, n=2, size="1024x1024")
        image_url = response["data"][0]["url"]
        return redirect(image_url)

    result = request.args.get("result")
    return render_template("index.html", result=result)
