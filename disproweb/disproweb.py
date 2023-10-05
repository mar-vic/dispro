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
index = {}
total_title_count = 0
for author in authors:
    titles = [(title,
               [f"./data/{author}/{title}/{title_version}" for title_version in os.listdir(f"{data_root}{author}/{title}/")])
              for title in os.listdir(data_root + author + "/") if os.path.isdir(f"{data_root}{author}/{title}/")]

    corpus.append((author, titles))

    # Creating index
    author_names = list(reversed(author.split()))
    author_key = author_names[0][0].lower()
    if author_key in index:
        index[author_key].append((f"{author_names[0]}, {' '.join(author_names[1:])}", len(titles), author.lower().replace(" ", "-")))
    else:
        index[author_key] = [(f"{author_names[0]}, {' '.join(author_names[1:])}", len(titles), author.lower().replace(" ", "-"))]

    total_title_count += len(titles)

with open("../index.html", "w") as f:
    f.write(template.render(corpus=corpus,
                            title_count = total_title_count,
                            author_count=len(authors),
                            index=index,
                            alphabet="aábcčdďeéfghiíjklľmnňoóôpqrsštťuúvwxyýzž"))
