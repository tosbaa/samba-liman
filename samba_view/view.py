import configparser
import json
samba_config_parser = configparser.ConfigParser()
samba_config_parser.read('../smb.conf')



def get_option_value(section_name, option_name):
    """ Takes two str and returns the option as string, exceptions are NoOptionError and NoSectionError"""
   
    return json.dumps(samba_config_parser.get(section_name, option_name))


def get_section_names():
    """ Returns section names as json according to the smb.conf file """
    
    return json.dumps({'section_names' : samba_config_parser.sections()})


def get_shared_users():
    """ Returns shared users as json according to 'valid users' option in smb.conf """
    
    samba_section_valid_users_dict = {}
    for section in samba_config_parser.sections():
        try:
            samba_section_valid_users_dict[section] = get_option_value(section, 'valid users').split(',')
        except configparser.NoOptionError:
            continue
    return json.dumps(samba_section_valid_users_dict)

def get_section_with_options(section_name):
    """ Takes section name(str) and returns section with option=value keys as json """
     
    if not samba_config_parser.has_section(section_name):
        raise Exception("Section {:s} can not be found".format(section_name))

    section_dict = {'section_name' : section_name}

    for option, value in samba_config_parser.items(section_name):
        section_dict[option] = value
    return json.dumps(section_dict)

def get_invalid_users():
    """ Returns denied users as json according to 'invalid users' option in smb.conf """
 
    samba_section_invalid_users_dict = {}
    for section in samba_config_parser.sections():
        try:
            samba_section_invalid_users_dict[section] = get_option_value(section, 'invalid users').split(',')
        except configparser.NoOptionError:
            continue
    return json.dumps(samba_section_invalid_users_dict)

