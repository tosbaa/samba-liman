import configparser
import subprocess
import os
SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_CONFIG_PARSER.read('../smb.conf')


def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def option_exist(section_name, option_name):
    """ Checks section_name(str) and option_name(str) and returns True if option exist """
    return SAMBA_CONFIG_PARSER.has_option(section_name, option_name)


def check_file_exist(file_path):
    """ Takes file_path(str) argument and checks that file exist in given path """
    return os.path.isfile(file_path) 
