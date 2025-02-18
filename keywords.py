import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords_ner(question):
    # Use spaCy to extract named entities
    doc = nlp(question)
    keywords = [ent.text for ent in doc.ents]
    
    # Use NLTK for additional keyword extraction
    tokens = word_tokenize(question)
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords and lowercase the tokens
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Combine spaCy keywords with filtered tokens from NLTK
    combined_keywords = list(set(keywords + filtered_tokens))
    
    return combined_keywords

question = "what year was the great wall of china built?"
keywords = extract_keywords_ner(question)
print("Keywords:", keywords)
