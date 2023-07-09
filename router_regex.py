# router_regex.py

import re
from collections import defaultdict
from functools import partial
from typing import Any, Callable

PARAM_REGEX = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}")


def replace_param(match: re.Match) -> str:
    param_name, convertor_type = match.groups("str")
    convertor_type = convertor_type.lstrip(":")

    match convertor_type:
        case "str":
            convertor = r"[^/]+"
        case "int":
            convertor = r"[0-9]+"
        case "path":
            convertor = r".*"
        case _:
            raise ValueError(f"Unknown convertor type {convertor_type}")

    return f"(?P<{param_name}>{convertor})"


def compile_path(path: str) -> re.Pattern:
    re_path = PARAM_REGEX.sub(replace_param, path)

    return re.compile(f"^{re_path}$")


Handler = Callable[..., Any]


class Router:
    def __init__(self, path: str, handler: Handler) -> None:
        self.path = compile_path(path)
        self.handler = handler

    def match(self, path: str) -> dict[str, str] | None:
        if match := self.path.match(path):
            return match.groupdict()


class Routers:
    def __init__(self) -> None:
        self._routers: dict[str, list[Router]] = defaultdict(list)

    def add_router(self, method: str, router: Router) -> None:
        self._routers[method].append(router)

    def get_handler(self, method: str, path: str) -> Handler | None:
        for router in self._routers.get(method, []):
            if params := router.match(path):
                return partial(router.handler, **params)
