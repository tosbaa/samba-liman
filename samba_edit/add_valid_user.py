#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 1
# User ile dosya paylaş 
# Verilen kullanıcı samba paylaşımına eklenir 
# 1.0
# samba
#
# 3
# Yagiz Kocer
# yagizkocer@gmail.com
# Havelsan
# add_valid_user

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

def add_user(section_name, user_name):
    if not SAMBA_CONFIG_PARSER.has_option(section_name, "valid users"):
        add_option(section_name, "valid users", user_name)
    else:
        sed_script = r"sed -r -i '/^\[%s\]/,/^\[/{s/(^valid users = .*)/\1, %s/}' %s" % (section_name, user_name, SAMBA_FILE_PATH)
        subprocess.Popen(sed_script, shell=True)

def user_exist(section_name, user_name):
    try:
        already_defined_users = [user.strip() for user in get_option_value(section_name, "valid users").split(",")]
        print(already_defined_users)
        return user_name in already_defined_users
    except configparser.NoOptionError:
        return True

def add_option(section_name, option_name, value):
   sed_script = "sed -i '/\[{:s}\]/a {:s} \= {:s}' {:s}".format(section_name, option_name, value, SAMBA_FILE_PATH)
   subprocess.Popen(sed_script, shell=True)

def before():
    if not SAMBA_CONFIG_PARSER.has_section(SECTION_NAME):
        print("Section name : '{:s}' not exist".format(SECTION_NAME))
        exit()
    if user_exist(SECTION_NAME, USER_NAME):
        print("User : '{:s}' already in valid users".format(USER_NAME))
        exit()
    print("ok")

def run():
    add_user(SECTION_NAME, USER_NAME)

def after():
    if not user_exist(SECTION_NAME, USER_NAME):
        print("User: {:s} can not be added".format(USER_NAME))
        exit()
    print("ok")

def automate():
    before_output = make_bash_call('before')
    if before_output != "ok\n":
        print(before_output)
        exit()
    print('before ok')

    make_bash_call('run')    

    after_output = make_bash_call('after')
    if after_output != 'ok\n':
        print(after_output)
        exit()
    print('after ok')


def make_bash_call(stage_name):
    bash = ['python3.7', __file__, stage_name, sys.argv[2], sys.argv[3]]
    output = subprocess.Popen(bash, stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8')


if __name__ == "__main__":
   globals()[sys.argv[1]]()