# import cv2
# import openai
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY")
# x_list = []
# y_list = []


# def imgShow(imgList, row_num=1):
#     img_num = len(imgList)
#     # Matplotlibでグラフを描く際の基本パーツとしてFigureとAxesがあります。

#     # Figure：描画領域全体
#     # Axes：一つ一つのプロットを描く領域（座標軸）
#     if img_num == 1:
#         fig = plt.figure()
#         ax = fig.add_subplot(111)
#         ax.imshow(imgList[0])

#     else:
#         fig, axes = plt.subplots(row_num, round(img_num / row_num))
#         ax = axes.ravel()
#         for i in range(img_num):
#             ax[i].imshow(imgList[i])
#             ax[i].set_xticks([])
#             ax[i].set_yticks([])

#     plt.show()


# img = cv2.imread("static/image/man.png")
# rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # マスク画像の生成（マスク画像をかけたい画像サイズと同じ）
# mask = np.zeros(rgb.shape, dtype=np.uint8)
# cv2.rectangle(
#     rgb,
#     (255, 126),
#     (377, 296),
#     (255, 255, 255),
#     -1,
# )
# imgShow([rgb])
# cv2.imwrite("static/image/rgb.png", rgb)
# url = "static/image/rgb.png"
# response = openai.Image.create_edit(
#     image=open("static/image/man.png", "rb"),
#     mask=open(url, "rb"),
#     prompt="A sunlit indoor lounge area with a pool containing a flamingo",
#     n=1,
#     size="512x512",
# )
# image_url = response["data"][0]["url"]


# def onMouse(event, x, y, flags, params):
#     if len(x_list) == 2:
#         event = ""
#         # bgr -> rgb
#         rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         # マスク画像の生成（マスク画像をかけたい画像サイズと同じ）
#         mask = np.zeros(rgb.shape, dtype=np.uint8)
#         cv2.rectangle(
#             rgb,
#             (x_list[0], y_list[0]),
#             (x_list[1], y_list[1]),
#             (255, 255, 255),
#             -1,
#         )
#         # 画像の合成
#         rgb_and = cv2.bitwise_and(rgb, mask)
#         # 画像の表示
#         imgShow(rgb_and)
#     # waitKey(0)で画像上で何かしらのキーを押せば閉じられるようにする
#     elif event == cv2.EVENT_LBUTTONDOWN:
#         x_list.append(x)
#         y_list.append(y)
#         print(x_list, y_list)


# # 画像を表示させる
# cv2.imshow("face", img)
# # クリックした際にonMouse関数が発火
# cv2.setMouseCallback("face", onMouse)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
