import os
import json
import typing as t

_MESSAGES: t.Dict[str, t.Dict[str, str]] = json.load(
    open("/usr/src/app/telegram/messages.json")
)


def txt(country_code: str, text_key: str) -> str:
    unknown = "Unknown"

    if country_code not in _MESSAGES:
        return unknown

    if text_key not in _MESSAGES[country_code]:
        return unknown

    return _MESSAGES[country_code][text_key]


def get_list_of_languages() -> t.List[str]:
    return list(_MESSAGES.keys())
