import functools
import gzip
import json
import logging
import os
import re
import warnings
from typing import Any, Callable, Dict, List, Optional, TypeVar
from urllib import request

from downloader.downloader_components.error import RegexMatchError


logger = logging.getLogger(__name__)


class DeferredGeneratorlist():
    def __init__(self, generator):
        self.gen = generator
        self._elements = []
    

    def __eq__(self, other):
        return list(self) == other
    

    def __getitem__(self, key) -> Any:
        if not isinstance(key, (int, slice)):
            raise TypeError('Key must be either a slice or int')

        key_slice = key
        if isinstance(key, int):
            key_slice = slice(key, key + 1, 1)
        
        while len(self._elements) < key_slice.stop:
            try: 
                next_item = next(self.gen)
            except StopIteration:
                raise IndexError
            else:
                self._elements.append(next_item)
        return self._elements[key]


    def __iter__(self):
        iter_index = 0
        while True:
            try: 
                curr_item = self[iter_index]
            except IndexError:
                return
            else:
                yield curr_item
                iter_index += 1

    def __next__(self):
        pass

    def __len__(self):
        pass

    def __repr__(self):
        pass

    def __reversed__(self):
        pass

    def generate_all(self):
        pass
