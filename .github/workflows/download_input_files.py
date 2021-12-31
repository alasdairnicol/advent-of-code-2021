#!/usr/bin/env python
import urllib.request
import os

def main():
    cookie = os.environ['cookie']
    year = os.environ['year']

    headers={'Cookie': f'session={cookie}'}

    for day in range(1, 5):
        url = f'https://adventofcode.com/{year}/day/{day}/input'
        request=urllib.request.Request(url=url,headers=headers)
        response=urllib.request.urlopen(request)

        if response.status == 200:
            print(f"Writing response for day {day}")
            with open(f"day{day:02}.txt", 'wb') as f:
                f.write(response.read())

if __name__ == "__main__":
  main()

