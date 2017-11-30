from flask import Flask, render_template;
from os import environ

class PageData:
    def __init__(self, name, title, description=""):
        self.name = name
        self.title = title
        self.description = description

app = Flask(__name__)

import views
import taxes
import analytics