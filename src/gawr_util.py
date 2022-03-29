#!/usr/bin/python3

import re
import json
import uuid
from json import JSONEncoder
from datetime import datetime


def generate_guid():
    return str(uuid.uuid4())


def kebab_case(s: str):
    punctuation_pattern = re.compile(r'[?!.,\'\"]')
    capitals_pattern = re.compile(r'(?<!^)(?=[A-Z])')
    underscore_pattern = re.compile(r'_')
    multispace_pattern = re.compile(r'\s+')
    spaces_pattern = re.compile(r' ')
    s = punctuation_pattern.sub('', s)
    s = capitals_pattern.sub(' ', s)
    s = underscore_pattern.sub(' ', s)
    s = multispace_pattern.sub(' ', s)
    s = spaces_pattern.sub('-', s).lower()
    return s

def try_get(obj: any, property_name: str):
    if property_name in obj:
        return obj.get(property_name)
    return None;

def json_serialize(obj):
    return json.dumps(obj, indent=2, separators=(',', ':'), cls=DefaultJsonEncoder)

class DefaultJsonEncoder(JSONEncoder):
    def default(self, o):
        o.__dict__
