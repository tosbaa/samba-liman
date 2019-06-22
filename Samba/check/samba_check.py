import configparser
import subprocess

SAMBA_CONFIG_PARSER = configparser.ConfigParser()
SAMBA_CONFIG_PARSER.read('smb.conf')


def section_exist(section_name):
    """ Takes section_name(str) argument and returns True if the given name exist """
    return SAMBA_CONFIG_PARSER.has_section(section_name)


def option_exist(section_name, option_name):
    """ Checks section_name(str) and option_name(str) and returns True if option exist """
    return SAMBA_CONFIG_PARSER.has_option(section_name, option_name)


def check_file_exist(file_path):
    """ Takes file_path(str) argument and checks that file exist in given path """
    if file_path == "":
        return False

    bash_script = 'test -f ' + file_path + ' && echo TRUE'
    check_file_process = subprocess.Popen(bash_script, shell=True, stdout=subprocess.PIPE)
    
    ## Slicing makes b'TRUE\n' -> TRUE
    bash_output = str(check_file_process.stdout.read())[2:6]
    
    if bash_output == 'TRUE':
        return True
    return False


def check_section_duplication(section_name):
    if SAMBA_CONFIG_PARSER.has_section(section_name):
        raise configparser.DuplicateSectionError('section {:s} already exist'.format(section_name))

print(check_file_exist('/Users/yagiz/Desktop/deneme.txt1'))