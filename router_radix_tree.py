# router_radix_tree.py

import re
from collections import defaultdict
from functools import partial
from itertools import zip_longest
from typing import Any, Callable, Optional, Self

from node import Node


Handler = Callable[..., Any]


def split_parts(path: str) -> list[str]:
    return [part for part in re.sub(r"/+", "/", path).split("/") if part != ""]


class Router:
    def __init__(self, path: str, handler: Handler) -> None:
        self.path = path
        self.handler = handler

    def match(self, path: str) -> dict[str, str] | None:
        parts = iter(split_parts(path))
        params = {}

        for self_part, arg_part in zip_longest(split_parts(self.path), parts):
            if self_part is None or arg_part is None:
                return None

            if self_part[0] == ":":
                params[self_part[1:]] = arg_part

            elif self_part[0] == "*":
                params[self_part[1:]] = "/".join([arg_part, *parts])

            elif self_part != arg_part:
                return None

        return params


class RouterNode(Node[Router]):
    def find_child(self, path: str) -> Optional[Self]: 
        for node in self.children:
            if node.value.startswith("/:"):
                if (sep := path.find("/", 2)) == -1:
                    return node
                return node.find_child(path[sep:])

            if node.value.startswith("/*"):
                return node

            if not path.startswith(node.value):
                continue

            if len(path) == len(node.value):
                return node

            return node.find_child(path[len(node.value) :])


class Routers:
    def __init__(self) -> None:
        self._routers: dict[str, RouterNode] = defaultdict(RouterNode)  # type: ignore

    def add_router(self, method: str, router: Router) -> None:
        node = self._routers[method]
        parts = split_parts(router.path)

        path = ""
        for i, part in enumerate(parts):
            path += "/" + part

            if i == len(parts) - 1:
                node.make_child(path, router)
            else:
                node.make_child(path)

    def get_handler(self, method: str, path: str) -> Handler | None:
        if node := self._routers[method].find_child(path):
            if router := node.payload:
                if params := router.match(path):
                    return partial(router.handler, **params)
