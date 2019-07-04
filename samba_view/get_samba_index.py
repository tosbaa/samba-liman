#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 1
# Samba bilgi
# Sambada paylasılan dosyanın bilgilerini getirir
# 1.0
# samba
#
# 3
# Yagiz Kocer
# yagizkocer@gmail.com
# Havelsan
# get_samba_index

import configparser
import json
import sys
import subprocess
from os import stat, path
from pwd import getpwuid

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../samba_view"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)
IGNORED_SECTIONS = ["global", "printers", "homes", "print$"]


def get_samba_index():
    shared_files_dict = {}
    for section in SAMBA_CONFIG_PARSER.sections():
        if not section in IGNORED_SECTIONS:
            section_dict = {}
            file_path = SAMBA_CONFIG_PARSER.get(section, "path")
            file_info = stat(file_path)
            section_dict["owner"] = getpwuid(file_info.st_uid).pw_name
            section_dict["size"] = file_info.st_size
            section_dict["path"] = file_path
            shared_files_dict[section] = section_dict
    return json.dumps(shared_files_dict) 


def before():
    if not path.isfile(SAMBA_FILE_PATH):
        print("Samba config file not found on : {:s}".format(SAMBA_FILE_PATH))
        exit()
    print("ok")


def run():
    print(get_samba_index())


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