
import os
import json


class Config:
    def __init__(self, **entries):
        self.pacmd_sink = ""
        self.pacmd_card = ""
        self.xrandr_name = ""
        self.resolution = ""
        self.rate = ""
        self.launch = []
        self.__dict__.update(entries)



def load(config_path: str, name: str) -> (bool, Config):
    # load configured sinks
    with open(config_path, "r") as config_file:
        sinks = json.load(config_file)

    if not name in sinks:
        return False

    config = Config(**sinks[name])
    print(config.__dict__)
    return (True, config)
    

def get_sink(name :str) -> {}:

    # get config file path
    pwd = os.path.dirname(os.path.abspath(__file__))
    config_path = f"{pwd}/sinks.json"

    # load configured sinks
    with open(config_path, "r") as config_file:
        sinks = json.load(config_file)
        
    if not name in sinks:
        return None
    else:
        return sinks[name]