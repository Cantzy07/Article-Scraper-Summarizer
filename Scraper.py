import os

import newspaper
import validators
import re

from openai import OpenAI

#connect the localhost LLM model
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Scraper
# receive user input then validate that it is a real article
print("Enter the url of an article: ")
url = input()
while not url:
    print("Empty input\nEnter the url of an article:")
    url = input()
if validators.url(url):
    print("Valid URL")
else:
    exit()

# if it is a real article then write to a txt file with the contents
article = newspaper.Article(url)
article.download()
article.parse()

title = article.title
articleBody = article.text
sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)
file = open(sanitized_title, 'w')
file.write(articleBody)
file.close()
# end Scraper

#Create model and parameters
#Uses open-source LLM gemma from LM Studio
completion = client.chat.completions.create(
        model="lmstudio-ai/gemma-2b-it-GGUF",
        messages=[
            {"role": "system", "content": "You are a professional assistant"},
            {"role": "user", "content": f"I want you to create a summary of the given article: {articleBody}"}
        ],
        temperature=0.7,
    )
articleSummary = completion.choices[0].message.content
file = open(sanitized_title + "_summary", 'w')
file.write(articleSummary)
file.close()
