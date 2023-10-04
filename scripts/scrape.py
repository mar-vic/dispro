import os
import re
import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

def download_title(author="hugo", title="robotnici_mora", url="https://zlatyfond.sme.sk/dielo/5126/Hugo_Robotnici-mora-I-Sieur-Clubin/1"):
    def get_all_chapters(url):
        """Generate a list of chapters of a book at given URL from zlaty fond"""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # scrape the contents
        current_chapter = soup.find("div", class_="titlepage").parent

        # find the url of next chapter if theere is one
        pagination = soup.select(".strankovanie a")
        next_chapter_anchor = [anchor for anchor in pagination if anchor.b.contents == ["nasledujúca kapitola »"]]
        next_chapter_url = None if len(next_chapter_anchor) == 0 else "https://zlatyfond.sme.sk" + next_chapter_anchor[0].attrs["href"]

        # recursively iterate through all chapters
        if next_chapter_url:
            return [current_chapter] + get_all_chapters(next_chapter_url)
        else:
            return [current_chapter]

    # breakpoint()
    soup = BeautifulSoup("<html><body></body></html>")
    chapters = get_all_chapters(url)
    for chapter in chapters:
        soup.body.append(chapter)
        
    # Create file with directories
    filename = f"/home/marcus/Projects/korpus/data/zlaty_fond/{author}/{title}/{title}__zf.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save the file
    with open(f"/home/marcus/Projects/korpus/data/zlaty_fond/{author}/{title}/{title}__zf.html", "w", encoding="utf-8") as file:
        file.write(str(soup.prettify()))

    print(f"\n~~Successfully downloaded '{title}' from {author}~~\n")

    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, "html.parser")

    # current_chapter_content = soup.find("div", class_="titlepage").parent
    # current_chapter_title = current_chapter_content.find("div", class_="titlepage").h2.contents[1]
    # # breakpoint()
    # pagination = soup.select(".strankovanie a")
    # next_chapter_anchor = [anchor for anchor in pagination if anchor.b.contents == ["nasledujúca kapitola »"]]
    # next_chapter_url = None if len(next_chapter_anchor) == 0 else "https://zlatyfond.sme.sk" + next_chapter_anchor[0].attrs["href"]

    # # Create file with directories
    # filename = f"/home/marcus/Projects/korpus/data/zlaty_fond/{author}/{title}/{title}__kap{chapter}.html"
    # os.makedirs(os.path.dirname(filename), exist_ok=True)

    # # Save the file
    # with open(f"/home/marcus/Projects/korpus/data/zlaty_fond/{author}/{title}/{title}__kap{chapter}.html", "w", encoding="utf-8") as file:
    #     file.write(str(current_chapter_content.prettify()))

    # print(f"Downloaded chapter {chapter} of {title}!")

    # # breakpoint()
    # if next_chapter_url:
    #     download_title(author="hugo", title="robotnici_mora", chapter=chapter+1, url=next_chapter_url)

def scrape_golden_fund():
    # response = requests.get("https://zlatyfond.sme.sk/autori")
    # soup = BeautifulSoup(response.content, "html.parser")
    with open("../data/zlaty_fond/zoznam_autorov.html") as f:
        soup = BeautifulSoup(f, "html.parser")

    # First, get the author spans
    author_spans = soup.find_all(attrs={"name": re.compile("^autor_")})

    # Then get the authors
    authors = [author_span.parent.parent for author_span in author_spans]

    authors_cleaned = []
    for author in authors:
        name = author.b.contents[0]
        titles = [{"name": anchor.contents[0],
                   "url": anchor.attrs["href"] + "/1"}
                  for anchor in author.ul.find_all("a")]
        authors_cleaned.append({"name": name, "titles": titles})

    # breakpoint()

    for author in authors_cleaned:
        print(f"\n{author['name']} has written following titles: \n")
        for title in author["titles"]:
            print(f"* {title['name']} (URL: {title['url']})")
        user_input = input("\nDo you want to download them?")
        
        if user_input == '':
            for title in author["titles"]:
                user_input = input(f"\nDo you want to download {title['name']} from {author['name']} at {title['url']}")

                if user_input == '':
                    download_title(author=author["name"], title=title["name"], url=title["url"])