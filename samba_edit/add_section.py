import sys
import configparser
import os
import subprocess
SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_FILE_PATH = '../smb.conf'
SAMBA_CONFIG_PARSER.read(SAMBA_FILE_PATH)

SECTION_NAME = sys.argv[2]
FILE_PATH = sys.argv[3]


def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    
    return SAMBA_CONFIG_PARSER.has_section(section_name)

def file_exist(file_path):
    """ Takes file_path(str) argument and checks that file exist in given path """
    
    return os.path.isdir(file_path)


def is_path_duplicate(path):
    """ Checks other sections path, if there is a match, returns an error """

    for section in SAMBA_CONFIG_PARSER.sections():
        try:
            if path == SAMBA_CONFIG_PARSER.get(section, 'path'):
                return True
        except configparser.NoOptionError:
            continue
    return False


def add_section(section_name, file_path):
    """ Add section to smb.conf file, checks for existence and duplication for path """

    with open(SAMBA_FILE_PATH, "a") as samba_config_file:
        new_config_parser = configparser.ConfigParser()
        new_config_parser.add_section(section_name)
        new_config_parser.set(section_name, 'path', file_path)
        new_config_parser.write(samba_config_file)


def before():
    if section_exist(SECTION_NAME):
        print('Section name : {:s} already exist'.format(SECTION_NAME))
        exit()
    elif not file_exist(FILE_PATH):
        print('No file in path : {:s}'.format(FILE_PATH))
        exit()
    elif is_path_duplicate(FILE_PATH):
        print('Given file path is already defined in config file')
        exit()
    print('ok')



def run():
    add_section(SECTION_NAME,FILE_PATH)


def after():
    if not section_exist(SECTION_NAME):
        print('Section : {:s} can not be created'.format(SECTION_NAME))
        exit()
    print('ok')


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
