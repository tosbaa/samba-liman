import configparser
import json
import sys
import subprocess

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)

SECTION_NAME = sys.argv[2]
OPTION_NAME = sys.argv[3]



def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def option_exist(section_name, option_name):
    """ Checks section_name(str) and option_name(str) and returns True if option exist """

    return SAMBA_CONFIG_PARSER.has_option(section_name, option_name)


def get_option_value(section_name, option_name):
    """ Takes two str and returns the option as string, exceptions are NoOptionError and NoSectionError"""
   
    return json.dumps(SAMBA_CONFIG_PARSER.get(section_name, option_name))


def before():
    if not section_exist(SECTION_NAME):
        print("Section : '{:s}' is not exist".format(SECTION_NAME))
        exit()
    if not option_exist(SECTION_NAME, OPTION_NAME):
        print("Option : '{:s}' is not exist".format(OPTION_NAME))
    
    print("ok")


def run():
    print(get_option_value(SECTION_NAME, OPTION_NAME))


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
