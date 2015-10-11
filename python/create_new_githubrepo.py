#!/usr/bin/env python
# -*- coding: utf-8 -*-


def create_github_repo(localrepodir, password=-None):
  import requests, json, os
  reponame = os.path.abspath(localrepodir).split('/')[-1]
  github_url = "https://api.github.com/relic7/repos"
  data = json.dumps({'name': reponame, 'description':'repo generated from cmd line for ' + reponame})
  r = requests.post(github_url, data, auth=('relic7', password))
  print r.json



if __name == '__main__':
  import sys, os
  try:
    localrepodir = sys.argv[1]
  except IndexError:
    localrepodir = os.path.abspath('.')

  create_github_repo(localrepodir)
