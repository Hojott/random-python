#!/usr/bin/env python3

import sys

from datetime import date

def get_days_since() -> int:
    """ Get days since the day """

    the_day = date(2023, 6, 12)
    today = date.today()

    return (today - the_day).days

def get_script() -> str:
    """ Get the running script """

    with open(sys.argv[0], 'r') as f:
        return f.read()

def main() -> None:
    """ Print days """

    print(get_script())
    print(f"Days since the day: {get_days_since()}")

if __name__ == "__main__":
    main()

