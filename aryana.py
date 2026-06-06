import re

file = "the-verdict.txt"

with open(file) as f:
    text = f.read()

text_length = len(text)

print(f"The length of the text is {text_length}")
print(f"The beginning of the text looks like: {text[:99]}...")

splits = re.split(r"(\s)", text)
print(splits)
