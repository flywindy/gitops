import os
import json
import time
import glob

import yaml
from flask import Flask
from flask import request
from github import Github
from flask import render_template


GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN', '')

app = Flask(__name__)
g = Github(GITHUB_ACCESS_TOKEN)

def check_pr(pr):
    files = [file for file in pr.get_files()]
    print(files)
    if len(files) != 1:
        return False

    print(files[0].status)
    if files[0].status != 'added':
        print(files[0].status)
        return False

    login = pr.user.login 
    filename = files[0].filename
    login_yml = "{login}.yml".format(login=login)
    print(login_yml)
    print(filename.replace("messages/", ""))

    if filename.replace("messages/", "") == login_yml:
        return False

    return True

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        payload = json.loads(request.data)
        if payload['action'] == 'opened' or payload['action'] == 'reopened':
            repo = g.get_repo(payload['repository']['id'])
            pr_number = payload['number']
            pr = repo.get_pull(pr_number)
            if check_pr(pr):
                pr.as_issue().create_comment('This is good.')
                pr.merge()
            else:
                pr.as_issue().create_comment('Something wrong.')
            return ''

    messages = []
    for f in glob.glob("messages/*.yml"):
        with open(f, 'r') as stream:
            data = yaml.load(stream)
            try:
                messages.append({
                    'message': data['message'],
                    'display_name': data['displayname']
                })
            except yaml.YAMLError as exc:
                print(exc)

    return render_template('index.html', messages=messages)
