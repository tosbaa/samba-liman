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


def file_exist(file_path):
    """ Takes file_path(str) argument and checks that file exist in given path """
    
    return os.path.isfile(file_path)


def is_path_duplicate(path):
    """ Checks other sections path, if there is a match, returns an error """

    for section in SAMBA_CONFIG_PARSER.sections():
        try:
            if path == SAMBA_CONFIG_PARSER.get(section, 'path'):
                return True
        except configparser.NoOptionError:
            continue
    return False
