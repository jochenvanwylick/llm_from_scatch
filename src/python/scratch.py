import logging
import re
from rich.logging import RichHandler
from tokenizer import SimpleTokenizerV1
from rapidfuzz import fuzz

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
