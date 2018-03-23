
from dataset import *

import sys


def parseval(value):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    elif value[0] == '[' or value[0] == '{' or value[0] == '(':
        return eval(value)
    try:
        val = value
        val = float(value)
        val = int(value)
        return val
    except Exception:
        return val


def main(prog_name, args):
    if len(args) < 1:
        print "Usage: " + prog_name + " <config_module> [option=value]*"
        sys.exit()

    if len(args) >= 2:
        tasks = [arg for arg in args[1:] if arg.find("=") == -1]
        options = {}
        for (option, value) in [arg.split("=") for arg in args[1:] if arg.find("=") != -1]:
            options[option] = parseval(value)
    else:
        tasks = []
        options = {}

    config_module = args[0]
    module = __import__(config_module)
    module.write_dataset(options)



if __name__ == '__main__':
    prog_name = sys.argv[0]
    args = sys.argv[1:]
    main(prog_name, args)

