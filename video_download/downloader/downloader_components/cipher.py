import logging
import re
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple

from downloader.downloader_components.error import ExtractError, RegexMatchError
