#!/usr/bin/env python3

import sys

import pdf2eltec

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to provide a path to file you want validate!")
        exit()

    pdf2eltec.validate(sys.argv[1])
