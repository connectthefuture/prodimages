#!/usr/bin/env python
# -*- coding: utf-8 -*-

def create_github_repo(localrepodir, password='', reponame=None):
  import requests, json, os
  if not password:
  	password = str(input('Enter your Github password: '))
  if not reponame:
  	reponame = str(input('Enter a Name for the new repo: '))
  github_url = "https://api.github.com/relic7/repos"
  data = json.dumps({'name': reponame, 'description':'repo generated from cmd line for ' + reponame})
  r = requests.post(github_url, data, auth=('relic7', password))
  print r.json()
  return r.json()


if __name__ == '__main__':
  import sys, os
  reponame = ''
  localrepodir = ''
  try:
    localrepodir = sys.argv[1]
    try:
    	reponame = sys.argv[2]
  	except IndexError:
  		pass
  except IndexError:
    localrepodir = os.path.abspath('.')

  create_github_repo(localrepodir, reponame=reponame)
