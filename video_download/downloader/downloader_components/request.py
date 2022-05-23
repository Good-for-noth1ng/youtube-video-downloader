import http.client
import json
import logging
import re
from functools import lru_cache
import socket
from urllib import parse
from urllib.error import URLError
from urllib.request import Request, urlopen
from downloader.downloader_components.error import RegexMatchError, MaxRetriesError

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
    split_url = parse.urlsplit(url=url)
    base_url = '%s://%s/%s?' % (split_url.scheme, split_url.netloc, split_url.path)
    querys = dict(parse.parse_qsl(split_url.query))
    querys['sq'] = 0
    url = base_url + parse.urlencode(querys)

    segment_data = b''
    for chunk in read_response_in_chunks(url=url, timeout=timeout, max_retries=max_retries):
        yield chunk
        segment_data += chunk

    stream_info = segment_data.split(b'\r\n')
    segment_count_pattern = re.compile(b'Segment-Count: (\\d+)')
    for line in stream_info:
        match = segment_count_pattern.search(line)
        if match:
            segment_count = int(match.group(1).decode('utf-8'))

    sequence_num = 1
    while sequence_num <= segment_count:
        querys['sq'] = seq_num
        url = base_url + parse.urlencode(query=querys)

        yield from read_response_in_chunks(url=url, timeout=timeout, max_retries=max_retries)
        sequence_num += 1
    return    

def read_response_in_chunks(url, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, max_retries=0):
    file_size = default_range_size
    downloaded = 0
    while downloaded < file_size:
        stop_pos = min(downloaded + default_range_size, file_size) - 1
        range_header = f"bytes={downloaded}-{stop_pos}"
        tries = 0

        while True:
            if tries >= 1 + max_retries:
                raise MaxRetriesError()
            try:
                response = execute_request(url=url, method="GET", headers={"Range": range_header}, timeout=timeout)
            except URLError as e:
                if isinstance(e.reason, socket.timeout):
                    pass
                else:
                    raise
            except http.client.IncompleteRead:
                pass
            else:
                break
            tries += 1  

        if file_size == default_range_size:
            try:
                content_range = response.info()["Content-Range"]
                file_size = int(content_range.split("/")[1])
            except (KeyError, IndexError, ValueError) as e:
                logger.error(e)
        while True:
            chunk = response.read()
            if not chunk:
                break
            downloaded += len(chunk)
            yield chunk
    return

@lru_cache
def get_file_size(url):
    return int(head(url)["content-length"])

@lru_cache
def get_file_size_from_seq_request(url):
    total_size = 0
    split_url = parse.urlsplit(url=url)
    base_url = '%s://%s/%s?' % (split_url.scheme, split_url.netloc, split_url.path)
    querys = dict(parse.parse_qsl(split_url.query))

    querys['sq'] = 0
    url = base_url + parse.urlencode(querys)
    response = execute_request(url=url, method="GET")
    response_value = response.read()
    total_size += len(response_value)

    segment_count = 0
    stream_info = response_value.split(b'\r\n')
    segment_regex = b'Segment-Count: (\\d+)'
    for line in stream_info:
        try:
            segment_count = int(regex_search(segment_regex, line, 1)) #import regex_search from helpers
        except RegexMatchError:
            pass
    
    if segment_count == 0:
        raise RegexMatchError('seq_filesize', segment_regex)

    sequence_num = 1
    while sequence_num < segment_count:
        querys['sq'] = sequence_num
        url = base_url + parse.urlencode(querys)
        total_size += int(get_headers(url=url)['content-length'])
        sequence_num += 1
    return total_size

def get_headers(url):
    """Get headers from get request"""
    response_headers = execute_request(url=url, method="HEAD").info()
    return {k.lower(): v for k, v in response_headers.items()}