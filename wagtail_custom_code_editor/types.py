from __future__ import annotations
from typing import Dict, List, Any, TypedDict, Optional


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


class CustomCodeEditorOptionsDict(TypedDict, total=False):
    mode: Optional[str]
    theme: Optional[str]
    width: Optional[str]
    height: Optional[str]
    font_size: Optional[str]
    keybinding: Optional[str]
    useworker: Optional[bool]
    extensions: Optional[str | List]
    enable_options: Optional[bool]
    enable_modes: Optional[bool]
    options: Dict[str, Any]
    modes: List[Dict[str, str]]
    dropdown_config: DropdownConfig
    attrs: Dict[str, Any]


class CustomCodeEditorOptionsKwargs(TypedDict, total=False):
    ace: CustomCodeEditorOptionsDict
