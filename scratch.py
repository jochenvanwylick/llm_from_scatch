import logging
import re
from rich.logging import RichHandler

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
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
log.info(f"Split text into {len(preprocessed)} words")

all_words = sorted(set(preprocessed))
vocab_size = len(all_words)
log.info(f"Vocabulary size {len(all_words)}")


vocab = {token: integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    log.info(f"Vocab entry: {item}")
    if i >= 5:
        break


class SimpleTokenizerV1:
    def __init__(self, vocab) -> None:
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text):
        # Use regex to split - extracting words - which will make up the dictionary later
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        ids = [self.str_to_int[s] for s in preprocessed]

        log.info(f"Split text into {len(preprocessed)} words")
        return ids

    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])

        text = re.sub(r'\s+([,.?!"()\'])', r"\1", text)
        return text


t = SimpleTokenizerV1(vocab)
text = """"It's the last he painted, you know,"
    Mrs. Gisburn said with pardonable pride. """
ids = t.encode(text)
log.info(f"Encoding of:\n{text}\nIs equal to: {ids}")
decoded = t.decode(ids)
log.info(f"Decoded:\n{decoded}")


log.info(text.strip())
log.info(decoded.strip())
assert decoded.strip() == text.strip(), "Decoded text should match encoded text"
assert len(ids) == 14, "Expecting 14 encoded tokens"
