import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAPI_KEY = os.getenv("OPENAPI_KEY")
print(OPENAPI_KEY)
# Initialize the OpenAI client with your API key
openai.api_key = OPENAPI_KEY

def extract_keywords_from_question_gpt(question, model="gpt-3.5-turbo"):
    prompt = f"Given the following question, answer by extracting relevant keywords to be checked in the data for the answer:\n\nQuestion: {question}\n\nKeywords:"
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
    )
    keywords = response.choices[0].text.strip()
    return keywords

question = "During which dynasty were the most well-known sections of the Great Wall built?"
keywords = extract_keywords_from_question_gpt(question)
print("Keywords:", keywords)
