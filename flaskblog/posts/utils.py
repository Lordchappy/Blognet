from flask import request
import os
from flaskblog import app,Cloud


def  media(form,post):
    file_names =[]
    files = request.files.getlist(form.files_upload.name)
    for num,file in enumerate(files):
        _, ext = os.path.splitext(file.filename)
        filename = "Post{}-{}{}".format(post.id,str(num),str(ext).lower())
        file.save(os.path.join(app.root_path, 'static/imagefolder', filename))
        saved_media =  Cloud.upload(os.path.join(app.root_path, 'static/imagefolder', filename))
        file_names.append(saved_media["secure_url"])
        os.remove(os.path.join(app.root_path, 'static/imagefolder', filename))           
    return file_names


def delete_post_images(files):
    for image_url in files:
        public_id = image_url.split(".")[2].split("/")[-1]
        if public_id != "default_xfjzu9":
            Cloud.destroy(public_id)