#!/usr/bin/python
# Copyright (c) 2023 Mikheil Tabidze
import sys

import requests


def healthcheck():
    try:
        url = sys.argv[1]
        response = requests.get(url=url)
        if response.status_code == 200:
            sys.exit(0)
        else:
            print(f"Healthcheck error: status_code {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"Healthcheck error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    healthcheck()
