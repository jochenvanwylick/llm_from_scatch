import logging
import re
from rich.logging import RichHandler
from tokenizer import SimpleTokenizerV1, SimpleTokenizerV2
from rapidfuzz import fuzz
from importlib.metadata import version
import tiktoken


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

# Read the source file
training_file = "the-verdict.txt"
with open(training_file, "r", encoding="utf-8") as f:
    raw_text = f.read()
log.info(f"Training file {training_file} read - {len(raw_text)} characters")

# Use regex to split - extracting words - which will make up the dictionary later
preprocessed: list[str] = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
log.info(f"Split text into {len(preprocessed)} words")

all_words: list[str] = sorted(set(preprocessed))
vocab_size = len(all_words)
log.info(f"Vocabulary size {len(all_words)}")

vocab: dict[str, int] = {token: integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    log.info(f"Vocab entry: {item}")
    if i >= 5:
        break

t = SimpleTokenizerV1(vocab)
text = (
    """"It's the last he painted, you know, Mrs. Gisburn said with pardonable pride."""
)
encoded: list[int] = t.encode(text)
decoded: str = t.decode(encoded)

ratio: float = fuzz.ratio(text, decoded)
assert ratio > 0.95, "expecting orginal to VERY similar to original>encoded>decoded"

all_tokens = sorted(list(set(preprocessed)))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
vocab = {token: integer for integer, token in enumerate(all_tokens)}

print(len(vocab.items()))

for i, item in enumerate(list(vocab.items())[-5:]):
    print(item)

t1 = SimpleTokenizerV2(vocab)
text1 = "Hello, do you like tea?"
text2 = "In the sunlit terraces of the palace."
text = " <|endoftext|> ".join((text1, text2))
print(text)

print(t1.encode(text))

print("tiktoken version: ", version("tiktoken"))

tokenizer = tiktoken.get_encoding("gpt2")

text = (
    "Hello, do you like tea? <|endoftext|> In the sunlit terracesof some unknownPlace."
)

integers = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
print(integers)
strings = tokenizer.decode(integers)
print(strings)
