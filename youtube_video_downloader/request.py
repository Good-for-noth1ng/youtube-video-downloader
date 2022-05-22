import http.client
import json
import logging
import re
from functools import lru_cache
import socket
from urllib import parse
from urllib.error import URLError
from urllib.request import Request, urlopen

"""Executes post or get request"""
def execute_request(url, method=None, headers=None, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    pass

"""Makes get request"""
def get(url):
    pass

"""Makes post request"""
def post(url):
    pass

def seq_stream(url):
    pass


