__author__ = 'gabriel'


def read_cfg(cfg_file):
    configs = dict()
    with open(cfg_file) as f:
        lines = f.readlines()
        for l in lines:
            separator = l.find("=")
            command = l[:separator].strip()
            argument = l[separator+1:].strip()

            if command not in configs:
                configs[command] = list()

            configs[command].append(argument)
    return configs
