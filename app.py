import os
import json
import time
import glob
from urllib.request import urlretrieve

import yaml
from flask import Flask
from flask import request
from github import Github
from flask import render_template


GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN', '')

app = Flask(__name__, static_url_path='/static')
app.config['FREEZER_DESTINATION'] = 'docs'

g = Github(GITHUB_ACCESS_TOKEN)

def check_pr(pr):
    print(pr)
    files = [file for file in pr.get_files()]
    
    # check number of file
    print(files) 
    if len(files) != 1:
        return False

    # check file status
    print(files[0].status)
    if files[0].status != 'added':
        print(files[0].status)
        return False

    # check filename
    login = pr.user.login 
    filename = files[0].filename.replace("messages/", "")
    login_yml = "{login}.yml".format(login=login)
    if filename != login_yml:
        return False

    # check yaml format
    urlretrieve(files[0].raw_url, filename)
    with open(filename, 'r') as stream:
        try:
            data = yaml.load(stream)
            if not data.get('displayname') or not data.get('message'):
                return False
        except yaml.YAMLError as exc:
            print(exc)
            return False
    os.remove(filename)

    return True

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        payload = json.loads(request.data)
        if payload.get('action') and payload['action'] in ['opened', 'reopened']:
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
