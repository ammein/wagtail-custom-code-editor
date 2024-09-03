from __future__ import annotations
from typing import TypedDict


class CSSPosition(TypedDict, total=False):
    top: str | int | float
    left: str | int | float
    right: str | int | float
    bottom: str | int | float


class DropdownConfig(TypedDict, total=False):
    position: CSSPosition
    height: str
    width: str
    borderRadius: str
    boxShadow: str
    backgroundColor: str
