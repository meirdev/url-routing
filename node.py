# node.py

from dataclasses import dataclass, field
from itertools import takewhile
from typing import Generic, Optional, Self, TypeVar


def min_prefix(s1: str, s2: str) -> int:
    return sum(1 for _ in takewhile(lambda x: x[0] == x[1], zip(s1, s2)))


T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: str = ""
    children: list[Self] = field(default_factory=list)
    payload: Optional[T] = None

    def make_child(self, value: str, payload: Optional[T] = None) -> None:
        for child_idx, child in enumerate(self.children):
            min_pre = min_prefix(child.value, value)

            if min_pre == 0:
                continue

            if min_pre < min(len(child.value), len(value)):
                """
                Example
                -------
                value: /ports

                current tree:
                └── /posts

                updated tree:
                └── /po
                    ├── sts
                    └── rts
                """

                self.children[child_idx] = self.__class__(
                    value=child.value[:min_pre],
                    children=[
                        self.__class__(
                            value=child.value[min_pre:],
                            children=child.children,    # type: ignore
                            payload=child.payload,
                        ),
                        self.__class__(
                            value=value[min_pre:],
                            payload=payload,
                        ),
                    ],
                )

            elif len(value) < len(child.value):
                """
                Example
                -------
                value: /user

                current tree:
                └── /users

                updated tree:
                └── /user
                    └── s
                """

                self.children[child_idx] = self.__class__(
                    value=child.value[: len(value)],
                    children=[
                        self.__class__(
                            value=child.value[len(value) :],
                            children=child.children,    # type: ignore
                            payload=child.payload,
                        ),
                    ],
                    payload=child.payload,
                )

            elif len(value) > len(child.value):
                """
                Example
                -------
                value: /users

                current tree:
                └── /user

                updated tree:
                └── /user
                    └── s
                """

                child.make_child(
                    value=value[len(child.value) :],
                    payload=payload,
                )

            # overwrite existing node
            else:
                if payload is not None:
                    child.payload = payload

            return

        """
        Example
        -------
        value: /posts

        current tree:
        └── /users

        updated tree:
        └── /
            ├── users
            └── posts
        """

        self.children.append(
            self.__class__(
                value=value,
                payload=payload,
            )
        )

    def find_child(self, path: str) -> Optional[Self]:
        for node in self.children:
            if not path.startswith(node.value):
                continue

            if len(path) == len(node.value):
                return node

            return node.find_child(path[len(node.value) :])
