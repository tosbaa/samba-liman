import configparser
import json
import sys
import subprocess

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = "../smb.conf"
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)


def get_section_names():
    """ Returns section names as json according to the smb.conf file """
    
    return json.dumps({'section_names' : SAMBA_CONFIG_PARSER.sections()})


def before():
    print("ok")


def run():
    print(get_section_names())

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
    bash = ['python3.7', __file__, stage_name] 
    output = subprocess.Popen(bash, stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8')


if __name__ == "__main__":
   globals()[sys.argv[1]]()
