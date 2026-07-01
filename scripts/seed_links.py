import csv

SHARD_BITS = 14
SEQUENCE_BITS = 50

MAX_SHARD_ID = (1 << SHARD_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def base62_encode(number: int) -> str:
    if number < 0:
            raise ValueError("Base62 encoding only supports non-negative integers")

    if number == 0:
        return BASE62_ALPHABET[0]

    base = len(BASE62_ALPHABET)
    chars = []

    while number > 0:
        number, remainder = divmod(number, base)
        chars.append(BASE62_ALPHABET[remainder])

    return "".join(reversed(chars))

def make_id(sequence: int) -> str:
    shard_id = 1
    #unique_id = (self.shard_id << SEQUENCE_BITS) | (sequence)
    unique_id = (sequence << SHARD_BITS) | shard_id
    return base62_encode(unique_id)

# Create N entries
TOTAL_LINKS = 1000000
with open("seed_links.csv", "w") as file:
     writer = csv.writer(file)
     for sequence in range(1, TOTAL_LINKS + 1):
          short_id = make_id(sequence)
          full_url = f"https://example.com/page/{sequence}"

          writer.writerow([sequence, short_id, full_url])