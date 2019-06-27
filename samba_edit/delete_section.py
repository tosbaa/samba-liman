import sys
import configparser
import os
import subprocess
SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = '../smb.conf'
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)
BLOCKED_SECTIONS = ["global", "homes", "printers", "print$"]

SECTION_NAME = sys.argv[2]

def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def make_bash_call(stage_name):
    bash = ['python3.7', __file__, stage_name, sys.argv[2]] 
    output = subprocess.Popen(bash, stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8')


def delete_section(section_name):
    sed_script = "sed -i '/^\[%s\]/,/^\[/{/^\[/!d};/^\[%s\]/d' %s" % (SECTION_NAME, SECTION_NAME, SAMBA_FILE_PATH)
    subprocess.Popen(sed_script, shell=True)


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
        print('Section name : {:s} not exist'.format(SECTION_NAME))
        exit()
    if SECTION_NAME in BLOCKED_SECTIONS:
        print('Section name : {:s} can not be deleted'.format(SECTION_NAME))
        exit()
    print('ok')


def run():
    delete_section(SECTION_NAME)


def after():
    if section_exist(SECTION_NAME):
        print('Section : {:s} can not be deleted'.format(SECTION_NAME))
    print('ok')


if __name__ == "__main__":
   globals()[sys.argv[1]]()
