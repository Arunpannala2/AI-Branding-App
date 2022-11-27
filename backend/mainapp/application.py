import os
from typing import List
import openai
import argparse
import re

MAX_INPUT_LENGTH = 13

def main():
    print("Running application!")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    u_input = args.input

    print(f"User input: {u_input}")
    if validate_len(u_input):
        create_branding(u_input)
        create_keywords(u_input)
    else:
        raise ValueError(f"Input length too long, must be under {MAX_INPUT_LENGTH}. Submitted input is {u_input}")

def create_keywords(prompt: str) -> List[str]:

    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"Generate related branding keywords for {prompt}: "
    print(enriched_prompt)

    response = openai.Completion.create(
        model="text-davinci-002", prompt=enriched_prompt, temperature=0, max_tokens=32)

    #Extract output text
    keywords_text: str = response["choices"][0]["text"]

    #Strip whitespace
    keywords_text = keywords_text.strip()
    keywords_split = re.split(",|\n|;|-", keywords_text)
    keywords_split = [k.lower().strip() for k in keywords_split]
    keywords_split = [k for k in keywords_split if len(k) > 0]
    print(f"Keywords: {keywords_split}")
    return keywords_split

def validate_len(prompt:str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def create_branding(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate branding snippet for {prompt}: "
    print(enriched_prompt)
    response = openai.Completion.create(
        model="text-davinci-002", prompt=enriched_prompt, temperature=0, max_tokens=32)

    #Extract output text
    branding_text: str = response["choices"][0]["text"]

    #Strip whitespace
    branding_text = branding_text.strip()
    
    #Add ... to truncated statements.
    last_char = branding_text[-1]
    if last_char not in(".", "!", "?"):
        branding_text += "..."
    
    print(f"Snippet: {branding_text}")
    return branding_text


if __name__ == "__main__":
    main()