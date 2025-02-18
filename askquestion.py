import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer
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

def extract_relevant_context(context, keyword, window=100):
    # Use regular expressions to find all occurrences of the keyword
    pattern = re.compile(r'\b{}\b'.format(re.escape(keyword)), re.IGNORECASE)
    matches = [match.start() for match in pattern.finditer(context)]

    if not matches:
        return context  # Return the original context if no keyword is found

    # Extract text around each keyword occurrence
    snippets = []
    for match in matches:
        start = max(match - window, 0)
        end = min(match + window, len(context))
        snippet = context[start:end]
        snippets.append(snippet)
    
    # Combine snippets and ensure it's not too long
    relevant_context = ' '.join(snippets)
    return relevant_context[:1500] 

# Initialize the T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def answer_question(content, question):
    input_text = f"question: {question} context: {content}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(input_ids, max_length=512, num_beams=5, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

query = input("Enter your Query: ")
title = search_wikipedia(query)

if title:
    summary = get_wikipedia_content(title)
    print("Summary:", summary)
    smallercontext = extract_relevant_context(summary,)
    
    # Ask a specific question
    question = input("Enter your question: ")
    answer = answer_question(summary, question)
    print("Answer:", answer)
else:
    print("No results found.")
