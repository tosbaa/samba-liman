import sys
import configparser
import os
import subprocess
SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = '../smb.conf'
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)
BLOCKED_SECTIONS = ["global", "homes", "printers", "print$"]

OLD_SECTION_NAME = sys.argv[2]
NEW_SECTION_NAME = sys.argv[3]

def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def is_section_name_unique(section_name):
    return not (section_name in SAMBA_CONFIG_PARSER.sections())


def update_section_name(old_name, new_name):
    sed_script = "sed -i 's/^\[{:s}\]$/\[{:s}\]/' {:s}".format(old_name, new_name, SAMBA_FILE_PATH)
    subprocess.Popen(sed_script, shell=True)


def make_bash_call(stage_name):
    bash = ['python3.7', __file__, stage_name, sys.argv[2], sys.argv[3]]
    output = subprocess.Popen(bash, stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8')

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
    if not section_exist(OLD_SECTION_NAME):
        print('Section : {:s} is not exist'.format(OLD_SECTION_NAME))
        exit()
    if not is_section_name_unique(NEW_SECTION_NAME):
        print('Section : {:s} already defined'.format(NEW_SECTION_NAME))
        exit()
    if OLD_SECTION_NAME in BLOCKED_SECTIONS:
        print("Section : {:s} can not be modified".format(OLD_SECTION_NAME))
        exit()
    if NEW_SECTION_NAME in BLOCKED_SECTIONS:
        print('Special name : {:s}  can not be assigned '.format(NEW_SECTION_NAME))
        exit()
    print('ok')

def run():
    update_section_name(OLD_SECTION_NAME, NEW_SECTION_NAME)


def after():
    if not section_exist(NEW_SECTION_NAME):
        print("Section could't be updated")
        exit()
    print('ok')

if __name__ == "__main__":
   globals()[sys.argv[1]]()