from audioop import reverse
import re
import string


def get_first_number(key: str) -> str:
    for char in key:
        if char in string.digits:
            return char


def get_last_number(key: str) -> str:
    return get_first_number(reversed(key))


def get_calibration_value(key: str) -> int:
    a = get_first_number(key)
    b = get_last_number(key)
    return int(a + b)


def part_one(keys: list[str]) -> int:
    out = 0
    for key in keys:
        out += get_calibration_value(key)

    return out


NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def reverse_string(string):
    return "".join(reversed(string))


pattern = re.compile("|".join(list(NUMBERS.keys()) + [x for x in string.digits]))
reverse_pattern = re.compile(
    "|".join([reverse_string(x) for x in NUMBERS.keys()] + [x for x in string.digits])
)


def get_first_and_last(key):
    a = pattern.search(key).group(0)
    b = reverse_string(reverse_pattern.search(reverse_string(key)).group(0))

    a = NUMBERS.get(a) or a
    b = NUMBERS.get(b) or b

    return a, b


def get_calibration_advanced(key):
    a, b = get_first_and_last(key)
    return int(a + b)


def part_two(keys):
    out = 0
    for key in keys:
        out += get_calibration_advanced(key)

    return out
