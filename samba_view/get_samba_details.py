#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 1
# Section bilgi
# Paylaşılan dosya kullanıcılarını ve kullanıcıların acl bilgilerini getirir
# 1.0
# samba
#
# 3
# Yagiz Kocer
# yagizkocer@gmail.com
# Havelsan
# get_samba_details

import configparser
import json
import sys
import subprocess

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)

SECTION_NAME = sys.argv[2]


def get_shared_users(section_name):
    """ Returns shared users as json according to 'valid users' option in smb.conf """
    
    samba_section_valid_users_dict = {}

    try:
        samba_section_valid_users_dict[section_name] = get_option_value(section_name, 'valid users').split(',')
    except configparser.NoOptionError:
        pass
    except AttributeError:
        pass
    return json.dumps(samba_section_valid_users_dict)


def get_option_value(section_name, option_name):
    """ Takes two str and returns the option as string, exceptions are NoOptionError and NoSectionError"""
   
    return (SAMBA_CONFIG_PARSER.get(section_name, option_name))


def before():
    if not SAMBA_CONFIG_PARSER.has_section(SECTION_NAME):
        print("Section : '{:s}' is not exist".format(SECTION_NAME))
        exit()
    print("ok")

def run():
    print(get_shared_users(SECTION_NAME))

def after():
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
