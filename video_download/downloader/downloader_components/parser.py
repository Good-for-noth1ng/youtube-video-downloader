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

def find_object_from_startpoint(html, start_point):
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

def parse_for_object_from_startpoint(html, start_point):
    full_obj = find_object_from_startpoint(html, start_point)
    try:
        return json.loads(full_obj)
    except json.decoder.JSONDecodeError:
        try:
            return ast.literal_eval(full_obj)
        except (ValueError, SyntaxError):
            raise HTMLParseError("Couldn't parse object")

def throttling_array_split(js_array):
    results = []
    curr_substring = js_array[1:]

    comma_regex = re.compile(r",")
    func_regex = re.compile(r"function\([^)]*\)")

    while len(curr_substring) > 0:
        if curr_substring.startswith('function'):
            match = func_regex.search(curr_substring)
            match_start, match_end = match.span()

            function_text = find_object_from_startpoint(curr_substring, match.span()[1])
            full_function_def = curr_substring[:match_end + len(function_text)]
            results.append(full_function_def)
            curr_substring = curr_substring[len(full_function_def) + 1:]
        else:
            match = comma_regex.search(curr_substring)
            try:
                match_start, match_end = macth.span()
            except AttributeError:
                match_start = len(curr_substring) - 1
                match_end = match_start + 1
            curr_el = curr_substring[:match_start]
            results.append(curr_el)
            curr_substring = curr_substring[match_end:]
    return results