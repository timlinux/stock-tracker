#!/usr/bin/env python
import requests
from datetime import date

today = date.today().strftime("%Y-%m-%d")

symbols = requests.get(f"https://www.nasdaq.com/ef2efeb8-f12c-4d3f-8307-b61b2ec38dc0").text.splitlines()[1:]
symbols = sorted(set(symbols))

with open("symbols.txt", "w") as f:
    f.write("\n".join(symbols))
