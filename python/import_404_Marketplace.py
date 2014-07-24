#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,sqlalchemy,glob


badurldir = '/mnt/Post_Complete/Complete_Archive/MARKETPLACE/ERRORS/'
errorfiles = glob.glob(os.path.join(os.path.abspath(badurldir), '*.txt')
