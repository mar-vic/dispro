import xml.dom.minidom
from bs4 import BeautifulSoup

with open("./test_pretty.xml", "r") as f:
    # x = BeautifulSoup(f.read().replace("\n", "").rstrip(), "xml").prettify()
    x = BeautifulSoup(f.read().replace("\n", ""), "xml").prettify()
    print(x)
    # lines = [line for line in f.readlines()]
    # print(lines)

with open("./test_prettiest.xml", "w") as f:
    f.write(x)
