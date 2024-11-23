#!/usr/bin/env python
import sys
import shutil
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.is_file():
            print("This is not a file!")
            sys.exit(0)
        # print(p.absolute())
        author = input("Author: ")
        title = input("Title: ")
        publisher = input("Publisher: ")
        Path(f"processing/{author}/{title}/{publisher}/").mkdir(parents=True)
        shutil.copy(p.absolute(), f"./processing/{author}/{title}/{publisher}/{title}__{author}__{publisher}{p.suffix}")
    else:
        print("I need a file to work on!")
