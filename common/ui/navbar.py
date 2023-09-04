# common.ui.navbar.py

from flask import url_for
import os
from jinja2 import ChoiceLoader, FileSystemLoader, Environment

def getUIDir(file=__file__):
    return os.path.join(os.path.dirname(os.path.abspath(file)), 'templates')

common_ui_folder = getUIDir()

class navbar:
    def __init__(self, local_ui_folder, *args, **kargs):
        super().__init__(*args, **kargs)
        loader = ChoiceLoader(
            [
                FileSystemLoader(local_ui_folder),  # Your project-specific templates
                FileSystemLoader(common_ui_folder),  # Common templates
            ]
        )
        self.jinja2_env = Environment(loader=loader)
        self.jinja2_env.globals['url_for'] = url_for 
    
    def getEnv(self):
        return self.jinja2_env