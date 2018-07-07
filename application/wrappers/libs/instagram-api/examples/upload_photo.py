#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

InstagramAPI = InstagramAPI("tomisin10", "gooder")
InstagramAPI.login()  # login

photo_path = '/home/tomisin/Pictures/Screenshot from 2018-03-11 22-46-40.jpg'
caption = "Sample photo"
InstagramAPI.uploadPhoto(photo_path, caption=caption)
