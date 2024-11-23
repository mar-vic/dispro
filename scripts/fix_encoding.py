#!/usr/bin/env python

import chardet
import codecs
import sys
import shutil

# with open("prihody_a_skusenosti_mladenca_reneho_I__bajza__tatran.txt", "r", encoding="Windows-1254") as f:
#     # result = chardet.detect(f.read())
#     # print(result["encoding"])
#     contents = f.read()
#     print(contents)

# with codecs.open("prihody_a_skusenosti_mladenca_reneho_I__bajza__tatran.txt", "r", encoding="cp1252") as f:
#     contents = f.read()
#     print(contents)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="cp1250") as f:
            contents = f.read()

        shutil.copy(sys.argv[1], sys.argv[1] + ".BAK")

        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write(contents)
