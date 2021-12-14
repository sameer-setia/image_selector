import os
import datetime
import shutil
import json
import glob
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)
cwd = os.getcwd()
today = str(datetime.date.today())
app.static_url_path = os.environ.get("SOURCE_FOLDER")
app.static_folder = os.environ.get("SOURCE_FOLDER")
if not os.path.isdir(cwd + "/images"):
    os.mkdir(cwd + "/images")

if not os.path.isdir(cwd + "/images/"+today):
    os.mkdir(cwd + "/images/"+today)
    os.mkdir(cwd + "/images/"+today+"/Daffodil")
    os.mkdir(cwd + "/images/"+today+"/G-eng")


result = list(Path(os.environ.get("SOURCE_FOLDER")).rglob("*.[jJ][pP][gG]"))
d = {}
d1 = {}
d2 = {}
total_done = len(glob.glob(cwd + "/images/"+today+"/*/*.jpg"))
with open("done.json", 'r') as f:
    d1 = json.load(f)
for i in result:
    full_path = str(i)
    img_path = full_path.replace(app.static_folder + '/', "")
    image = str(i).split("/")[-1]
    if image not in d1:
        d2[img_path] = full_path
        d[image] = img_path
images = list(d.values())
images.sort()


@app.route('/')
def home():
    if len(images) == 0:
        return 'no images available to review'
    full_filename = images[0]
    return render_template("index.html", user_image=full_filename, count=total_done)


@app.route('/daffodil')
def daffodil():
    tmp = images.pop(0)
    d1[tmp.split('/')[-1]] = True
    with open("done.json", "w") as file:
        json.dump(d1, file)
    shutil.copy(d2[tmp], cwd + "/images/"+today+"/Daffodil")
    global total_done
    total_done += 1
    return home()


@app.route('/no/')
def no():
    tmp = images.pop(0)
    d1[tmp.split('/')[-1]] = True
    with open("done.json", "w") as file:
        json.dump(d1, file)
    if len(images) == 0:
        return 'no images available to review'
    return home()


@app.route('/g-eng/')
def g_eng():
    tmp = images.pop(0)
    d1[tmp.split('/')[-1]] = True
    with open("done.json", "w") as file:
        json.dump(d1, file)
    shutil.copy(d2[tmp], cwd + "/images/"+today+"/G-eng")
    if len(images) == 0:
        return 'no images available to review'
    global total_done
    total_done += 1
    return home()
