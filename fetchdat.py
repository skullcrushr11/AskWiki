import requests
import re

def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "format": "json",
        "search": query,
        "limit": 1,  # Limit the search to one result
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    if data[1]:
        return data[1][0]  # Return the first search result
    else:
        return None

def get_wikipedia_content(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
    }

    response = requests.get(url, params=params)
    data = response.json()

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    content = page.get("extract", "No content available.")

    return content


# def get_section(content, section_title):
#     pattern = re.compile(r'==\s*' + re.escape(section_title) + r'\s*==(.+?)(==\s*\w)', re.DOTALL)
#     match = pattern.search(content)
#     if match:
#         return match.group(1).strip()
#     else:
#         return "Section not found."
    

query = input("Enter your Query: ")
title = search_wikipedia(query)
print(title)

if title:
    summary = get_wikipedia_content(title)
    # maincontent = get_section(summary,query)
    # print(maincontent)
    print(summary)
else:
    print("No results found.")
