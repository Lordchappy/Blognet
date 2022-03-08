from flask import request
import os

from flask_restful import abort
from flaskblog import app,Cloud


def  media(form,post):
    file_names =[]
    files = request.files.getlist(form.files_upload.name)
    for num,file in enumerate(files):
        saved_media =  Cloud.upload(file)
        file_names.append(saved_media["secure_url"])     
    return file_names


def delete_post_images(files):
    for image_url in files:
        public_id = image_url.split(".")[2].split("/")[-1]
        if public_id != "default_xfjzu9":
            Cloud.destroy(public_id)