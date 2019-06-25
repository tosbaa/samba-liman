import sys
import configparser
import os
import subprocess
SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = '../smb.conf'
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)

SECTION_NAME = sys.argv[2]
OPTION_NAME = sys.argv[3]
VALUE = sys.argv[4]

def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def option_exist(section_name, option_name):
    """ Checks section_name(str) and option_name(str) and returns True if option exist """
    
    return SAMBA_CONFIG_PARSER.has_option(section_name, option_name)


def make_bash_call(stage_name):
    bash = ['python3.7', __file__, stage_name, sys.argv[2], sys.argv[3], sys.argv[4]]
    output = subprocess.Popen(bash, stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8')


def get_option_value(section_name, option_name):
    return SAMBA_CONFIG_PARSER.get(section_name, option_name)


def update_option(SECTION_NAME, OPTION_NAME, VALUE):
    print("!!!!!!!" + OPTION_NAME)
    sed_script = "sed -i '/^\[%s\]/,/^\[/s/^%s.*/%s \= %s/' %s" % (SECTION_NAME, OPTION_NAME, OPTION_NAME, VALUE, SAMBA_FILE_PATH)
    subprocess.Popen(sed_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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


def before():
    if not section_exist(SECTION_NAME):
        print('Section : {:s} is not exist'.format(SECTION_NAME))
        exit()
    if not option_exist(SECTION_NAME, OPTION_NAME):
        print('Option : {:s} is not defined'.format(OPTION_NAME))
        exit()
    print('ok')


def run():
    update_option(SECTION_NAME, OPTION_NAME, VALUE)


def after():
    if not option_exist(SECTION_NAME, OPTION_NAME):
        print('Option : {:s} can not be updated'.format(OPTION_NAME))
        exit()
    if VALUE != get_option_value(SECTION_NAME, OPTION_NAME):
        print('Value : {:s} can not be assigned'.format(VALUE))
        exit()
    print('ok')


if __name__ == "__main__":
   globals()[sys.argv[1]]()
