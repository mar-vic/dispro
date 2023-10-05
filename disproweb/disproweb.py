import os
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("disproweb"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")
data_root = "../data/"
authors = [item for item in os.listdir(data_root) if os.path.isdir(data_root + item + "/")]

corpus = []
total_title_count = 0
for author in authors:
    titles = [(title,
               [f"./data/{author}/{title}/{title_version}" for title_version in os.listdir(f"{data_root}{author}/{title}/")])
              for title in os.listdir(data_root + author + "/") if os.path.isdir(f"{data_root}{author}/{title}/")]

    corpus.append((author, titles))
    total_title_count += len(titles)

with open("../index.html", "w") as f:
    f.write(template.render(corpus=corpus, title_count = total_title_count, author_count=len(authors)))
