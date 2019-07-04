#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 1
# Paylaşılan kullanıcılar
# Dosyanın paylaşıldığı kullanıcıları getirir 
# 1.0
# samba
# section_name:string,file_path:string
# 3
# Yagiz Kocer
# yagizkocer@gmail.com
# Havelsan
# shared_users


import configparser
import json
import sys
import subprocess
import re

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "/etc/samba/smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)
SECTION_NAME = sys.argv[2]
FILE_PATH = sys.argv[3]
PERMISSIONS_PATTERN = "%s([wrx-]{3}).*([wrx-]{3})|%s([wrx-]{3}).*([wrx-]{3})*"
FILE_OWNER_GROUP = {"file" : "# file: ", "owner" : "# owner: " , "group" : "# group: "}
PERMISSIONS_GROUP = {"user_permission" : "user::", "group_permission" : "group::", "other_permission" : "other::"}
USERS_GROUPS_PATTERN = "%s:([wrx-]{3}).*([wrx-]{3})|%s:([wrx-]{3}).*([wrx-]{3})*" 

def get_shared_users(section_name, file_path):
    """ Returns shared users as json according to 'valid users' option in smb.conf """
    
    shared_users_dict = {}

    acl_dict = parse_acl(get_acl(file_path))
    shared_users_dict["name"] = section_name
    acl_extra_users = acl_dict["users"]
    if not SAMBA_CONFIG_PARSER.has_option(section_name, "valid users"):
        shared_users_dict["valid_users"] = None
    else:
        valid_users = get_option_value(section_name, "valid users").split(",")
        user_permission_dict = {}

        for shared_user in valid_users:
            if shared_user in acl_extra_users:
                user_permission_dict[shared_user] = acl_extra_users[shared_user]
            else:
                user_permission_dict[shared_user] = None
        shared_users_dict["valid_users"] = user_permission_dict
    
    shared_users_dict["groups"] = acl_dict["groups"] if "groups" in acl_dict else None
    return json.dumps(shared_users_dict)



    #try:
    #    acl_dict = parse_acl(get_acl(file_path))
    #    shared_users_dict["name"] = section_name
    #    acl_extra_users = [user for user in acl_dict["users"].keys() if "users" in acl_dict]
    #    valid_users_acl = {}
    #    
    #    for shared_user in get_option_value(section_name, 'valid users').split(','):
    #        if shared_user in acl_extra_users:
    #            valid_users_acl[shared_user] = acl_dict["users"][shared_user]
    #        else:
    #            valid_users_acl[shared_user] = None
    #    shared_users_dict["groups"] = acl_dict["groups"] if "groups" in acl_dict else None
    #    shared_users_dict["valid_users"] = valid_users_acl if valid_users_acl else None
    #    

    #except configparser.NoOptionError:
    #    pass
    #except AttributeError:
    #    pass
    #except ValueError:
    #    pass
    #return json.dumps(shared_users_dict)


def get_option_value(section_name, option_name):
    """ Takes two str and returns the option as string, exceptions are NoOptionError and NoSectionError"""
   
    return (SAMBA_CONFIG_PARSER.get(section_name, option_name))


def get_acl(file_path):
    bash_script = "getfacl -p {:s}".format(file_path)
    bash_output = subprocess.Popen(bash_script, shell=True, stdout=subprocess.PIPE).stdout
    acl_string = bash_output.read().decode("utf-8")
    return acl_string

def parse_acl(acl_string):
    acl_dict = {}

    for key, key_pattern in FILE_OWNER_GROUP.items():
        acl_dict[key] = re.search("%s(.*)" % (key_pattern), acl_string).group(1)
    
    for key, key_pattern in PERMISSIONS_GROUP.items():
        match_group = re.search(PERMISSIONS_PATTERN % (key_pattern, key_pattern), acl_string).groups()
        acl_dict[key] = list(filter(lambda match: match != None, match_group))

    users = re.findall("user:([\w\d]+)", acl_string)
    groups = re.findall("group:([\w\d]+)", acl_string)
    
    user_list = {}
    group_list = {}

    for user in users:
        match_group = re.search(USERS_GROUPS_PATTERN % (user, user), acl_string).groups()
        match_group_valid = list(filter(lambda match: match != None, match_group))
        user_list[user] = match_group_valid
    acl_dict["users"] = user_list

    for group in groups:
        match_group = re.search(USERS_GROUPS_PATTERN % (group, group), acl_string).groups()
        match_group_valid = list(filter(lambda match: match != None, match_group))
        group_list[group] = match_group_valid
    acl_dict["groups"] = group_list
    


    for role in ["user", "group", "other"]:
        default_permissions = re.search("default:%s::(.*)" % role, acl_string)
        if default_permissions is not None:
            acl_dict["default_%s" % role] = default_permissions.group(1) 

    mask_match = re.search("mask::(.*)", acl_string)
    if mask_match is not None:
        acl_dict["mask"] = mask_match.group(1)

    default_users = re.findall("default:user:([\d\w]+):", acl_string)
    default_groups = re.findall("default:group:([\d\w]+):", acl_string)

    default_users_list = []
    default_groups_list = []

    for default_user in default_users:
        default_user_permission = re.search("default:user:%s:([wrx-]+)" % default_user, acl_string)
        if default_user_permission is not None:
            default_users_list.append({default_user : default_user_permission.group(1)})        
    if default_users:
        acl_dict["default_users"] = default_users_list 

    for default_group in default_groups:
        default_group_permission = re.search("default:group:%s:([wrx-]+)" % default_group, acl_string)
        if default_group_permission is not None:
            default_groups_list.append({default_group : default_group_permission.group(1)})
    if default_groups:
        acl_dict["default_groups"] = default_groups_list
    return acl_dict


def before():
    if not SAMBA_CONFIG_PARSER.has_section(SECTION_NAME):
        print("Section : '{:s}' is not exist".format(SECTION_NAME))
        exit()
    print("ok")

def run():
    print(get_shared_users(SECTION_NAME, FILE_PATH))

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
