import ast
import json
import re
from downloader.downloader_components.error import HTMLParseError

def parse_for_all_objects(html, preceding_regex):
    result = []
    regex = re.compile(preceding_regex)
    match_iter = regex.finditer(html)
    for match in match_iter:
        start_index = match.end()
        try:
            obj = parse_for_all_objects(html, start_index)
        except HTMLParseError:
            continue
        else:
            result.append(obj)
    if len(result) == o:
        raise HTMLParseError(f'No matches for regex {preceding_regex}')
    return result

def parse_for_objects(html, preceding_regex):
    regex = re.compile(preceding_regex)
    result = regex.search(html)
    if not result:
        raise HTMLParseError(f'No matches for regex {preceding_regex}')
    start_index = result.end()
    return parse_for_objects_from_startpoint(html, start_index)

def parse_for_objects_from_startpoint(html, start_point):
    html = html[start_point:]
    if html[0] not in ['{', '[']:
        raise HTMLParseError(f'Invalid start point. Start of HTML:\n{html[:20]}')
    stack = [html[0]]
    i = 1

    context_closers = {
        '{': '}',
        '[': ']',
        '"': '"'
    }

    while i < len(html):
        if len(stack) == 0:
            break
        curr_char = html[i]
        curr_context = stack[-1]

        if curr_char == context_closers[curr_context]:
            stack.pop()
            i += 1
            continue

        if curr_context == '"':
            if curr_char == '\\':
                i += 2
                continue
        else:
            if curr_char in context_closers.keys():
                stack.append(curr_char)
        i += 1
    full_obj = html[:i]
    return full_obj