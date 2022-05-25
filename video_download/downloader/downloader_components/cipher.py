import logging
import re
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple

from downloader.downloader_components.error import ExtractError, RegexMatchError
from downloader.downloader_components.helpers import cache, regex_search
from downloader.downloader_components.parser import find_object_from_startpoint, throttling_array_split

logger = logging.getLogger(__name__)

class Cipher:
    def __init__(self, js: str):
        self.transform_plan: str = get_transform_plan(js)
        var_regex = re.compile(r"^\w+\W")
        var_match = var_regex.search(self.transform_plan[0])
        if not var_match:
            raise RegexMatchError(caller="__init__", pattern=var_regex.pattern)
        var = var_match.group(0)[:-1]
        self.transform_map = get_transform_map(js, var)
        self.js_func_patterns = [
            r"\w+\.(\w+)\(\w,(\d+)\)",
            r"\w+\[(\"\w+\")\]\(\w,(\d+)\)"
        ]
        self.throttling_plan = get_throttling_plan(js)
        self.throttling_array = get_throttling_function_array(js)
        self.calculated_n = None


    def calculate_n(self, initial_n: list):
        """converts n to prevent throttling"""
        if self.calculated_n:
            return self.calculated_n

        for i in range(len(self.throttling_array)):
            if self.throttling_array[i] == 'b':
                self.throttling_array[i] = initial_n
        
        for step in self.throttling_plan:
            curr_func = self.throttling_array[int(step[0])]
            if not callable(curr_func):
                logger.debug(f"{curr_func} is not callable")
                logger.debug(f"Throttlong array:\n{self.throttling_array}\n")
                raise ExtractError(f"{curr_func} is not callable")
            first_arg = self.throttling_array[int(step[1])]
            if len(step) == 2:
                curr_func(first_arg)
            elif len(step) == 3:
                second_arg = self.throttling_array[int(step[2])]
                curr_func(first_arg, second_arg)

        self.calculated_n = ''.join(initial_n)
        return self.calculated_n


    def get_signature(self, ciphered_signature: str):
        signature = list(ciphered_signature)
        
        for js_func in self.transform_plan:
            name, argument = self.parse_functions(js_func)
            signature = self.transform_map[name](signature, argument)
            logger.debug(
                "applied transform function\n"
                "output: %s\n"
                "js function: %s\n"
                "argument: %d\n"
                "function: %s",
                "".join(signature),
                name, 
                argument,
                self.transform_map[name]
            )
        return "".join(signature)

    @cache
    def parse_functions(self, js_func: str) -> Tuple[str, int]:
        """js function -> tupple containing function name and integer argument"""
        logger.debug("parssing transform function")
        for pattern in self.js_func_patterns:
            regex = re.compile(pattern)
            parse_match = regex.search(js_func)
            if parse_match:
                fn_name, fn_arg = parse_match.groups()
                return fn_name, int(fn_arg)
        raise RegexMatchError(caller="parse_function", pattern="js_func_patterns")

def get_initial_function_name(js: str) -> str:
    pass

def get_transform_plan(js: str) -> List[str]:
    pass

def get_transform_objects(js: str, var: str) -> List[str]:
    pass

def get_transform_map(js: str, var: str) -> Dict:
    pass

def throttling_function_name(js: str) -> str:
    pass

def throttling_function_code(js: str) -> str:
    pass

def get_throttling_function_array(js: str) -> List[Any]:
    pass

def get_throttling_plan(js: str):
    pass

def reverse(arr: List, _:Optional[Any]):
    pass

def splice(arr: list, b: int):
    pass

def swap(arr: List,  b: int):
    pass

def throttling_reverse(arr: list):
    pass

def throttling_push(d: list, e: Any):
    pass

def throttling_mod_func(d: list, e: int):
    pass

def throttling_unshift(d: list, e: int):
    pass

def throttling_cipher_function(d: list, e: str):
    pass

def throttling_nested_splice(d: list, e: int):
    pass

def throttling_prepend(d: list, e: int):
    pass

def throttling_swap(d: list, e: int):
    pass

def js_splice(arr: list, start: int, delete_count: None, *items):
    pass

def map_functions(js_func: str) -> Callable:
    pass