import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os

url = os.getenv("STORAGE_BUCKET")

# credentials.jsonのパスを指定
credFilePath = "credentials.json"
# キーファイルの認証
cred = credentials.Certificate(credFilePath)
default_app = firebase_admin.initialize_app(cred)


# 第一引数に確認したバケットのurl(gs://以降のもの)、第二引数に上記で指定したdefault_app
bucket = storage.bucket(url, default_app)
# ローカル環境のアップロードしたい画像のパスを指定
blob = bucket.blob("../static/image/imagesout_color.png")
# Storage上のアップロード先を指定
blob.upload_from_filename("../static/image/imagesout_color.png")
