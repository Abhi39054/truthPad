# encoding : utf-8

# Python Imports

import os
import sys
import json
import re

# Library Imports
from flask import Flask, render_template, request



# Instantiate Flask
app = Flask(__name__)

def get_id():
    path = './files'
    file_path = os.listdir(path)
    if len(file_path) > 0:
        file_list = [int(x.split('.txt')[0]) for x in file_path]
        # print("max = ",max(file_list))
        return int(max(file_list)) + 1
    else:
        return 0


@app.route('/new')
def index():
    return render_template("notepad.html", text_value = "", url_value = "")

@app.route('/submit', methods =["POST"])
def submit():
    
    save_path = './files'

    
    text_data = request.form.get("textarea")
    save_url = request.form.get("save_url")

    # print("text_data = ",text_data)
    # print("save_url = ",save_url)
    # print("save_url = ",request.form['save_url'])

    if save_url == "".strip() or save_url == None:  
        file_id = str(get_id())
        save_url = "http://127.0.0.1:5000"+"/"+file_id
    else:
        file_id = save_url.split('/')[-1]
        if not file_id.isdigit():
            return "url is not correct."
        
    
    with open(os.path.join(save_path,file_id+'.txt'), 'w+') as fp:
        fp.write(text_data)

    return render_template("notepad.html", text_value = text_data, url_value = save_url)

@app.route('/<string:file_id>')
def show(file_id):
    save_path = './files'
    file_data = ""
    with open(os.path.join(save_path,file_id+'.txt'), 'r') as fp:
        file_data = fp.read()
    return render_template("notepad.html", text_value = file_data, url_value = "http://127.0.0.1:5000"+"/"+file_id)


if __name__ == "__main__":
    app.run(debug=True)