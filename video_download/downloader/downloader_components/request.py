import http.client
import json
import logging
import re
from functools import lru_cache
import socket
from urllib import parse
from urllib.error import URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)
default_range_size = 9437184

"""Executes post or get request"""
def execute_request(url: str, method=None, headers=None, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
    if headers:
        base_headers.update(headers)
    if data:
        if not isinstance(data, bytes):
            data = bytes(json.dumps(data), encoding="utf-8")
    if url.lower().startswith("http"):
        request = Request(url=url, headers=base_headers, method=method, data=data)
    else:
        raise ValueError("Invalid url")
    return urlopen(request, timeout=timeout)

"""Makes get request"""
def get(url, extra_headers=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    if extra_headers is None:
        extra_headers = {}
    response = execute_request(url=url, headers=extra_headers, timeout=timeout)
    return response.read().decode("utf-8")

"""Makes post request"""
def post(url, extra_headers=None, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    if extra_headers is None:
        extra_headers = {}
    if data is None:
        data = {}
    extra_headers.update({"Content-Type": "application/json"})
    response = execute_request(url=url, headers=extra_headers, data=data, timeout=timeout)
    return response.read().decode("utf-8")

def read_response_in_sequence(url, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, max_retries=0):
    pass

def read_response_in_chunks(url, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, max_retries=0):
    pass

def get__file_size(url):
    pass

def get_file_size_from_seq_request(url):
    pass

def get_headers(url):
    """Get headers from get request"""
    response_headers = execute_request(url=url, method="HEAD").info()
    return {k.lower(): v for k, v in response_headers.items()}