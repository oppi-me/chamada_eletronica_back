from configparser import ConfigParser


def config(section):
    parser = ConfigParser()
    parser.read('config.ini')

    data = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the configuration file.')

    return data
