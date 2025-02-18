import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re

model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def answer_question(content, question):
    input_text = f"question: {question} context: {content}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(input_ids, max_length=512, num_beams=5, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

context="my name is tarun and i study engineering , modi is the prime minister"
question="who is modi"
answer=answer_question(context,question)
print(answer)