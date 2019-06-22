import configparser
samba_config_parser = configparser.ConfigParser()
samba_config_parser.read('smb.conf')
#print(samba_config_parser.sections())




def print_section_with_options(section_name):
    if not samba_config_parser.has_section(section_name):
        raise Exception("Section {:s} can not be found".format(section_name))
    else:
        print("Section : ", section_name)
        for option, value in samba_config_parser.items(section_name):
            print("    {:s}={:s}".format(option, value))


def get_option_value(section_name, option_name):
    try:
        return samba_config_parser.get(section_name, option_name)
    except configparser.NoSectionError:
        return "Section can not be found"
    except configparser.NoOptionError:
        return "Option can not be found"


def section_to_dict(section_name):
    if not samba_config_parser.has_section(section_name):
        raise Exception("Section {:s} can not be found".format(section_name))
    else:
        section_dict = {}
        section_dict["section_name"] = section_name

        for option, value in samba_config_parser.items(section_name):
            section_dict[option] = value

        return section_dict


def create_section(section_name):
    with open("smb.conf", "a") as samba_config_file:
        try:
            new_config_parser = configparser.ConfigParser()
            new_config_parser.add_section(section_name)
            new_config_parser.write(samba_config_file)
        except configparser.DuplicateSectionError:
            raise Exception("{:s} already exist".format(section_name))


def write_section_dict_to_file(section_dict):
    with open("smb.conf", "a") as samba_config_file:
        try:
            new_config_parser = configparser.ConfigParser()
            section_name = section_dict["section_name"]
            new_config_parser.add_section(section_name)
            samba_config_parser.add_section(section_name)
            del section_dict["section_name"]

            for option in section_dict:
                new_config_parser.set(section_name, option, section_dict[option])
            
            new_config_parser.write(samba_config_file)
        except configparser.DuplicateSectionError:
            print("{:s} already exist".format(section_name))

def get_section_names():
    return samba_config_parser.sections()


def has_section_already(section_dict):
    return samba_config_parser.has_section(section_dict("section_name"))

get_section_names()