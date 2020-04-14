#Look how to read the argument from the command line
from os import *
from datetime import datetime
import sys
import json

def function_calls(args):
    func = args[1]
    project = args[2]
    message = " ".join(args[3:])
    daytime = datetime.today()
    if(func == "new"):
        print(func + " feature is currently being worked on")
        print(daytime)
        print(message)
    elif(func == "last"):
        print(func + " action not yet implemented")
        print("prioritize last > last project_name")
    elif(func == "del"):
        print(func + " action not yet implemented")
        print("prioritize del > del project_name > del log_id")
    else:
        print(func + " action not supported yet")


if __name__ == '__main__':
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))

    function_calls(sys.argv)
