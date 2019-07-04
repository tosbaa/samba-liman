#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 1
# Paylaşılan dosyadan user sil 
# Verilen kullanıcı samba paylaşımından çıkarılır
# 1.0
# samba
#
# 3
# Yagiz Kocer
# yagizkocer@gmail.com
# Havelsan
# remove_valid_user

import configparser
import json
import sys
import subprocess
import re

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)
SECTION_NAME = sys.argv[2]
USER_NAME = sys.argv[3]

def get_option_value(section_name, option_name):
    """ Takes two str and returns the option as string, exceptions are NoOptionError and NoSectionError"""
   
    return (SAMBA_CONFIG_PARSER.get(section_name, option_name))


def remove_valid_user(section_name, user_name)