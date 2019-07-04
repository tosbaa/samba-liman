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


def remove_valid_user(section_name, user_name):
    users = get_option_value(section_name, "valid users").split(",")
    users_stripped = [user.strip() for user in users]
    users_stripped.remove(user_name)
    print(users_stripped)
    if len(users_stripped) == 0:
        delete_option(section_name, "valid users")
    else:
        after_remove_string = ", ".join(users_stripped)
        sed_script = r"sed -r -i '/^\[%s\]/,/^\[/{s/valid users = .*/valid users = %s/}' %s" % (section_name, after_remove_string, SAMBA_FILE_PATH)
        subprocess.Popen(sed_script, shell=True)


def user_exist(section_name, user_name):
    try:
        already_defined_users = [user.strip() for user in get_option_value(section_name, "valid users").split(",")]
        return user_name in already_defined_users
    except configparser.NoOptionError:
        return True

def delete_option(section_name, option_name):
    ## I use % instead of .format cause /{:s} can not be seen by parser
    sed_script = "sed -i '/^\[%s\]/,/^\[.*$/{/%s.*/d}' %s" % (section_name, option_name, SAMBA_FILE_PATH)
    subprocess.Popen(sed_script, shell=True)


def before():
    if not SAMBA_CONFIG_PARSER.has_section(SECTION_NAME):
        print("Section : '{:s}' is not exist".format(SECTION_NAME))
        exit()
    
    if not user_exist(SECTION_NAME, USER_NAME):
        print("User : {:s} is not defined in config file".format(USER_NAME))
        exit()
    
    if not SAMBA_CONFIG_PARSER.has_option(SECTION_NAME, "valid users"):
        print("Section : '{:s}' has no valid users option".format(SECTION_NAME))
        exit()
    
    print("ok")


def run():
    remove_valid_user(SECTION_NAME, USER_NAME)


def after():
    if user_exist(SECTION_NAME, USER_NAME):
        print("User : '{:s}' couldn't be removed".format(USER_NAME))
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