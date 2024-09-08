#https://www.reddit.com/r/learnpython/comments/pkb6ar/beautifulsoup_capturing_paragraphs_until_next/
from requests_cache import CachedSession
import json
import re
from bs4 import BeautifulSoup, Tag


def find_section(heading):
    for sibling in heading.next_siblings:
        if not isinstance(sibling, Tag):
            continue
        if sibling.name in {'h2', 'h3', 'h4', 'h5'}:
            break
        if sibling.name == 'p':
            yield sibling


session = CachedSession()
endpoint = "https://en.wiktionary.org/w/api.php"
search = "soup"
response = session.get(f"{endpoint}?action=query&format=json&titles={search}&prop=extracts")
text = json.loads(response.text)
for page in text["query"]["pages"].values():
    soup = BeautifulSoup(page["extract"], "html.parser")
    for heading in soup.find_all(id=re.compile("^Etymology")):
        sentences = tuple(find_section(heading))
        #sentences = tuple(sentence.get_text() for sentence in find_section(heading))
        print()
