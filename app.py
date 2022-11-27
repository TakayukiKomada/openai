import os
import pprint
import time
import numpy as np
import urllib.error
import urllib.request
from PIL import Image
import openai
from flask import Flask, redirect, render_template, request, url_for
from time import sleep
import random
import io
from io import BytesIO
import cv2
from config import Image2

BASE_PATH = "static/image/"
app = Flask(__name__)

x_list = []
y_list = []


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


@app.route("/")
def index():
    # IMG_LIST = os.listdir("static/image")
    # IMG_LIST = ["image/" + i for i in IMG_LIST]
    # return render_template("index.html", imagelist=IMG_LIST)

    query = Image2.select()
    query_result = query.execute()
    return render_template("index.html", imagelist=query_result)


@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        search = request.form["search"]
        imagelist = Image2.select().where(Image2.name.contains(search))
        IMG_LIST = os.listdir("static/image")
        IMG_LIST = ["image/" + i for i in IMG_LIST]
        return render_template("search.html", imagelist=imagelist)


@app.route("/update", methods=("GET", "POST"))
def update():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Image.create(prompt=animal, n=1, size="512x512")
        image_url = response["data"][0]["url"]
        # 画像データを取得する
        img_in = urllib.request.urlopen(image_url).read()
        img_bin = io.BytesIO(img_in)
        # Pillowで開き、画像を保存する
        img = Image.open(img_bin)
        animal2 = random.sample(range(10000), 1)
        sleep(10)
        img.save(f"static/image/imagesout_color_{animal}{animal2}.png", "PNG")
        file_name = f"imagesout_color_{animal}{animal2}.png"
        image = BASE_PATH + file_name
        Image2.create(
            name=animal,
            image=image,
        )

        return redirect(url_for("update", result=image_url, imageUrl=image))

    result = request.args.get("result")
    imageUrl = request.args.get("imageUrl")
    return render_template("update.html", result=result, image=imageUrl)


@app.route("/variation", methods=("GET", "POST"))
def variation():
    if request.method == "POST":
        name = request.form["name"]
        image = request.form["imageUrl"]
        response = openai.Image.create_variation(
            image=open(image, "rb"), n=1, size="512x512"
        )
        image_url = response["data"][0]["url"]
        # 画像データを取得する
        img_in = urllib.request.urlopen(image_url).read()
        img_bin = io.BytesIO(img_in)
        # Pillowで開き、画像を保存する
        img = Image.open(img_bin)
        animal2 = random.sample(range(10000), 1)
        sleep(10)
        img.save(f"static/image/imagesout_color_{name}{animal2}.png", "PNG")
        file_name = f"imagesout_color_{name}{animal2}.png"
        image = BASE_PATH + file_name
        Image2.create(
            name=name,
            image=image,
        )
        return redirect(
            url_for("variation", result=image_url, imageUrl=image, name=name)
        )

    result = request.args.get("result")
    imageUrl = request.args.get("imageUrl")
    name = request.args.get("name")

    return render_template("variation.html", result=result, image=imageUrl, name=name)


@app.route("/variationid/<id>", methods=("GET", "POST"))
def variationid(id):
    if request.method == "POST":
        img = Image2.get(id=id)
        name = img.name
        response = openai.Image.create_variation(
            image=open(img.image, "rb"), n=1, size="512x512"
        )
        image_url = response["data"][0]["url"]
        img_in = urllib.request.urlopen(image_url).read()
        img_bin = io.BytesIO(img_in)
        # Pillowで開き、画像を保存する
        img2 = Image.open(img_bin)
        animal2 = random.sample(range(10000), 1)
        sleep(10)
        img2.save(f"static/image/imagesout_color_{name}{animal2}.png", "PNG")
        file_name = f"imagesout_color_{name}{animal2}.png"
        image = BASE_PATH + file_name
        Image2.create(
            name=name,
            image=image,
        )
        return redirect(url_for("variationid", result=image_url))
    result = request.args.get("result")
    imageUrl = request.args.get("image")
    return render_template("variationid.html", result=result, image=imageUrl)


# This is the BytesIO object that contains your image data

# @app.route("/tweak", methods=("GET", "POST"))
# def tweak():
# # This is the BytesIO object that contains your image data
#     byte_stream: BytesIO = [your image data]
#     byte_array = byte_stream.getvalue()
#     response = openai.Image.create_variation(
#     image=byte_array,
#     n=1,
#     size="512x512"
#     )

# # 出力先のパスを生成
# @app.route("/edit", methods=("GET", "POST"))
# def onMouse(event, x, y, flags, params):
#     if len(x_list) == 2:
#         event = ""
#     elif event == cv2.EVENT_LBUTTONDOWN:
#         x_list.append(x)
#         y_list.append(y)

#     img = cv2.imread("static/image/man.png")

#     # 画像を表示させる
#     cv2.imshow("face", img)

#     # クリックした際にonMouse関数が発火
#     cv2.setMouseCallback("face", img)
#     # bgr -> rgb
#     rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     # マスク画像の生成（マスク画像をかけたい画像サイズと同じ）
#     mask = np.zeros(rgb.shape, dtype=np.uint8)

#     cv2.rectangle(
#         mask,
#         (x_list[0], y_list[0]),
#         (x_list[1], y_list[1]),
#         (255, 255, 255),
#         -1,
#     )
# 画像の合成
# rgb_and = cv2.bitwise_and(rgb, mask)
# # 画像の表示
# imgShow(rgb_and)
# # waitKey(0)で画像上で何かしらのキーを押せば閉じられるようにする
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# openai.Image.create_edit(
#     image1=open('static/image/man.png', "rb"),
#     mask=open("mask.png", "rb"),
#     prompt="A cute baby sea otter wearing a beret",
#     n=1,
#     size="1024x1024"
# )
# image_url2 = response["data"][0]["url"]
# with urllib.request.urlopen(image_url2) as web_file:
#         image = Image.open(web_file)
#         sleep(10)
#         animal2 = random.sample(range(10000), 1)
#         image.save(f"static/image/imagesout_color_{animal2}.png")

# result = request.args.get("result")
# return render_template("edit.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
