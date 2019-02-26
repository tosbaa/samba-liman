import configparser
import json
import sys
import subprocess

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)


def get_option_value(section_name, option_name):
    """ Takes two str and returns the option as string, exceptions are NoOptionError and NoSectionError"""
   
    return json.dumps(SAMBA_CONFIG_PARSER.get(section_name, option_name))


def get_invalid_users():
    """ Returns denied users as json according to 'invalid users' option in smb.conf """
 
    samba_section_invalid_users_dict = {}
    for section in SAMBA_CONFIG_PARSER.sections():
        try:
            samba_section_invalid_users_dict[section] = get_option_value(section, 'invalid users').split(',')
        except configparser.NoOptionError:
            continue
    return json.dumps(samba_section_invalid_users_dict)


def before():
    print("ok")

def run():
    print(get_invalid_users())

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