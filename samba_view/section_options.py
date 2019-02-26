import configparser
import json
import sys
import subprocess

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)

SECTION_NAME = sys.argv[2]


def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def get_section_with_options(section_name):
    """ Takes section name(str) and returns section with option=value keys as json """
    section_dict = {}
    option_value = {}
    
    for option, value in SAMBA_CONFIG_PARSER.items(section_name):
        option_value[option] = value
    
    section_dict[section_name] = option_value
    
    return json.dumps(section_dict)


def before():
    if not section_exist(SECTION_NAME):
        print("Section : '{:s}' not exist".format(SECTION_NAME))
        exit()
    
    print("ok")

def run():
    print(get_section_with_options(SECTION_NAME))

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
    bash = ['python3.7', __file__, stage_name, sys.argv[2]]
    output = subprocess.Popen(bash, stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8')



if __name__ == "__main__":
   globals()[sys.argv[1]]()