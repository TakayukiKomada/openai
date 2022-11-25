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
import cv2


app = Flask(__name__)

x_list = []
y_list = []


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update", methods=("GET", "POST"))
def update():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Image.create(prompt=animal, n=1, size="1024x1024")
        image_url = response["data"][0]["url"]
        with urllib.request.urlopen(image_url) as web_file:
            image = Image.open(web_file)
            sleep(10)
            animal2 = random.sample(range(10000), 1)
            image.save(f"static/image/imagesout_color_{animal}{animal2}.png")
            # web_file.save(static/images/imagesout_color.png)

        return redirect(url_for("update", result=image_url))

    result = request.args.get("result")
    return render_template("update.html", result=result)


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
    rgb_and = cv2.bitwise_and(rgb, mask)
    # 画像の表示
    imgShow(rgb_and)
    # waitKey(0)で画像上で何かしらのキーを押せば閉じられるようにする
    cv2.waitKey(0)
    cv2.destroyAllWindows()
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
