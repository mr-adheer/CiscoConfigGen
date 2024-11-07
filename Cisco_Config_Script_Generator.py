#!/usr/bin/env python3
# based on https://developer.cisco.com/codeexchange/github/repo/Tes3awy/Cisco-Configuration-Using-Python-Jinja-CSV/
## install the follwoing Python3 packages ##
# Jinja2

import os
import time
from csv import DictReader
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

CONFIG_TEMPLATE = "Config_Script_Template.j2"
OUTPUT_DIR = "Configuration_Output_Files"
INPUT_CSV_FILE = "Config_Script_Input_Values.csv"

# Create configs directory if not created already
time = datetime.now()
DIR_NOW = f"{time.strftime('%Y%b%d_%H%M%S')}_{'Config_Scripts'}"
FILE_NOW = time.strftime('%d_%b_%Y-%H-%M-%S')
DIR_PATH = os.path.join(OUTPUT_DIR,DIR_NOW)
if not os.path.exists(DIR_PATH):
    os.makedirs(DIR_PATH)

def build_template(config_template_file: str = CONFIG_TEMPLATE, parameters_file: str = INPUT_CSV_FILE,):
    
    # Handle Jinja template
    env = Environment(loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(name=config_template_file)
    
    # Read the parameters from csv file and convert it to a dictionary
    with open(file=parameters_file, mode="rt", encoding="utf-8") as params:
        for param in DictReader(params):
            dict_params = dict(param)
            config = template.render(dict_params)
            global FILE_NOW, DIR_PATH
            FILE_NAME = f"{dict_params.get('DEVICE_TYPE')}{'_('}{dict_params.get('BRANCH_NAME')}{'-'}{dict_params.get('BRANCH_ID')}{')'}_{'('}{dict_params.get('HOSTNAME')}{')'}_{FILE_NOW}.{'txt'}"
            FILE_PATH = os.path.join(DIR_PATH, FILE_NAME)
            with open(file=FILE_PATH, mode="wt", encoding="utf-8") as cfg_file:
                cfg_file.write(config)
            print(f"Configuration file '{FILE_NAME}' is created in Folder '{DIR_NOW}'", end="\n\n")
if __name__ == "__main__":
    build_template()